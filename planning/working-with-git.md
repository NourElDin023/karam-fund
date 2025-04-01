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
