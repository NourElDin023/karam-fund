# Karam Fund - Crowdfunding Web App

## Project Overview

Karam Fund is a web platform for starting fundraising projects in Egypt. The platform allows users to create fundraising campaigns, donate to projects, and interact with the community through comments and ratings.

## Core Features

### 1. Authentication System

#### Registration

-   User information to collect:
    -   First name
    -   Last name
    -   Email
    -   Password
    -   Confirm password
    -   Phone number (validated for Egyptian numbers)
    -   Profile Picture
-   Activation email after registration
    -    Email contains activation link (is_activated)
    -    Link expires after 24 hours
    -    Users cannot login without activation

We have added the following fields to `User` model:


-   Bio
-   Email activated
-   Birthdate
-   Facebook profile
-   Country


#### Login

-   Users can login with email and password after activation
-   Social login with Facebook (Bonus)

#### Password Reset (Bonus)

-   Forgot password functionality (Bonus)
    -   Sends password reset link to user's email

#### User Profile

-   View profile information
-   View created projects
-   View donations history
-   Edit profile data (except email)
-   Additional optional information:
    -   Birthdate
    -   Facebook profile
    -   Country
-   Account deletion (Disabled for admin users)
    -   Confirmation message before deletion (Only in frontend)
    -   Password confirmation for account deletion (Bonus - Add password field to the request body)
    -   When a user deletes their account, all their projects and donations are moved to a dummy user `deleted_user` then the user entry is deleted from the database. This is to keep the integrity of the database and avoid orphaned records.

### 2. Projects

#### Project Creation

-   Project details:
    -   Title
    -   Details/Description
    -   Category (from admin-defined list)
    -   Multiple pictures
    -   Total target amount (e.g., 250,000 EGP)
    -   Multiple tags
    -   Start/end dates for the campaign

#### Project Interaction

-   View projects and donate
-   Comment on projects
    -   Nested comments/replies (Bonus - Handled with `parent` field in the comment model (something similar to reddit) and the parent of the root comment is `null`)
-   Report inappropriate projects
-   Report inappropriate comments
-   Rate projects
-   Project cancellation by creator (if donations < 25% of target)

#### Project Display Page

-   Show overall average rating
-   Display project pictures in a slider
-   Show 4 similar projects based on tags

### 3. Homepage

-   Slider showing top 5 highest-rated running projects
-   List of latest 5 projects
-   List of latest 5 featured projects (admin-selected)
-   Categories list with ability to view projects by category
-   Search functionality for projects by title or tag

## Inspiration

Similar projects for reference:

-   [GoFundMe](https://www.gofundme.com)
-   [Kickstarter](https://www.kickstarter.com)
-   [Crowdfunding.com](https://www.crowdfunding.com)

## Project Timeline

-   Deadline: April 11, 2025

## Project Structure

1. User Authentication App
2. Projects App
3. Homepage/Main App
4. Admin Dashboard

## Tech Stack

-   Backend: Django
-   Database: PostgreSQL
-   Frontend: HTML, CSS, JavaScript
-   Additional libraries as needed
