from django import forms

GITHUB_DOMAIN = "github.com"


class GithubUrlMixin:
    def clean_github_url(self):
        url = self.cleaned_data.get("github_url", "").strip()
        if url and GITHUB_DOMAIN not in url:
            raise forms.ValidationError("Ссылка должна вести на github.com.")
        return url
