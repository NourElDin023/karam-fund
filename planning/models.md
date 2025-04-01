# `User` Model Fields

| Field Name       | Field Key          | Nullable | Data Type      | Key | Default Value |
| ---------------- | ------------------ | :------: | -------------- | --- | ------------- |
| ID               | `id`               |    ❌    | `int`          | PK  |               |
| First Name       | `first_name`       |    ❌    | `varchar`      | ❌  |               |
| Last Name        | `last_name`        |    ❌    | `varchar`      | ❌  |               |
| Email            | `email`            |    ❌    | `varchar`      | ❌  |               |
| Password         | `password`         |    ❌    | `varchar`      | ❌  |               |
| Phone Number     | `phone_number`     |    ❌    | `varchar (12)` | ❌  |               |
| Is Admin         | `is_admin`         |    ❌    | `boolean`      | ❌  | `false`       |
| Profile Picture  | `profile_picture`  |    ✔️    | `varchar`      | ❌  | `NULL`        |
| Bio              | `bio`              |    ✔️    | `text`         | ❌  | `NULL`        |
| Email Activated  | `is_activated`     |    ✔️    | `boolean`      | ❌  | `false`       |
| Birthdate        | `birthdate`        |    ✔️    | `date`         | ❌  | `NULL`        |
| Facebook Profile | `facebook_profile` |    ✔️    | `varchar`      | ❌  | `NULL`        |
| Country          | `country`          |    ✔️    | `varchar`      | ❌  | `NULL`        |
| Created At       | `created_at`       |    ❌    | `timestamp`    | ❌  | Timestamp     |

Notes:

- When a user deletes their account, all their projects and donations are moved to a dummy user `deleted_user` then the user entry is deleted from the database. This is to keep the integrity of the database and avoid orphaned records.
- Admins can't delete their accounts.
- When a user attempts to log in without activating their account, the system will automatically resend the activation email containing the activation link and display a message prompting the user to check their email for the link.

# `Project` Model Fields

| Field Name     | Field Key        | Nullable | Data Type | Key                       | Default Value |
| -------------- | ---------------- | :------: | --------- | ------------------------- | ------------- |
| ID             | `id`             |    ❌    | `int`     | PK                        |               |
| Title          | `title`          |    ❌    | `varchar` | ❌                        |               |
| Description    | `description`    |    ❌    | `text`    | ❌                        |               |
| target_amount  | `target_amount`  |    ❌    | `decimal` | ❌                        |               |
| current_amount | `current_amount` |    ❌    | `decimal` | ❌                        | 0             |
| Category       | `category`       |    ❌    | `int`     | FK (`ProjectCategory.id`) |               |
| Creator        | `creator`        |    ❌    | `int`     | FK (`User.id`)            |               |
| campaign_start | `campaign_start` |    ❌    | `date`    | ❌                        | Timestamp     |
| campaign_end   | `campaign_end`   |    ❌    | `date`    | ❌                        |               |
| Is Active      | `is_active`      |    ❌    | `boolean` | ❌                        | `true`        |
| Average Rating | `avg_rating`     |    ❌    | `decimal` | ❌                        | 0             |
| Is Reported    | `is_reported`    |    ❌    | `boolean` | ❌                        | `false`       |
| Is Deleted     | `is_deleted`     |    ❌    | `boolean` | ❌                        | `false`       |
| Is Cancelled   | `is_cancelled`   |    ❌    | `boolean` | ❌                        | `false`       |

Notes:

- The `avg_rating` field is calculated based on the ratings given by users, so we will get the average rating for each project from project ratings in the `ProjectRate` model.
- `is_reported` is set to `false` by default and is updated to `true` when a user reports a project.
- `is_deleted` is set to `true` when admin reviews and accepts the report, then the project will be hidden from the website.
- If user wants to cancel their project, we will check if the project amount is less than 25% of the target amount, then we will set `is_cancelled` to `true` and the project will be hidden from the website. If the project amount is more than 25% of the target amount, we will not allow the user to cancel their project.
- `is_active` each day we will check the current date and the `campaign_end` date, if the current date is greater than the `campaign_end` date, we will set `is_active` to `false` and the project will be hidden from the website. If the project is cancelled or deleted, we will also set `is_active` to `false`. (**_Idea will be addressed later/see if there is a better way to handle this._**)

