import datetime
from pymongo import MongoClient, ASCENDING, DESCENDING
from django.conf import settings
from django.contrib.auth.hashers import make_password, check_password

# Initialize MongoDB Client
client = MongoClient(settings.MONGO_URI, serverSelectionTimeoutMS=5000)
db = client[settings.MONGO_DB_NAME]

# Collections
users_collection = db['users']
complaints_collection = db['complaints']

# Create indexes for performance & constraints
try:
    users_collection.create_index([("email", ASCENDING)], unique=True)
    complaints_collection.create_index([("complaint_id", ASCENDING)], unique=True)
    complaints_collection.create_index([("user_id", ASCENDING)])
    complaints_collection.create_index([("status", ASCENDING)])
    complaints_collection.create_index([("category", ASCENDING)])
except Exception as e:
    print(f"MongoDB index creation notice: {e}")


def seed_initial_data():
    """Seed default users and demo complaints if collections are empty."""
    if users_collection.count_documents({}) == 0:
        # Create Default Admin
        users_collection.insert_one({
            "name": "System Administrator",
            "email": "admin@college.edu",
            "password": make_password("admin123"),
            "role": "admin",
            "created_at": datetime.datetime.now(datetime.timezone.utc)
        })

        # Create Default Demo Student
        users_collection.insert_one({
            "name": "Alex Morgan",
            "email": "student@college.edu",
            "password": make_password("student123"),
            "role": "user",
            "created_at": datetime.datetime.now(datetime.timezone.utc)
        })
        print("Initial users seeded.")

    if complaints_collection.count_documents({}) == 0:
        now = datetime.datetime.now(datetime.timezone.utc)
        demo_complaints = [
            {
                "complaint_id": "CMP-1001",
                "user_id": "student@college.edu",
                "user_name": "Alex Morgan",
                "title": "Wi-Fi speed extremely slow in Hostel Block B",
                "category": "Internet/Wi-Fi",
                "description": "The Wi-Fi access point on the 2nd floor of Block B drops connection repeatedly and speeds are below 100kbps during evening hours.",
                "location": "Hostel Block B, 2nd Floor",
                "status": "In Progress",
                "admin_response": "IT support team assigned. Router access point replacement scheduled for tomorrow morning.",
                "created_at": now - datetime.timedelta(days=2),
                "updated_at": now - datetime.timedelta(days=1)
            },
            {
                "complaint_id": "CMP-1002",
                "user_id": "student@college.edu",
                "user_name": "Alex Morgan",
                "title": "Library AC leaking water near study desks",
                "category": "Library",
                "description": "Air conditioner #3 on the main library floor is leaking water directly onto study table 12.",
                "location": "Main Library Ground Floor",
                "status": "Pending",
                "admin_response": "",
                "created_at": now - datetime.timedelta(hours=12),
                "updated_at": now - datetime.timedelta(hours=12)
            },
            {
                "complaint_id": "CMP-1003",
                "user_id": "student@college.edu",
                "user_name": "Alex Morgan",
                "title": "Broken projector in Seminar Hall 2",
                "category": "Infrastructure",
                "description": "The ceiling projector has a damaged HDMI port and flickers red color intermittently.",
                "location": "Academic Building 1, Room 204",
                "status": "Resolved",
                "admin_response": "HDMI cable and connector board replaced. Tested and fully operational.",
                "created_at": now - datetime.timedelta(days=5),
                "updated_at": now - datetime.timedelta(days=3)
            }
        ]
        complaints_collection.insert_many(demo_complaints)
        print("Demo complaints seeded.")


# Run Seeding automatically on module import
try:
    seed_initial_data()
except Exception as e:
    print(f"Error seeding database: {e}")


# --- USER HELPER FUNCTIONS ---

def register_user(name, email, password, role="user"):
    """Register a new user in MongoDB."""
    email_clean = email.strip().lower()
    if users_collection.find_one({"email": email_clean}):
        return False, "An account with this email already exists."
    
    hashed_pwd = make_password(password)
    user_doc = {
        "name": name.strip(),
        "email": email_clean,
        "password": hashed_pwd,
        "role": role,
        "created_at": datetime.datetime.now(datetime.timezone.utc)
    }
    result = users_collection.insert_one(user_doc)
    return True, str(result.inserted_id)


def authenticate_user(email, password, required_role=None):
    """Authenticate user credentials against MongoDB."""
    email_clean = email.strip().lower()
    user = users_collection.find_one({"email": email_clean})
    if not user:
        return None, "Invalid email address or password."
    
    if not check_password(password, user["password"]):
        return None, "Invalid email address or password."
    
    if required_role and user.get("role") != required_role:
        return None, f"Access denied. Account is not authorized as {required_role}."
    
    return user, None


