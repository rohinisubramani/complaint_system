from django.shortcuts import render, redirect
from django.contrib import messages
from . import db
from .decorators import login_required_user, admin_required

# Complaint Categories as specified in prompt
CATEGORIES = [
    'Academic',
    'Hostel',
    'Transport',
    'Canteen',
    'Library',
    'Infrastructure',
    'Internet/Wi-Fi',
    'Other'
]

STATUSES = ['Pending', 'In Progress', 'Resolved', 'Rejected']


def home(request):
    """Landing Home Page."""
    return render(request, 'home.html')


def user_register(request):
    """User Registration View."""
    if request.session.get('user_id'):
        return redirect('user_dashboard')

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip().lower()
        password = request.POST.get('password', '').strip()
        confirm_password = request.POST.get('confirm_password', '').strip()

        # Backend Validation
        if not name or not email or not password or not confirm_password:
            messages.error(request, "All fields are required.")
            return render(request, 'register.html', {'name': name, 'email': email})

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, 'register.html', {'name': name, 'email': email})

        if len(password) < 6:
            messages.error(request, "Password must be at least 6 characters long.")
            return render(request, 'register.html', {'name': name, 'email': email})

        success, msg = db.register_user(name, email, password, role='user')
        if success:
            messages.success(request, "Registration successful! You can now log in.")
            return redirect('user_login')
        else:
            messages.error(request, msg)
            return render(request, 'register.html', {'name': name, 'email': email})

    return render(request, 'register.html')


def user_login(request):
    """User/Student Login View."""
    if request.session.get('user_id'):
        if request.session.get('role') == 'admin':
            return redirect('admin_dashboard')
        return redirect('user_dashboard')

    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()

        if not email or not password:
            messages.error(request, "Email and Password are required.")
            return render(request, 'login.html', {'email': email})

        user, err = db.authenticate_user(email, password, required_role=None)
        if user:
            request.session['user_id'] = user['email']
            request.session['user_name'] = user['name']
            request.session['role'] = user['role']

            messages.success(request, f"Welcome back, {user['name']}!")
            if user['role'] == 'admin':
                return redirect('admin_dashboard')
            return redirect('user_dashboard')
        else:
            messages.error(request, err)
            return render(request, 'login.html', {'email': email})

    return render(request, 'login.html')


def user_logout(request):
    """Logout action."""
    request.session.flush()
    messages.info(request, "You have been logged out successfully.")
    return redirect('home')


@login_required_user
def user_dashboard(request):
    """User Dashboard View."""
    user_email = request.session.get('user_id')
    stats = db.get_complaint_stats(user_email=user_email)
    user_complaints = db.get_user_complaints(user_email)
    recent_complaints = user_complaints[:5]  # Limit to 5 recent

    context = {
        'user_name': request.session.get('user_name'),
        'stats': stats,
        'recent_complaints': recent_complaints,
    }
    return render(request, 'dashboard.html', context)


@login_required_user
def submit_complaint(request):
    """Submit Complaint View."""
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        category = request.POST.get('category', '').strip()
        description = request.POST.get('description', '').strip()
        location = request.POST.get('location', '').strip()

        if not title or not category or not description or not location:
            messages.error(request, "Please fill in all required fields.")
            return render(request, 'submit_complaint.html', {
                'categories': CATEGORIES,
                'title': title,
                'category': category,
                'description': description,
                'location': location
            })

        if category not in CATEGORIES:
            messages.error(request, "Invalid category selected.")
            return render(request, 'submit_complaint.html', {'categories': CATEGORIES})

        user_email = request.session.get('user_id')
        user_name = request.session.get('user_name', 'Student')

        complaint_id = db.create_complaint(
            user_email=user_email,
            user_name=user_name,
            title=title,
            category=category,
            description=description,
            location=location
        )

        messages.success(request, f"Complaint submitted successfully! Your Ticket ID is {complaint_id}.")
        return redirect('my_complaints')

    return render(request, 'submit_complaint.html', {'categories': CATEGORIES})


@login_required_user
def my_complaints(request):
    """List student's submitted complaints."""
    user_email = request.session.get('user_id')
    status_filter = request.GET.get('status', '').strip()
    category_filter = request.GET.get('category', '').strip()

    complaints = db.get_user_complaints(user_email)

    if status_filter:
        complaints = [c for c in complaints if c.get('status') == status_filter]
    if category_filter:
        complaints = [c for c in complaints if c.get('category') == category_filter]

    context = {
        'complaints': complaints,
        'categories': CATEGORIES,
        'statuses': STATUSES,
        'selected_status': status_filter,
        'selected_category': category_filter,
    }
    return render(request, 'my_complaints.html', context)


