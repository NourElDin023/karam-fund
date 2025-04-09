from django.contrib import admin
from admin_dashboard.models import AdminSelectedprojects
from donations.models import ProjectDonations
from interactions.models import ProjectComments, ProjectRatings
from projects.models import (
    Project,
    ProjectCategory,
    Tag,
    ProjectTags,
    projectMedia,
)
from reports.models import ProjectReport, CommentReport
from users.models import User

# User model
admin.site.register(User)

# Projects-related models
admin.site.register(Project)
admin.site.register(ProjectCategory)
admin.site.register(Tag)
admin.site.register(ProjectTags)
admin.site.register(projectMedia)

# Interactions-related models
admin.site.register(ProjectComments)
admin.site.register(ProjectRatings)

# Donations-related models
admin.site.register(ProjectDonations)

# Reports-related models
admin.site.register(ProjectReport)
admin.site.register(CommentReport)

# Admin dashboard-related models
admin.site.register(AdminSelectedprojects)
