import os
import django
import random
from decimal import Decimal
from datetime import datetime, timedelta
from django.utils import timezone

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'karamfund.settings')
django.setup()

# Import models after Django setup
from django.contrib.auth import get_user_model
from projects.models import Project, ProjectCategory, Tag, ProjectTags, projectMedia
from donations.models import ProjectDonations
from interactions.models import ProjectComments, ProjectRatings
from reports.models import ProjectReport, CommentReport
from admin_dashboard.models import AdminSelectedprojects

User = get_user_model()

print("Creating dummy data for Karam Fund...")

# Clean existing data - this will ensure we don't get unique constraint violations
print("Cleaning existing data...")
# Clean up in reverse order of dependencies
AdminSelectedprojects.objects.all().delete()
CommentReport.objects.all().delete()
ProjectReport.objects.all().delete()
ProjectRatings.objects.all().delete()
ProjectComments.objects.all().delete()
ProjectDonations.objects.all().delete()
ProjectTags.objects.all().delete()
projectMedia.objects.all().delete()
Project.objects.all().delete()
Tag.objects.all().delete()
ProjectCategory.objects.all().delete()
# Don't delete the superuser - this could delete your main admin account
User.objects.filter(is_superuser=False).delete()
print("Existing data cleaned")

# 1. Create Users
users = []
print("Creating users...")
for i in range(1, 11):
    user = User.objects.create_user(
        username=f"user{i}@example.com",
        email=f"user{i}@example.com",
        password="password123",
        first_name=f"FirstName{i}",
        last_name=f"LastName{i}"
    )
    users.append(user)

# Get existing admin or create one if necessary
try:
    admin_user = User.objects.get(username="admin")
except User.DoesNotExist:
    admin_user = User.objects.create_superuser(
        username="admin",
        email="admin@example.com",
        password="admin123",
        first_name="Admin",
        last_name="User"
    )
users.append(admin_user)
print(f"Created {len(users)} users")

# 2. Create Project Categories
categories = []
print("Creating project categories...")
category_names = [
    "Education", "Healthcare", "Environment", 
    "Community Development", "Arts & Culture", 
    "Disaster Relief", "Technology", "Animal Welfare",
    "Sports", "Human Rights"
]

for name in category_names:
    category = ProjectCategory.objects.create(
        name=name,
        description=f"Projects related to {name.lower()}"
    )
    categories.append(category)
print(f"Created {len(categories)} project categories")

# 3. Create Tags
tags = []
print("Creating tags...")
tag_names = [
    "Urgent", "Featured", "Innovative", 
    "Sustainable", "Low-cost", "Global", 
    "Local", "Youth", "Women", "Elderly"
]

for name in tag_names:
    tag = Tag.objects.create(name=name)
    tags.append(tag)
print(f"Created {len(tags)} tags")

# 4. Create Projects
projects = []
print("Creating projects...")
project_titles = [
    "Clean Water Initiative", 
    "Digital Literacy Program",
    "Community Garden Project",
    "Healthcare for All",
    "Education for Underprivileged Children",
    "Renewable Energy Solutions",
    "Elderly Care Program",
    "Shelter for Homeless",
    "Wildlife Conservation",
    "Art Therapy Workshop"
]

project_descriptions = [
    "Providing clean water access to rural communities.",
    "Teaching digital skills to disadvantaged youth.",
    "Creating sustainable community gardens in urban areas.",
    "Making healthcare accessible to underserved populations.",
    "Providing quality education to children in need.",
    "Implementing renewable energy solutions in remote areas.",
    "Supporting elderly with daily care needs.",
    "Building shelter for homeless individuals.",
    "Protecting endangered wildlife species.",
    "Using art as therapy for trauma survivors."
]

now = timezone.now()

for i in range(10):
    campaign_end = now.date() + timedelta(days=random.randint(30, 180))
    target_amount = Decimal(random.randint(5000, 50000))
    current_amount = Decimal(random.randint(0, int(target_amount))) if random.random() > 0.3 else Decimal('0.00')
    
    project = Project.objects.create(
        title=project_titles[i],
        description=project_descriptions[i],
        target_amount=target_amount,
        current_amount=current_amount,
        category=random.choice(categories),
        creator=random.choice(users),
        campaign_end=campaign_end,
        is_active=random.random() > 0.2,
        avg_rating=Decimal(random.randint(0, 5)),
        is_reported=random.random() > 0.8,
        is_deleted=False,
        is_cancelled=random.random() > 0.9
    )
    projects.append(project)
print(f"Created {len(projects)} projects")

