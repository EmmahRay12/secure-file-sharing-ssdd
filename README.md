# Secure File Sharing Application

A secure, web-based file sharing platform built with Python (Flask) that implements **AES-256-GCM encryption**, **user authentication**, and **Role-Based Access Control (RBAC)** to protect sensitive data during storage and transmission.

---

## 📋 Project Information

| Item | Details |
|------|---------|
| **Course** | SSDD (Secure Software Design & Development) |
| **Technology** | Python Flask, HTML/CSS/JS, SQLite |
| **Security** | AES-256-GCM Encryption, RBAC, SHA-256 Hashing |
| **Type** | Academic Prototype |

---

## 🛡️ Key Security Features

1. **AES-256-GCM Encryption** - All files are encrypted with unique per-file keys before storage
2. **Master Key Protection** - Per-file keys are encrypted with a master key
3. **Secure Authentication** - Password hashing with Werkzeug's PBKDF2
4. **Role-Based Access Control (RBAC)** - Admin and User roles with granular permissions
5. **File Integrity Verification** - SHA-256 hash verification on every download
6. **Activity Logging** - Complete audit trail of all user actions
7. **Session Security** - HTTP-only cookies, secure session management

---

## 👥 Team Members

| Member | Responsibility |
|--------|---------------|
| Noor e Emaan Fatima | Frontend, documentation, and testing support |
| Mahaz Hafeez | Backend development and security implementation |
| Arooba Fatima | UI design and frontend development |
| Umm e Momina | Database design and integration |
| Fathima Zahra | Testing, validation, and documentation support |

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone/Extract the project:**
```bash
cd secure-file-sharing
```

2. **Create a virtual environment (recommended):**
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Run the application:**
```bash
python app.py
```

5. **Open in browser:**
```
http://localhost:5000
```

### Default Admin Account
```
Username: admin
Password: Admin@123
```

---

## 📁 Project Structure

```
secure-file-sharing/
├── app.py                  # Main Flask application with all routes
├── config.py               # Application configuration settings
├── models.py               # Database models (User, File, Permissions, Logs)
├── encryption.py           # AES-256-GCM encryption module
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation
│
├── static/
│   ├── css/
│   │   └── style.css       # Complete stylesheet
│   └── js/
│       └── main.js         # Frontend JavaScript
│
├── templates/
│   ├── base.html           # Base template with navigation
│   ├── index.html          # Landing page
│   ├── login.html          # Login page
│   ├── register.html       # Registration page
│   ├── dashboard.html      # User dashboard
│   ├── upload.html         # File upload page
│   ├── files.html          # My files listing
│   ├── shared_files.html   # Files shared with me
│   ├── file_details.html   # File details & sharing
│   ├── profile.html        # User profile
│   ├── admin.html          # Admin dashboard
│   ├── admin_users.html    # Admin user management
│   ├── admin_files.html    # Admin file management
│   ├── admin_logs.html     # Admin activity logs
│   └── error.html          # Error pages
│
├── uploads/                # Encrypted file storage (auto-created)
└── keys/                   # Encryption key storage (auto-created)
```

---

## 🔐 How Encryption Works

1. **Upload:** User selects a file to upload
2. **Key Generation:** A unique AES-256 key is generated for the file
3. **File Encryption:** The file is encrypted using AES-256-GCM with the unique key
4. **Key Encryption:** The file key is encrypted using the master key (PBKDF2 derived)
5. **Hash Generation:** SHA-256 hash is computed for integrity verification
6. **Storage:** Encrypted file is saved; metadata and encrypted key are stored in database

### Download Process:
1. User requests download (must have permission)
2. File key is decrypted from database
3. File is decrypted using the file key
4. SHA-256 integrity check is performed
5. Original file is sent to the user

---

## 👤 User Roles

### Admin
- Manage all users (activate/deactivate, change roles)
- View all uploaded files
- Download any file
- View complete activity logs
- Delete any file

### Regular User
- Register and login
- Upload and manage own files
- Share files with specific users (view/download permissions)
- Download own files and files shared with them
- View own activity history
- Update profile and password

---

## 🔧 Technologies Used

| Component | Technology |
|-----------|-----------|
| Frontend | HTML5, CSS3, JavaScript |
| Backend | Python 3, Flask |
| Database | SQLite (SQLAlchemy ORM) |
| Encryption | AES-256-GCM (cryptography library) |
| Password Hashing | Werkzeug (PBKDF2-SHA256) |
| Icons | Font Awesome 6 |
| Fonts | Google Fonts (Inter) |