<!--
Donation history
Category field PK
Multiple pictures `userid_timestamp_uuid`
Project cancellation by creator (if donations < 25% of target)
 -->

# `ProjectMedia` Model Fields

| Field Name | Field Key   | Nullable | Data Type   | Key               | Default Value |
| ---------- | ----------- | -------- | ----------- | ----------------- | ------------- |
| ID         | `id`        | ❌       | `int`       | PK                |               |
| Project    | `project`   | ❌       | `int`       | FK (`Project.id`) |               |
| Media URL  | `media_url` | ❌       | `varchar`   | ❌                |               |
| Added At   | `added_at`  | ❌       | `timestamp` | ❌                | Timestamp     |

Notes:

- The `media_url` field will store the URL of project images. Images will be saved in a folder named `project_media` in the form of `projectId_timestamp_userId_uuid` to avoid name conflicts. The `timestamp` will be the time when the image was uploaded, and the `userId` will be the ID of the project creator who uploaded the image. The `uuid` is a unique identifier for each image.

# `ProjectCategory` Model Fields

| Field Name | Field Key | Nullable | Data Type | Key | Default Value |
| ---------- | --------- | :------: | --------- | --- | ------------- |
| ID         | `id`      |    ❌    | `int`     | PK  |               |
| Name       | `name`    |    ❌    | `varchar` | ❌  |               |

# `Tag` Model Fields

| Field Name | Field Key | Nullable | Data Type | Key | Default Value |
| ---------- | --------- | :------: | --------- | --- | ------------- |
| ID         | `id`      |    ❌    | `int`     | PK  |               |
| Name       | `name`    |    ❌    | `varchar` | ❌  |               |

# `ProjectTags` Model Fields

| Field Name | Field Key | Nullable | Data Type | Key               | Default Value |
| ---------- | --------- | :------: | --------- | ----------------- | ------------- |
| Project    | `project` |    ❌    | `int`     | FK (`Project.id`) |               |
| Tag        | `tag`     |    ❌    | `int`     | FK (`Tag.id`)     |               |

# `ProjectDonations` Model Fields

| Field Name | Field Key    | Nullable | Data Type   | Key               | Default Value |
| ---------- | ------------ | :------: | ----------- | ----------------- | ------------- |
| ID         | `id`         |    ❌    | `int`       | PK                |               |
| User       | `user`       |    ❌    | `int`       | FK (`User.id`)    |               |
| Project    | `project`    |    ❌    | `int`       | FK (`Project.id`) |               |
| Amount     | `amount`     |    ❌    | `decimal`   | ❌                |               |
| Created_at | `created_at` |    ❌    | `timestamp` | ❌                | Timestamp     |

Notes:

- The `current_amount` field in the `Project` model should be updated each time a user donates to a project.

# `ProjectComments` Model Fields

| Field Name     | Field Key        | Nullable | Data Type   | Key                       | Default Value |
| -------------- | ---------------- | :------: | ----------- | ------------------------- | ------------- |
| ID             | `id`             |    ❌    | `int`       | PK                        |               |
| User           | `user`           |    ❌    | `int`       | FK (`User.id`)            |               |
| Project        | `project`        |    ❌    | `int`       | FK (`Project.id`)         |               |
| Comment        | `comment`        |    ❌    | `text`      | ❌                        |               |
| Parent Comment | `parent_comment` |    ✔️    | `int`       | FK (`ProjectComments.id`) | `NULL`        |
| Created_at     | `created_at`     |    ❌    | `timestamp` | ❌                        | Timestamp     |
| Is Reported    | `is_reported`    |    ❌    | `boolean`   | ❌                        | `false`       |
| Is Deleted     | `is_deleted`     |    ❌    | `boolean`   | ❌                        | `false`       |