# 5. Create Project Media
print("Creating project media...")
media_count = 0
for project in projects:
    # Create 1-3 media items per project
    for _ in range(random.randint(1, 3)):
        media_type = random.choice(['image', 'video'])
        
        if media_type == 'image':
            projectMedia.objects.create(
                project=project,
                image=f"project_media/images/dummy_image_{random.randint(1, 5)}.jpg",
                media_type='image'
            )
        else:
            projectMedia.objects.create(
                project=project,
                video_url=f"https://www.youtube.com/watch?v=example{random.randint(1, 999)}",
                media_type='video'
            )
        media_count += 1
print(f"Created {media_count} media items")

# 6. Create Project Tags
print("Creating project tags...")
tags_count = 0
for project in projects:
    # Assign 2-4 random tags to each project
    selected_tags = random.sample(tags, random.randint(2, 4))
    for tag in selected_tags:
        ProjectTags.objects.create(
            project=project,
            tag=tag
        )
        tags_count += 1
print(f"Created {tags_count} project tags")

# 7. Create Donations
print("Creating donations...")
donations_count = 0
for _ in range(10):
    # Pick random projects that aren't cancelled or deleted
    valid_projects = [p for p in projects if not p.is_cancelled and not p.is_deleted]
    if valid_projects:
        project = random.choice(valid_projects)
        user = random.choice(users)
        
        # Avoid donating to your own project
        while user == project.creator:
            user = random.choice(users)
            
        amount = Decimal(random.randint(10, 500))
        
        ProjectDonations.objects.create(
            user=user,
            project=project,
            amount=amount
        )
        donations_count += 1
print(f"Created {donations_count} donations")

# 8. Create Comments
print("Creating comments...")
comments = []
for _ in range(10):
    project = random.choice(projects)
    user = random.choice(users)
    
    # Create root comments
    comment = ProjectComments.objects.create(
        user=user,
        project=project,
        comment_text=f"This is a comment about {project.title}. {'I love this idea!' if random.random() > 0.5 else 'I have some concerns...'}"
    )
    comments.append(comment)

# Create some replies
replies_count = 0
for _ in range(5):
    if comments:
        parent_comment = random.choice(comments)
        user = random.choice(users)
        
        reply = ProjectComments.objects.create(
            user=user,
            project=parent_comment.project,
            comment_text=f"Reply to comment {parent_comment.ID}: {'Good point!' if random.random() > 0.5 else 'I disagree because...'}", 
            parent_comment=parent_comment
        )
        replies_count += 1

print(f"Created {len(comments)} comments and {replies_count} replies")

# 9. Create Ratings
print("Creating ratings...")
ratings_count = 0
for _ in range(10):
    project = random.choice(projects)
    user = random.choice(users)
    
    # Avoid rating your own project
    while user == project.creator:
        user = random.choice(users)
        
    # Random rating between 1-5
    rating = random.randint(1, 5)
    
    ProjectRatings.objects.create(
        user=user,
        project=project,
        rate=rating
    )
    ratings_count += 1
print(f"Created {ratings_count} ratings")

# 10. Create Reports
print("Creating reports...")
project_reports_count = 0
comment_reports_count = 0

# Project reports
for _ in range(5):
    project = random.choice(projects)
    user = random.choice(users)
    
    # Avoid reporting your own project
    while user == project.creator:
        user = random.choice(users)
        
    reason = random.choice(['scam', 'misleading', 'offensive', 'other'])
    
    ProjectReport.objects.create(
        reporter=user,
        project=project,
        reason=reason
    )
    project_reports_count += 1

# Comment reports
if comments:
    for _ in range(5):
        comment = random.choice(comments)
        user = random.choice(users)
        
        # Avoid reporting your own comment
        while user == comment.user:
            user = random.choice(users)
            
        reason = random.choice(['spam', 'harassment', 'inappropriate', 'other'])
        
        CommentReport.objects.create(
            reporter=user,
            comment=comment,
            reason=reason
        )
        comment_reports_count += 1

print(f"Created {project_reports_count} project reports and {comment_reports_count} comment reports")

# 11. Create Admin Selected Projects
print("Creating admin selected projects...")
selected_count = 0
# Select 3 random projects to feature
for project in random.sample(projects, 3):
    AdminSelectedprojects.objects.create(
        project=project
    )
    selected_count += 1
print(f"Created {selected_count} admin selected projects")

print("\nDummy data creation complete!")
print("---------------------------------------")
print("Summary:")
print(f"- {len(users)} users")
print(f"- {len(categories)} project categories")
print(f"- {len(tags)} tags")
print(f"- {len(projects)} projects")
print(f"- {media_count} media items")
print(f"- {tags_count} project tags")
print(f"- {donations_count} donations")
print(f"- {len(comments)} comments and {replies_count} replies")
print(f"- {ratings_count} ratings")
print(f"- {project_reports_count} project reports")
print(f"- {comment_reports_count} comment reports")
print(f"- {selected_count} admin selected projects")