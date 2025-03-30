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
    -   Mobile phone (validated for Egyptian numbers)
    -   Profile Picture
-   Activation email after registration
    -   Email contains activation link
    -   Link expires after 24 hours
    -   Users cannot login without activation

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
-   Account deletion
    -   Confirmation message before deletion
    -   Password confirmation for account deletion (Bonus)

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
    -   Nested comments/replies (Bonus)
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

-   Deadline: May 16, 2019

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
