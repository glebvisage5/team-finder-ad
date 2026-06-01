from django import forms

from .models import Project, STATUS_OPEN, STATUS_CLOSED

GITHUB_DOMAIN = "github.com"

STATUS_DISPLAY_CHOICES = [
    (STATUS_OPEN, "Открыт"),
    (STATUS_CLOSED, "Закрыт"),
]


class ProjectForm(forms.ModelForm):
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

    def clean_github_url(self):
        url = self.cleaned_data.get("github_url", "").strip()
        if url and GITHUB_DOMAIN not in url:
            raise forms.ValidationError("Ссылка должна вести на github.com.")
        return url
