# KaramFund

**Karam in Action, Change in Motion.**

KaramFund is a crowdfunding platform designed to connect donors with impactful projects, fostering a culture of generosity and positive change.

## 🚀 Features

-   Secure and user-friendly donation system
-   Campaign creation and management
-   Transparent funding progress tracking
-   User authentication and profile management
-   Integration with payment gateways
-   Responsive and accessible UI

## 🛠️ Tech Stack

-   **Frontend:** React, Bootstrap
-   **Backend:** Django, Django REST Framework
-   **Database:** PostgreSQL
-   **Hosting:** PythonAnywhere

---

# Git Branching Workflow for KaramFund

## 1. Clone the Repository (For New Team Members)
If a team member hasn't cloned the repo yet, they should run:
```bash
git clone git@github.com:NourElDin023/karam-fund.git
cd karamfund
```

## 2. Set Up the Main Branch
Since all features will be merged into `main`, it's essential to avoid direct commits to `main`.

- Make sure you're on the `main` branch:
  ```bash
  git checkout main
  ```
- Pull the latest changes:
  ```bash
  git pull origin main
  ```

## 3. Creating a New Feature Branch
Whenever a team member starts working on a new feature:

- **Pull the latest `main` branch:**  
  ```bash
  git checkout main
  git pull origin main
  ```
- **Create a new feature branch:**
  ```bash
  git checkout -b feature/your-feature-name
  ```
  Examples:
  - `feature/authentication`
  - `feature/project-management`
  - `feature/donations`

## 4. Working on the Feature
Make changes and add files. After coding:
```bash
git add .
git commit -m "Implemented authentication system"
git push origin feature/your-feature-name
```

## 5. Opening a Pull Request (PR)
- Go to GitHub.
- Navigate to the **Pull Requests** tab.
- Click **New Pull Request**.
- Select **base branch** → `main`, and **compare** → `feature/your-feature-name`.
- Add a meaningful title and description.
- Click **Create Pull Request**.

## 6. Code Review & Merging
- At least one team member should review the PR.
- If approved, **merge into `main`**.
- After merging, **delete the feature branch** from GitHub.

To delete the local feature branch after merging:
```bash
git checkout main
git pull origin main
git branch -d feature/your-feature-name 
```

## Summary of Workflow
1. **Always work on a feature branch** (`feature/your-feature-name`).  
2. **Regularly pull updates** from `main` before starting new work.  
3. **Push to GitHub & open a PR** to merge into `main`.  
4. **Review and merge into `main`**.  
5. **Delete the feature branch after merging.**  

Following these steps ensures a smooth collaboration and clean repository history. 🚀
<!-- 
---
# 🚀 KaramFund Project - Task List

## ✅ Completed Tasks

### 🔹 Project Setup
- [x] Created a Django project (`karamfund`)
- [x] Initialized Git repository and pushed to GitHub
- [x] Set up a virtual environment
- [x] Installed required dependencies (`requirements.txt`)
- [x] Configured `settings.py` (Database, Static & Media files, CORS, REST framework)
- [x] Created essential Django apps: 
  - `accounts`
  - `projects`
  - `donations`
  - `categories`
  - `comments`
  - `ratings`
  - `reports`
- [x] Set up Git branching strategy (`main`, `feature/*` branches)
- [x] Configured `.gitignore`

### 🔹 GitHub Setup
- [x] Created GitHub repository
- [x] Established GitHub branching workflow
- [x] Created GitHub Project Board (Kanban)
- [x] Distributed work among team members

## 📌 Pending Tasks

### 🔹 User Authentication & Authorization
👤 **Assigned to: Person 1**
- [ ] Implement user registration & login
- [ ] Email verification & password reset
- [ ] Social authentication (optional)
- [ ] JWT authentication setup
- [ ] User profile management

### 🔹 Project Management Features
📁 **Assigned to: Person 2**
- [ ] CRUD operations for projects
- [ ] Handle project images, tags, and categories
- [ ] Implement project deadlines & funding targets
- [ ] Manage project ownership & contributors

### 🔹 Donations System
💰 **Assigned to: Person 3**
- [ ] Implement donation functionality
- [ ] Track donation history per user
- [ ] Ensure payment security (mock or real)
- [ ] Connect donations to project funding progress

### 🔹 Comments & Ratings System
📝 **Assigned to: Person 4**
- [ ] CRUD operations for comments & nested replies
- [ ] Implement project rating system
- [ ] Handle user interactions (likes, edits, deletions)
- [ ] Prevent spam & enforce moderation rules

### 🔹 Reports & Admin Dashboard
📊 **Assigned to: Person 5**
- [ ] Implement reporting system (users flagging issues)
- [ ] Set up admin dashboard for managing users & projects
- [ ] Manage reported content (review/delete)
- [ ] Generate analytics for project performance 
--- 
🚀 *Let's build KaramFund together!*
-->