@login_required_user
def complaint_detail(request, complaint_id):
    """View details of a specific complaint."""
    user_email = request.session.get('user_id')
    role = request.session.get('role')

    complaint = db.get_complaint_by_id(complaint_id)
    if not complaint:
        messages.error(request, "Complaint not found.")
        return redirect('user_dashboard' if role != 'admin' else 'admin_dashboard')

    # Security check: Non-admin users can only view their own complaint
    if role != 'admin' and complaint.get('user_id') != user_email:
        messages.error(request, "Access denied. You cannot view another student's complaint.")
        return redirect('user_dashboard')

    context = {
        'complaint': complaint,
        'statuses': STATUSES,
        'is_admin': role == 'admin'
    }
    return render(request, 'complaint_detail.html', context)


@login_required_user
def delete_complaint(request, complaint_id):
    """Delete pending complaint (Student action)."""
    user_email = request.session.get('user_id')
    if request.method == 'POST':
        success, msg = db.delete_complaint_by_id(complaint_id, user_email=user_email, is_admin=False)
        if success:
            messages.success(request, msg)
        else:
            messages.error(request, msg)
    return redirect('my_complaints')


@login_required_user
def user_profile(request):
    """User Profile View."""
    user_email = request.session.get('user_id')
    user = db.get_user_by_email(user_email)
    stats = db.get_complaint_stats(user_email=user_email)

    context = {
        'user': user,
        'stats': stats
    }
    return render(request, 'profile.html', context)


# --- ADMIN VIEWS ---

def admin_login(request):
    """Admin Login View."""
    if request.session.get('user_id') and request.session.get('role') == 'admin':
        return redirect('admin_dashboard')

    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()

        if not email or not password:
            messages.error(request, "Admin email and password required.")
            return render(request, 'admin_login.html', {'email': email})

        user, err = db.authenticate_user(email, password, required_role='admin')
        if user:
            request.session['user_id'] = user['email']
            request.session['user_name'] = user['name']
            request.session['role'] = user['role']

            messages.success(request, f"Logged in as Administrator ({user['name']}).")
            return redirect('admin_dashboard')
        else:
            messages.error(request, err or "Invalid admin credentials.")
            return render(request, 'admin_login.html', {'email': email})

    return render(request, 'admin_login.html')


@admin_required
def admin_dashboard(request):
    """Admin Dashboard Overview."""
    stats = db.get_complaint_stats()
    total_users = db.get_total_users_count()
    recent_complaints = db.get_all_complaints()[:5]

    context = {
        'stats': stats,
        'total_users': total_users,
        'recent_complaints': recent_complaints,
    }
    return render(request, 'admin_dashboard.html', context)


@admin_required
def admin_complaints(request):
    """Admin All Complaints View with Search and Filter."""
    search_query = request.GET.get('search', '').strip()
    status_filter = request.GET.get('status', '').strip()
    category_filter = request.GET.get('category', '').strip()

    complaints = db.get_all_complaints(
        search_query=search_query,
        status_filter=status_filter,
        category_filter=category_filter
    )

    context = {
        'complaints': complaints,
        'categories': CATEGORIES,
        'statuses': STATUSES,
        'search_query': search_query,
        'selected_status': status_filter,
        'selected_category': category_filter,
    }
    return render(request, 'admin_complaints.html', context)


@admin_required
def admin_update_complaint(request, complaint_id):
    """Admin action to update complaint status and post admin response."""
    if request.method == 'POST':
        status = request.POST.get('status', '').strip()
        admin_response = request.POST.get('admin_response', '').strip()

        if status and status in STATUSES:
            db.update_complaint(complaint_id, status=status, admin_response=admin_response)
            messages.success(request, f"Complaint {complaint_id} updated successfully.")
        else:
            messages.error(request, "Invalid status provided.")

    return redirect(request.META.get('HTTP_REFERER', 'admin_complaints'))


@admin_required
def admin_delete_complaint(request, complaint_id):
    """Admin action to delete inappropriate complaints."""
    if request.method == 'POST':
        success, msg = db.delete_complaint_by_id(complaint_id, is_admin=True)
        if success:
            messages.success(request, msg)
        else:
            messages.error(request, msg)

    return redirect('admin_complaints')


@admin_required
def admin_users(request):
    """Admin view of all registered users."""
    users = db.get_all_users()
    total_users = len(users)

    context = {
        'users': users,
        'total_users': total_users,
    }
    return render(request, 'admin_users.html', context)
