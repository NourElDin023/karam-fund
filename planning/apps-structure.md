# Karam Fund App Structure

| **App Name**          | **Models Included**                                                 | **Description**                                                       |
| --------------------- | ------------------------------------------------------------------- | --------------------------------------------------------------------- |
| **`admin_dashboard`** | `AdminSelectedProjects`                                             | Allows admins to feature projects and manage reports.                 |
| **`donations`**       | `ProjectDonations`                                                  | Manages donations, tracking user contributions to projects.           |
| **`interactions`**    | `ProjectComments`, `ProjectRate`                                    | Handles user comments, replies, and project ratings.                  |
| **`projects`**        | `Project`, `ProjectCategory`, `ProjectMedia`, `ProjectTags`, `tags` | Handles project creation, media uploads, categories, and tags.        |
| **`reports`**         | `ProjectReport`, `CommentReport`                                    | Stores and manages reports on projects and comments for admin review. |
| **`users`**           | `User`                                                              | Manages user authentication, profiles, and account settings.          |
