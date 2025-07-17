# 🍔 Food Delivery Web App

A full-stack food delivery platform built for IFN582 (Web Computing) at QUT.  
It simulates a real-world online ordering system, complete with user accounts, restaurant listings, cart functionality, and admin features.

---

## 🚀 Features

- User registration and login  
- Restaurant and food item management  
- Admin-only access and functionality  
- Dynamic cart system tied to a user's basket  
- Relational MySQL database schema  
- Flask backend with HTML/CSS/JS frontend  

---

## 🛠 Tech Stack

- Python (Flask)  
- HTML/CSS/JavaScript  
- MySQL  
- SQLAlchemy  

---

## ⚙️ Setup Instructions

### 📦 Install Dependencies

#### Windows  
py -m pip install -r requirements.txt

#### macOS  
You may need to set compiler flags to locate `mysql.h` before installation. First locate it:  
sudo find /usr -name mysql.h

Then update the `mysqlhome` variable in `mac.sh` if needed. Run:  
chmod +x ./mac.sh && sudo ./mac.sh

---

## 🗃️ Database Setup

1. Execute the `Assignment2.SQL` script to create and populate the database.  
2. Ensure the following line is updated in your Flask config:  
app.config['MYSQL_PASSWORD'] = 'your_password_here'

> Replace `'your_password_here'` with your actual MySQL root password.

---

## 🧱 Database Structure

- Food — Stores food items  
- Restaurant — Stores restaurants  
- RestaurantItem — Many-to-many relationship between food and restaurants  
- User — User login details and roles  
- Admin — Users with admin privileges  
- Basket — One basket per user (auto-generated on sign-up)  
- Selection — Items added to a user's cart  

---

## 👤 Preloaded Accounts

This system comes preloaded with:  
- 2 Admin accounts  
- 4 Basic user accounts  

❗ For security, default usernames/passwords have been removed from the public repo. You can create your own test users or edit the seeding logic in `Assignment2.SQL`.

---

## 📌 Notes

This repository is a clean, public version of the original private assignment submission.  
All credentials and sensitive data have been removed.  
If you'd like a walk-through or want to know more about the architecture, feel free to reach out!

---

## 📬 Contact

Built by Joshua Cox and Alek Karoli  
Graduate Certificate in IT – QUT
