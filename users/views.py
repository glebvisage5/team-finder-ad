from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect

from projects.constants import USERS_PER_PAGE
from projects.utils import paginate
from .constants import (
    FILTER_OWNERS_OF_FAVORITES,
    FILTER_OWNERS_OF_PARTICIPATING,
    FILTER_INTERESTED_IN_MINE,
    FILTER_PARTICIPANTS_OF_MINE,
)
from .forms import ChangePasswordForm, EditProfileForm, LoginForm, RegisterForm
from .models import User


def register(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        user = User.objects.create_user(
            email=form.cleaned_data["email"],
            name=form.cleaned_data["name"],
            surname=form.cleaned_data["surname"],
            password=form.cleaned_data["password"],
        )
        login(request, user)
        return redirect("projects:project_list")
    return render(request, "users/register.html", {"form": form})


def login_view(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        login(request, form.get_user())
        return redirect("projects:project_list")
    return render(request, "users/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("projects:project_list")


def users_list(request):
    queryset = User.objects.order_by("-id")
    active_filter = None

    if request.user.is_authenticated:
        active_filter = request.GET.get("filter")
        if active_filter == FILTER_OWNERS_OF_FAVORITES:
            queryset = User.objects.filter(
                owned_projects__in=request.user.favorites.all()
            ).distinct().order_by("-id")
        elif active_filter == FILTER_OWNERS_OF_PARTICIPATING:
            queryset = User.objects.filter(
                owned_projects__in=request.user.participated_projects.all()
            ).distinct().order_by("-id")
        elif active_filter == FILTER_INTERESTED_IN_MINE:
            queryset = User.objects.filter(
                favorites__in=request.user.owned_projects.all()
            ).distinct().order_by("-id")
        elif active_filter == FILTER_PARTICIPANTS_OF_MINE:
            queryset = User.objects.filter(
                participated_projects__in=request.user.owned_projects.all()
            ).distinct().order_by("-id")
        else:
            active_filter = None

    query_prefix = f"filter={active_filter}&" if active_filter else ""
    page_obj = paginate(queryset, USERS_PER_PAGE, request)

    return render(request, "users/participants.html", {
        "participants": queryset,
        "page_obj": page_obj,
        "active_filter": active_filter,
        "query_prefix": query_prefix,
    })


def user_detail(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    return render(request, "users/user-details.html", {"user": user})


@login_required
def edit_profile(request):
    user = request.user
    form = EditProfileForm(
        request.POST or None,
        request.FILES or None,
        instance=user,
        current_user=user,
    )
    if form.is_valid():
        form.save()
        return redirect("users:user_detail", user.pk)
    return render(request, "users/edit_profile.html", {"form": form})


@login_required
def change_password(request):
    user = request.user
    form = ChangePasswordForm(request.POST or None, user=user)
    if form.is_valid():
        user.set_password(form.cleaned_data["new_password1"])
        user.save()
        update_session_auth_hash(request, user)
        return redirect("users:user_detail", user.pk)
    return render(request, "users/change_password.html", {"form": form})
