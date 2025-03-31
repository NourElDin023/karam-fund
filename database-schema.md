# KaramFund Database Schema

## Tables Overview

### Users Table
Stores user information including authentication credentials.

- `id`: Primary Key
- `username`: Unique username
- `email`: Unique email
- `password`: Hashed password

### Projects Table
Contains details about crowdfunding projects.

- `id`: Primary Key
- `owner_id`: Foreign Key referencing `Users`
- `title`: Project title
- `description`: Project description
- `goal_amount`: Target funding amount
- `start_date`: Campaign start date
- `end_date`: Campaign end date

### Donations Table
Tracks user contributions to projects.

- `id`: Primary Key
- `user_id`: Foreign Key referencing `Users`
- `project_id`: Foreign Key referencing `Projects`
- `amount`: Donated amount

### Categories Table
Defines categories for classifying projects.

- `id`: Primary Key
- `name`: Category name
- `description`: Category description

### Comments Table
Stores user comments on projects.

- `id`: Primary Key
- `user_id`: Foreign Key referencing `Users`
- `project_id`: Foreign Key referencing `Projects`
- `text`: Comment content
- `created_at`: Timestamp

### Ratings Table
Allows users to rate projects.

- `id`: Primary Key
- `user_id`: Foreign Key referencing `Users`
- `project_id`: Foreign Key referencing `Projects`
- `rating`: Numeric rating value

### Reports Table
Handles user reports on projects.

- `id`: Primary Key
- `user_id`: Foreign Key referencing `Users`
- `project_id`: Foreign Key referencing `Projects`
- `reason`: Report reason
- `created_at`: Timestamp

### Media Table
Stores images or videos related to projects.

- `id`: Primary Key
- `project_id`: Foreign Key referencing `Projects`
- `image_url`: Media file path

## Notes
- All foreign keys enforce cascading deletes.
- Timestamps (`created_at`, `updated_at`) should be auto-generated.
- Indexes should be created for frequently queried columns.