Notes about the `ProjectComments` model:

- `is_deleted` is set to `false` by default and when a comment is reported, it is set to `true` and the comment is hidden from the project page when admin reviews and accepts the report.
- Comment replies are handled using the `parent` field in the comment model (something similar to reddit) and the parent of the root comment is `null` by default. (**_Bonus_**)

# `ProjectRate` Model Fields

| Field Name | Field Key    | Nullable | Data Type   | Key               | Default Value |
| ---------- | ------------ | :------: | ----------- | ----------------- | ------------- |
| ID         | `id`         |    ❌    | `int`       | PK                |               |
| User       | `user`       |    ❌    | `int`       | FK (`User.id`)    |               |
| Project    | `project`    |    ❌    | `int`       | FK (`Project.id`) |               |
| Rate       | `rate`       |    ❌    | `int`       | ❌                |               |
| Created_at | `created_at` |    ❌    | `timestamp` | ❌                | Timestamp     |

Notes:

- `avg_rating` field in the `Project` should be updated each time a user rates a project.
- To show top 5 highest-rated running projects in the homepage, we will need sort the projects by `avg_rating` and get the top 5 projects, and it should also be updated each time a user rates a project.

# `ProjectReport` Model Fields

| Field Name | Field Key    | Nullable | Data Type   | Key               | Default Value |
| ---------- | ------------ | :------: | ----------- | ----------------- | ------------- |
| ID         | `id`         |    ❌    | `int`       | PK                |               |
| Reporter   | `reporter`   |    ❌    | `int`       | FK (`User.id`)    |               |
| Project    | `project`    |    ❌    | `int`       | FK (`Project.id`) |               |
| Reason     | `reason`     |    ❌    | `text`      | ❌                |               |
| Created At | `created_at` |    ❌    | `timestamp` | ❌                | Timestamp     |
| Status     | `status`     |    ❌    | `varchar`   | ❌                | `'pending'`   |

Notes:

- Users can report a project for reasons like **scams, misleading information, offensive content, etc.**
- Admins **review reports** and update `status` (`pending`, `reviewed`, `accepted`, `rejected`).
- If the report is **accepted**, the `is_deleted` field in the `Project` model is updated to `true`.

---

# `CommentReport` Model Fields

| Field Name | Field Key    | Nullable | Data Type   | Key                       | Default Value |
| ---------- | ------------ | :------: | ----------- | ------------------------- | ------------- |
| ID         | `id`         |    ❌    | `int`       | PK                        |               |
| Reporter   | `reporter`   |    ❌    | `int`       | FK (`User.id`)            |               |
| Comment    | `comment`    |    ❌    | `int`       | FK (`ProjectComments.id`) |               |
| Reason     | `reason`     |    ❌    | `text`      | ❌                        |               |
| Created At | `created_at` |    ❌    | `timestamp` | ❌                        | Timestamp     |
| Status     | `status`     |    ❌    | `varchar`   | ❌                        | `'pending'`   |

Notes:

- Users can report **comments** for **spam, harassment, inappropriate content, etc.**
- Admins review reports and update `status` (`pending`, `reviewed`, `accepted`, `rejected`).
- If the report is **accepted**, the `is_deleted` field in the `ProjectComments` model is updated to `true`.

---

# `AdminSelectedProjects` Model Fields

| Field Name | Field Key | Nullable | Data Type | Key               | Default Value |
| ---------- | --------- | :------: | --------- | ----------------- | ------------- |
| Project    | `project` |    ❌    | `int`     | FK (`Project.id`) |               |

---

# Links

- [Database diagram on dbdiagram.io](https://dbdiagram.io/d/KaramFund-Database-Schema-67ea50064f7afba184c7b01c)
