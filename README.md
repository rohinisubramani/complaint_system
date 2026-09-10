# Complaint Management System

A simple and user-friendly **Complaint Management System** built using **HTML, CSS, JavaScript, Python, Django, and MongoDB (Atlas)**. Designed for college students to submit complaints and administrators to manage and resolve them.

---

## 🛠️ Technology Stack

| Layer | Technology |
|-------|------------|
| Frontend | HTML5, CSS3, JavaScript (Vanilla) |
| Backend | Python 3.x + Django 4.2 |
| Database | MongoDB Atlas (Cloud) / MongoDB Local |
| Styling | FontAwesome 6.4 + Google Fonts (Inter) |
| Libraries | PyMongo, python-dotenv |

---

## ✨ Features

### 👤 User / Student
- Register an account
- Login / Logout
- Dashboard with statistics (Total, Pending, In-Progress, Resolved)
- Submit a new complaint (8 categories)
- View all submitted complaints with filters
- Check complaint status & admin response
- Delete pending complaints
- View profile

### 🛡️ Admin
- Admin login portal (role-protected)
- Dashboard with 5 stat cards + recent complaints
- View, search, and filter all complaints
- Update complaint status (Pending → In Progress → Resolved → Rejected)
- Add admin response/notes
- Delete inappropriate complaints
- View all registered users

### 📋 Complaint Categories
Academic, Hostel, Transport, Canteen, Library, Infrastructure, Internet/Wi-Fi, Other

### 📊 Complaint Statuses
**Pending** → **In Progress** → **Resolved** / **Rejected**

---

## 📁 Project Structure

```
complaint system/
├── .env                          # Environment variables (MongoDB URI, Secret Key)
├── .env.example                  # Example env template
├── manage.py                     # Django management script
├── README.md                     # This file
├── requirements.txt              # Python dependencies
├── complaint_system/             # Django project config
│   ├── __init__.py
│   ├── settings.py               # Settings (DB, static, apps)
│   ├── urls.py                   # Root URL routing
│   ├── asgi.py
│   └── wsgi.py
└── complaints_app/               # Main Django application
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── db.py                     # PyMongo database layer (CRUD + seed)
    ├── decorators.py             # @login_required_user, @admin_required
    ├── models.py
    ├── tests.py
    ├── urls.py                   # App URL routes (18 endpoints)
    ├── views.py                  # All 14 views (user + admin)
    ├── migrations/
    ├── static/
    │   ├── css/
    │   │   └── style.css         # Complete responsive design system
    │   └── js/
    │       └── main.js           # Validation + modals + live search
    └── templates/
        ├── base.html             # Base layout with navbar
        ├── home.html             # Landing page
        ├── register.html         # Student registration
        ├── login.html            # Student login
        ├── dashboard.html        # Student dashboard
        ├── submit_complaint.html # Submit form
        ├── my_complaints.html    # Student's complaints list
        ├── complaint_detail.html # Complaint full details
        ├── profile.html          # Student profile
        ├── admin_login.html      # Admin login portal
        ├── admin_dashboard.html  # Admin dashboard
        ├── admin_complaints.html # Admin manage complaints
        └── admin_users.html      # Admin users directory
```

---

## 🚀 Quick Start — Commands to Run

### Step 1: Install Python
Make sure you have **Python 3.8+** installed. Check:
```bash
python --version
```

### Step 2: Navigate to the project folder
```bash
cd "c:\Users\Rohini S\OneDrive\Desktop\complaint system"
```

### Step 3: Install required dependencies
```bash
pip install django pymongo python-dotenv djongo
```

Or using the requirements file (create it first if needed):
```bash
pip install -r requirements.txt
```

### Step 4: Configure the .env file
The `.env` file is already set up with your MongoDB Atlas URI. You can edit it if needed:
```env
# MongoDB Atlas Connection String
MONGO_URI=mongodb+srv://complaint_system:IHpaRfyfwPmMYD09@cluster0.ef4e11o.mongodb.net/?appName=Cluster0

# MongoDB Database Name
MONGO_DB_NAME=complaint_system_db

# Django Secret Key (change this in production)
SECRET_KEY=django-insecure-%t9g@b7)cf3#5l20$88^28$rj+s#md)epp+pp40zxe!)lx9-5f
```

### Step 5: Apply Django migrations (for built-in admin/auth tables)
```bash
python manage.py migrate
```
> This will also automatically seed the database with default users and demo complaints on first run.

### Step 6: Start the Django development server
```bash
python manage.py runserver 0.0.0.0:8000
```

Or for default localhost:
```bash
python manage.py runserver
```

### Step 7: Open the application in your browser
👉 **http://localhost:8000/**

---

## 🔑 Default Login Credentials

On first run, the database is automatically seeded with these demo accounts:

| Role | Email Address | Password |
|------|---------------|----------|
| 🛡️ **Administrator** | `admin@college.edu` | `admin123` |
| 👤 **Student** | `student@college.edu` | `student123` |

