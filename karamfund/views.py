from django.shortcuts import render
from projects.models import Project, ProjectCategory
from admin_dashboard.models import AdminSelectedprojects
from django.db.models import Q

def home(request):
    # Fetch the top 5 highest-rated active projects
    highest_rated_projects = Project.objects.filter(is_active=True).order_by('-avg_rating')[:5]

    # Fetch the latest 5 projects
    latest_projects = Project.objects.filter(is_active=True).order_by('-campaign_start')[:5]

    # Fetch the latest 5 featured projects
    featured_projects = AdminSelectedprojects.objects.select_related('project').order_by('-id')[:5]

    # Fetch all categories
    categories = ProjectCategory.objects.all()

    # Search functionality
    query = request.GET.get('q', '')
    search_results = None
    if query:
        search_results = Project.objects.filter(
            Q(title__icontains=query) | Q(tags__name__icontains=query),
            is_active=True
        ).distinct()

    context = {
        'highest_rated_projects': highest_rated_projects,
        'latest_projects': latest_projects,
        'featured_projects': featured_projects,
        'categories': categories,
        'search_results': search_results,
        'query': query,
    }

    return render(request, 'home.html', context)