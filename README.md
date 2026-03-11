# 🏥 Aarogyam Multi-Speciality Clinic Management System

<div align="center">

![Django](https://img.shields.io/badge/Django-6.0-092E20?style=for-the-badge&logo=django&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.14-3776AB?style=for-the-badge&logo=python&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-18-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.0-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white)

**A full-stack web-based Clinic Management System built with Django & PostgreSQL.**  
Streamlining clinic operations — from appointment booking to digital prescriptions.

</div>

---

## 📋 Table of Contents

- [About the Project](#-about-the-project)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [System Modules](#-system-modules)
- [Database Design](#-database-design)
- [Screenshots](#-screenshots)
- [Installation & Setup](#-installation--setup)
- [Project Structure](#-project-structure)
- [Usage](#-usage)
- [Developer](#-developer)

---

## 📖 About the Project

**Aarogyam Multi-Speciality Clinic Management System** is a comprehensive web application designed to digitize and streamline the day-to-day operations of a multi-speciality clinic. The system replaces manual record-keeping with an efficient, secure, and user-friendly digital platform.

This project was developed as a **Final Year Project** for T.Y. B.Sc. (Computer Science), Semester VI at **Shri Dnyaneshwar Mahavidyalaya, Newasa**.

### 🎯 Problem Statement
Traditional clinics face challenges like:
- Manual appointment scheduling leading to double bookings
- Paper-based patient records that are hard to manage
- No digital prescription system
- Lack of real-time availability information

### ✅ Our Solution
A complete digital clinic management system with role-based access, real-time slot booking, and digital prescriptions with PDF download.

---

## ✨ Features

### 🔐 Authentication & Security
- Custom User model with three roles: **Admin**, **Staff**, **Patient**
- Login security: **5 failed attempts → 15-minute lockout**
- Show/Hide password toggle
- Remember Me functionality
- Forgot Password with email reset link
- Role-based dashboard routing

### 🌐 Public Booking System
- Public landing page (no login required)
- Online appointment booking form
- Real-time slot availability check (AJAX)
- Auto-creates patient records by phone number
- Doctor grid display with specialization

### 📅 Appointment Management
- Book, view, edit, and delete appointments
- 9 time slots (9:00 AM – 5:00 PM)
- Double-booking prevention
- Status tracking: Pending → Confirmed → Completed → Cancelled
- Filter available slots by doctor and date

### 💊 Prescription System
- Digital prescription creation per appointment
- Add multiple medicines with dosage, duration, instructions
- Diagnosis and doctor notes
- Next visit date scheduling
- **PDF download** of prescription
- Edit existing prescriptions

### 👨‍⚕️ Doctor Management
- Add, edit, delete doctors
- Specialization, experience, contact details
- Bio and profile information

### 👤 Patient Management
- Patient records with contact and medical info
- View appointment history
- Patient dashboard with prescription access

### 📊 Analytics & Reports
- Admin dashboard with key statistics
- Appointment trends
- Revenue and patient reports

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Backend Framework** | Django 6.0 |
| **Programming Language** | Python 3.14 |
| **Database** | PostgreSQL 18 |
| **Frontend** | Bootstrap 5, HTML5, CSS3, JavaScript |
| **Icons** | Font Awesome 6 |
| **Fonts** | Outfit, Plus Jakarta Sans (Google Fonts) |
| **PDF Generation** | xhtml2pdf |
| **Version Control** | Git & GitHub |
| **IDE** | Visual Studio Code |

### 🎨 Design System
| Element | Value |
|---------|-------|
| Primary Color | `#0ea5e9` (Sky Blue) |
| Success Color | `#10b981` (Emerald) |
| Warning Color | `#f59e0b` (Amber) |
| Secondary Color | `#6366f1` (Indigo) |
| Background | `#0f172a` (Dark Navy) |
| Card Background | `#1e293b` |
| Theme | Dark Mode |

---

## 🗂️ System Modules

```
Aarogyam CMS
├── 🔐 Authentication Module
│   ├── Login / Logout
│   ├── Role-based Access Control
│   ├── Password Reset
│   └── Login Security (Lockout)
│
├── 🌐 Public Module
│   ├── Landing Page
│   ├── Online Appointment Booking
│   └── Real-time Slot Availability
│
├── 📅 Appointment Module
│   ├── Appointment List
│   ├── Add / Edit / Delete
│   ├── Status Management
│   └── Time Slot Management
│
├── 💊 Prescription Module
│   ├── Add Prescription
│   ├── Medicine Management
│   ├── View Prescription
│   └── PDF Download
│
├── 👨‍⚕️ Doctor Module
│   ├── Doctor List
│   ├── Add / Edit / Delete
│   └── Specialization Management
│
├── 👤 Patient Module
│   ├── Patient List
│   ├── Patient Dashboard
│   └── Appointment History
│
└── 📊 Analytics Module
    ├── Admin Dashboard
    ├── Appointment Statistics
    └── Reports
```

---

## 🗄️ Database Design

### Entities & Relationships

```
Patient (1) ──────── (M) Appointment
Doctor  (1) ──────── (M) Appointment
Appointment (1) ──── (1) Prescription
Prescription (1) ─── (M) Medicine
```

### Key Models

**Patient**
| Field | Type |
|-------|------|
| patient_id | PK, AutoField |
| first_name | CharField |
| last_name | CharField |
| phone | CharField (unique) |
| age | IntegerField |
| gender | CharField |
| address | TextField |
| email | EmailField |

**Doctor**
| Field | Type |
|-------|------|
| doctor_id | PK, AutoField |
| first_name | CharField |
| last_name | CharField |
| specialization | CharField |
| phone | CharField |
| email | EmailField |
| experience_years | IntegerField |
| bio | TextField |

**Appointment**
| Field | Type |
|-------|------|
| appointment_id | PK, AutoField |
| patient | FK → Patient |
| doctor | FK → Doctor |
| appointment_date | DateField |
| time_slot | CharField |
| status | CharField |
| notes | TextField |
| created_at | DateTimeField |

**Prescription**
| Field | Type |
|-------|------|
| prescription_id | PK, AutoField |
| appointment | OneToOneField → Appointment |
| diagnosis | TextField |
| doctor_notes | TextField |
| next_visit_date | DateField |
| created_at | DateTimeField |

**Medicine**
| Field | Type |
|-------|------|
| medicine_id | PK, AutoField |
| prescription | FK → Prescription |
| name | CharField |
| dosage | CharField |
| duration | CharField |
| instructions | CharField |

---

## ⚙️ Installation & Setup

### Prerequisites
- Python 3.10+
- PostgreSQL 14+
- Git

### Step 1 — Clone the Repository
```bash
git clone https://github.com/Indr45thiscode/Aarogyam-Clinic_-Appointment.git
cd Aarogyam-Clinic_-Appointment
```

### Step 2 — Create Virtual Environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### Step 3 — Install Dependencies
```bash
pip install django
pip install psycopg2-binary
pip install xhtml2pdf
pip install pillow
```

### Step 4 — Database Setup (PostgreSQL)
```sql
CREATE DATABASE clinic_db;
CREATE USER clinic_user WITH PASSWORD 'yourpassword';
GRANT ALL PRIVILEGES ON DATABASE clinic_db TO clinic_user;
```

### Step 5 — Configure Settings
In `clinic_appointment/settings.py`, update:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'clinic_db',
        'USER': 'clinic_user',
        'PASSWORD': 'yourpassword',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### Step 6 — Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 7 — Create Superuser
```bash
python manage.py createsuperuser
```

### Step 8 — Run Server
```bash
python manage.py runserver
```

Visit: **http://127.0.0.1:8000**

---

## 📁 Project Structure

```
clinic_app/
│
├── accounts/                  # Authentication app
│   ├── models.py             # Custom User model
│   ├── views.py              # Login, logout, password reset
│   └── urls.py
│
├── appointments/              # Appointment & Prescription app
│   ├── models.py             # Doctor, Appointment, Prescription, Medicine
│   ├── views.py              # All appointment & prescription views
│   └── urls.py
│
├── patients/                  # Patient management app
│   ├── models.py             # Patient model
│   ├── views.py              # Patient CRUD & dashboard
│   └── urls.py
│
├── analytics/                 # Analytics & reports app
│
├── clinic_appointment/        # Main Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── templates/                 # All HTML templates
│   ├── base.html             # Base layout
│   ├── dashboard.html        # Admin dashboard
│   ├── accounts/             # Login, forgot password
│   ├── appointments/         # Appointment & prescription templates
│   ├── doctors/              # Doctor management
│   ├── patients/             # Patient management
│   └── public/               # Public landing page
│
├── static/                    # Static files (CSS, JS, images)
├── manage.py
└── README.md
```

---

## 🚀 Usage

### Admin/Staff Login
1. Go to `http://127.0.0.1:8000/login/`
2. Enter credentials
3. Access full dashboard

### Public Appointment Booking
1. Go to `http://127.0.0.1:8000/`
2. Fill in patient details
3. Select doctor, date & time slot
4. Submit booking

### Writing a Prescription
1. Go to **Appointments**
2. Click **Rx** button next to an appointment
3. Add diagnosis, medicines, doctor notes
4. Set next visit date
5. Click **Save Prescription**
6. Download PDF using **PDF** button

---

## 👨‍💻 Developer

| | |
|--|--|
| **Name** | Indrajit Namdeo Sawant |
| **Course** | T.Y. B.Sc. (Computer Science) |
| **Semester** | VI |
| **College** | Shri Dnyaneshwar Mahavidyalaya, Newasa |
| **GitHub** | [@Indr45thiscode](https://github.com/Indr45thiscode) |

---

## 📄 License

This project is developed for academic purposes.  
© 2026 Aarogyam Clinic Management System — Indrajit Namdeo Sawant

---

<div align="center">
  <strong>🏥 Aarogyam — Your Wellness Is Our Responsibility</strong>
</div>
