import re

from django import forms
from django.contrib.auth import authenticate

from .models import User, NAME_MAX_LENGTH, SURNAME_MAX_LENGTH

PHONE_REGEX = re.compile(r"^(8\d{10}|\+7\d{10})$")
GITHUB_DOMAIN = "github.com"

PASSWORD_LABEL = "Пароль"
EMAIL_LABEL = "Email"
NAME_LABEL = "Имя"
SURNAME_LABEL = "Фамилия"


class RegisterForm(forms.Form):
    name = forms.CharField(label=NAME_LABEL, max_length=NAME_MAX_LENGTH)
    surname = forms.CharField(label=SURNAME_LABEL, max_length=SURNAME_MAX_LENGTH)
    email = forms.EmailField(label=EMAIL_LABEL)
    password = forms.CharField(label=PASSWORD_LABEL, widget=forms.PasswordInput)

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Пользователь с таким email уже существует.")
        return email


class LoginForm(forms.Form):
    email = forms.EmailField(label=EMAIL_LABEL)
    password = forms.CharField(label=PASSWORD_LABEL, widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._user = None

    def clean(self):
        cleaned = super().clean()
        email = cleaned.get("email")
        password = cleaned.get("password")
        if email and password:
            user = authenticate(username=email, password=password)
            if user is None:
                raise forms.ValidationError("Неверный email или пароль")
            self._user = user
        return cleaned

    def get_user(self):
        return self._user


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["name", "surname", "avatar", "about", "phone", "github_url"]
        labels = {
            "name": NAME_LABEL,
            "surname": SURNAME_LABEL,
            "avatar": "Аватар",
            "about": "О себе",
            "phone": "Телефон",
            "github_url": "Ссылка на GitHub",
        }
        widgets = {
            "avatar": forms.FileInput(attrs={"id": "id_avatar"}),
        }

    def __init__(self, *args, **kwargs):
        self._current_user = kwargs.pop("current_user", None)
        super().__init__(*args, **kwargs)

    def clean_phone(self):
        phone = self.cleaned_data.get("phone", "").strip()
        if not phone:
            return phone
        if not PHONE_REGEX.match(phone):
            raise forms.ValidationError(
                "Введите телефон в формате 8XXXXXXXXXX или +7XXXXXXXXXX."
            )
        normalized = "+7" + phone[-10:]
        qs = User.objects.filter(phone__in=[normalized, "8" + phone[-10:]])
        if self._current_user:
            qs = qs.exclude(pk=self._current_user.pk)
        if qs.exists():
            raise forms.ValidationError("Этот номер телефона уже используется.")
        return normalized

    def clean_github_url(self):
        url = self.cleaned_data.get("github_url", "").strip()
        if url and GITHUB_DOMAIN not in url:
            raise forms.ValidationError("Ссылка должна вести на github.com.")
        return url


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(label="Текущий пароль", widget=forms.PasswordInput)
    new_password1 = forms.CharField(label="Новый пароль", widget=forms.PasswordInput)
    new_password2 = forms.CharField(label="Подтвердите новый пароль", widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        self._user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

    def clean_old_password(self):
        old = self.cleaned_data["old_password"]
        if self._user and not self._user.check_password(old):
            raise forms.ValidationError("Неверный текущий пароль.")
        return old

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get("new_password1")
        p2 = cleaned.get("new_password2")
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("Пароли не совпадают.")
        return cleaned
