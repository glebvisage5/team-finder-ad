from django import forms

from team_finder.mixins import GithubUrlMixin
from .constants import STATUS_DISPLAY_CHOICES
from .models import Project


class ProjectForm(GithubUrlMixin, forms.ModelForm):
    status = forms.ChoiceField(
        choices=STATUS_DISPLAY_CHOICES,
        label="Статус",
    )

    class Meta:
        model = Project
        fields = ["name", "description", "github_url", "status"]
        labels = {
            "name": "Название",
            "description": "Описание",
            "github_url": "Ссылка на GitHub",
        }
        widgets = {
            "description": forms.Textarea(attrs={"rows": 5}),
        }