def get_user_by_email(email):
    """Fetch user by email."""
    return users_collection.find_one({"email": email.strip().lower()})


def get_all_users():
    """Fetch list of all registered users."""
    users = list(users_collection.find({}, {"password": 0}).sort("created_at", DESCENDING))
    for u in users:
        u["id_str"] = str(u["_id"])
    return users


def get_total_users_count():
    """Get total count of registered users."""
    return users_collection.count_documents({})


# --- COMPLAINT HELPER FUNCTIONS ---

def generate_complaint_id():
    """Generate next sequential Complaint ID (e.g. CMP-1004)."""
    complaints = list(complaints_collection.find({}, {"complaint_id": 1}))
    max_num = 1000
    for c in complaints:
        cid = c.get("complaint_id", "")
        if cid.startswith("CMP-"):
            try:
                num = int(cid.split("-")[1])
                if num > max_num:
                    max_num = num
            except Exception:
                pass
    return f"CMP-{max_num + 1:04d}"



def create_complaint(user_email, user_name, title, category, description, location):
    """Create a new complaint record in MongoDB."""
    cid = generate_complaint_id()
    now = datetime.datetime.now(datetime.timezone.utc)
    doc = {
        "complaint_id": cid,
        "user_id": user_email.strip().lower(),
        "user_name": user_name.strip(),
        "title": title.strip(),
        "category": category.strip(),
        "description": description.strip(),
        "location": location.strip(),
        "status": "Pending",
        "admin_response": "",
        "created_at": now,
        "updated_at": now
    }
    complaints_collection.insert_one(doc)
    return cid


def get_complaint_by_id(complaint_id):
    """Fetch a single complaint by complaint_id."""
    return complaints_collection.find_one({"complaint_id": complaint_id.strip()})


def get_user_complaints(user_email):
    """Fetch complaints submitted by a specific user."""
    return list(complaints_collection.find({"user_id": user_email.strip().lower()}).sort("created_at", DESCENDING))


def get_all_complaints(search_query="", status_filter="", category_filter=""):
    """Fetch all complaints with optional search and filter parameters."""
    query = {}

    if status_filter:
        query["status"] = status_filter.strip()
    
    if category_filter:
        query["category"] = category_filter.strip()

    if search_query:
        sq = search_query.strip()
        query["$or"] = [
            {"complaint_id": {"$regex": sq, "$options": "i"}},
            {"title": {"$regex": sq, "$options": "i"}},
            {"description": {"$regex": sq, "$options": "i"}},
            {"user_name": {"$regex": sq, "$options": "i"}},
            {"location": {"$regex": sq, "$options": "i"}}
        ]

    return list(complaints_collection.find(query).sort("created_at", DESCENDING))


def update_complaint(complaint_id, status=None, admin_response=None):
    """Update complaint status and/or admin response."""
    update_data = {"updated_at": datetime.datetime.now(datetime.timezone.utc)}
    if status:
        update_data["status"] = status.strip()
    if admin_response is not None:
        update_data["admin_response"] = admin_response.strip()

    result = complaints_collection.update_one(
        {"complaint_id": complaint_id.strip()},
        {"$set": update_data}
    )
    return result.modified_count > 0


def delete_complaint_by_id(complaint_id, user_email=None, is_admin=False):
    """
    Delete a complaint.
    If user_email is provided (student action), only allow deleting if status is 'Pending'.
    Admin can delete any complaint.
    """
    query = {"complaint_id": complaint_id.strip()}
    if not is_admin:
        if not user_email:
            return False, "Unauthorized action."
        query["user_id"] = user_email.strip().lower()
        query["status"] = "Pending"

    comp = complaints_collection.find_one(query)
    if not comp:
        if not is_admin:
            return False, "Complaint not found or cannot be deleted (only Pending complaints can be deleted)."
        return False, "Complaint not found."

    complaints_collection.delete_one({"_id": comp["_id"]})
    return True, "Complaint deleted successfully."


def get_complaint_stats(user_email=None):
    """Calculate summary statistics for user or admin dashboard."""
    query = {}
    if user_email:
        query["user_id"] = user_email.strip().lower()

    total = complaints_collection.count_documents(query)
    
    pending_query = {**query, "status": "Pending"}
    pending = complaints_collection.count_documents(pending_query)

    in_progress_query = {**query, "status": "In Progress"}
    in_progress = complaints_collection.count_documents(in_progress_query)

    resolved_query = {**query, "status": "Resolved"}
    resolved = complaints_collection.count_documents(resolved_query)

    rejected_query = {**query, "status": "Rejected"}
    rejected = complaints_collection.count_documents(rejected_query)

    return {
        "total": total,
        "pending": pending,
        "in_progress": in_progress,
        "resolved": resolved,
        "rejected": rejected
    }
