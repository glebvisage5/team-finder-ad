from http import HTTPStatus

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse

from .forms import ProjectForm
from .models import Project, STATUS_OPEN, STATUS_CLOSED
from .utils import paginate, PROJECTS_PER_PAGE


def project_list(request):
    projects = Project.objects.select_related("owner").prefetch_related("participants")
    query_prefix = ""
    page_obj = paginate(projects, PROJECTS_PER_PAGE, request)

    return render(request, "projects/project_list.html", {
        "projects": projects,
        "page_obj": page_obj,
        "query_prefix": query_prefix,
    })


def project_detail(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    return render(request, "projects/project-details.html", {"project": project})


@login_required
def favorites(request):
    projects = request.user.favorites.select_related("owner").prefetch_related("participants")
    return render(request, "projects/favorite_projects.html", {"projects": projects})


@login_required
def create_project(request):
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user
            project.save()
            project.participants.add(request.user)
            return redirect(reverse("projects:project_detail", kwargs={"project_id": project.pk}))
    else:
        form = ProjectForm()
    return render(request, "projects/create-project.html", {"form": form, "is_edit": False})


@login_required
def edit_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id, owner=request.user)
    if request.method == "POST":
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect(reverse("projects:project_detail", kwargs={"project_id": project.pk}))
    else:
        form = ProjectForm(instance=project)
    return render(request, "projects/create-project.html", {"form": form, "is_edit": True})


@login_required
def toggle_favorite(request, project_id):
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=HTTPStatus.METHOD_NOT_ALLOWED)

    project = Project.objects.filter(pk=project_id).first()
    if project is None:
        return JsonResponse({"error": "Проект не найден"}, status=HTTPStatus.NOT_FOUND)

    is_favorited = request.user.favorites.filter(pk=project_id).exists()
    if is_favorited:
        request.user.favorites.remove(project)
    else:
        request.user.favorites.add(project)

    return JsonResponse({"status": "ok", "favorited": not is_favorited})


@login_required
def toggle_participate(request, project_id):
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=HTTPStatus.METHOD_NOT_ALLOWED)

    project = Project.objects.filter(pk=project_id).first()
    if project is None:
        return JsonResponse({"error": "Проект не найден"}, status=HTTPStatus.NOT_FOUND)

    is_participant = project.participants.filter(pk=request.user.pk).exists()
    if is_participant:
        project.participants.remove(request.user)
    else:
        project.participants.add(request.user)

    return JsonResponse({"status": "ok", "participant": not is_participant})


@login_required
def complete_project(request, project_id):
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=HTTPStatus.METHOD_NOT_ALLOWED)

    project = Project.objects.filter(pk=project_id).first()
    if project is None:
        return JsonResponse({"error": "Проект не найден"}, status=HTTPStatus.NOT_FOUND)

    if project.owner_id != request.user.pk:
        return JsonResponse({"error": "Нет доступа"}, status=HTTPStatus.FORBIDDEN)

    if project.status != STATUS_OPEN:
        return JsonResponse({"error": "Проект уже завершён"}, status=HTTPStatus.BAD_REQUEST)

    project.status = STATUS_CLOSED
    project.save(update_fields=["status"])

    return JsonResponse({"status": "ok", "project_status": STATUS_CLOSED})