> You can register new student accounts via the **Register** page. For new admin accounts, manually insert them into the MongoDB `users` collection with `role: "admin"`.

---

## 🗺️ All Pages / Routes

### Student Routes
| URL | Page |
|-----|------|
| `/` | Home Page |
| `/register/` | Student Registration |
| `/login/` | Student Login |
| `/logout/` | Logout |
| `/dashboard/` | Student Dashboard |
| `/submit-complaint/` | Submit New Complaint |
| `/my-complaints/` | My Complaints (with filters) |
| `/complaint/<ID>/` | Complaint Details |
| `/complaint/<ID>/delete/` | Delete Pending Complaint (POST) |
| `/profile/` | Student Profile |

### Admin Routes
| URL | Page |
|-----|------|
| `/admin-login/` | Admin Login Portal |
| `/admin-dashboard/` | Admin Dashboard |
| `/admin-complaints/` | Manage All Complaints (Search + Filter) |
| `/admin-complaints/<ID>/update/` | Update Status + Response (POST) |
| `/admin-complaints/<ID>/delete/` | Delete Any Complaint (POST) |
| `/admin-users/` | Registered Users Directory |

---

## 📋 Expected Workflow

### Student Flow
```
Register → Login → Dashboard → Submit Complaint → 
Complaint Saved (Status: Pending) → Check Status / View Admin Response
```

### Admin Flow
```
Admin Login → Admin Dashboard → View All Complaints → 
Open Complaint → Update Status → Add Admin Response → Save
```

---

## 🗄️ Database Collections (MongoDB)

### `users` Collection
```json
{
  "_id": "ObjectId",
  "name": "Student Name",
  "email": "student@college.edu",
  "password": "hashed_password",
  "role": "user",  // or "admin"
  "created_at": "ISODate"
}
```

### `complaints` Collection
```json
{
  "_id": "ObjectId",
  "complaint_id": "CMP-1004",
  "user_id": "student@college.edu",
  "user_name": "Student Name",
  "title": "Complaint title",
  "category": "Hostel",
  "description": "Detailed issue...",
  "location": "Block B Room 204",
  "status": "Pending",   // Pending | In Progress | Resolved | Rejected
  "admin_response": "",
  "created_at": "ISODate",
  "updated_at": "ISODate"
}
```

---

## 🔒 Security Features

- **Password Hashing** — Django's `make_password` / `check_password` (PBKDF2)
- **Role-Based Access** — Custom decorators `@login_required_user` and `@admin_required`
- **Session-Based Authentication** — Secured via Django sessions
- **User Isolation** — Students can only view/delete their own complaints
- **Deletion Rules** — Students can only delete **Pending** complaints; Admin can delete any
- **CSRF Protection** — All forms include Django CSRF tokens
- **Backend Validation** — All form data validated on server even if JS is disabled

---

## 🎨 UI Design

- Clean, modern, professional interface suitable for college projects
- Responsive layout (works on desktop, tablet, and mobile)
- **Color Theme**: Indigo (`#4f46e5`) primary with slate/gray neutrals
- Components: Navigation bar, Dashboard stat cards, Data tables, Forms, Buttons, Status badges, Modals
- Status Badges: Yellow (Pending), Blue (In Progress), Green (Resolved), Red (Rejected)

---

## 🛠️ Troubleshooting

### Issue: "MongoDB connection error"
- Check your internet connection (Atlas is cloud-based)
- Verify your IP is whitelisted in MongoDB Atlas Network Access settings
- Try adding your current IP to Atlas whitelist

### Issue: "Pip command not found"
```bash
python -m ensurepip --upgrade
python -m pip install django pymongo python-dotenv djongo
```

### Issue: Port 8000 already in use
```bash
python manage.py runserver 0.0.0.0:8001
```

### Issue: Reset / start fresh database
Connect to MongoDB Atlas via the web console and delete the `complaint_system_db` database, then run `migrate` again. Seeds will auto-create.

---

## 📦 Dependencies List

```
Django==4.2.30
pymongo==4.17.0
python-dotenv==1.2.2
djongo==1.2.31
dnspython==2.8.0
```

---

## 📝 Notes for College Project Presentation

1. **Architecture**: Explain the 3-tier setup — Browser (HTML/CSS/JS) → Django (Python Views) → MongoDB (Atlas Cloud)
2. **Authentication**: Walk through session-based auth + role decorators
3. **Database**: Show MongoDB Atlas collections (`users`, `complaints`) + indexes
4. **Demo Flow**: Register a new student → Submit complaint → Login as Admin → Update status & respond → Login as student → Check status update
5. **Security Points**: Mention password hashing, CSRF, role checks, user isolation

---

## 📄 License

Educational project suitable for college submission and demonstration.

---

**Built with ❤️ using Django + MongoDB Atlas**
