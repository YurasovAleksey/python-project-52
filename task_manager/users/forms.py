from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.utils.translation import gettext_lazy as _
from .models import User


class UserRegisterForm(UserCreationForm):
    password1 = forms.CharField(
        required=True,
        label='Пароль',
        widget=forms.PasswordInput,
        help_text='Ваш пароль должен содержать как минимум 3 символа.'
    )
    password2 = forms.CharField(
        required=True,
        label='Подтверждение пароля',
        widget=forms.PasswordInput,
        help_text='Для подтверждения введите, пожалуйста, пароль ещё раз.'
    )
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'password1',
            'password2',
        ]
        labels = {
            'first_name': _('Имя'),
            'last_name': _('Фамилия'),
            'username': _('Имя пользователя'),
            'password1': _('Пароль'),
            'password2': _('Подтверждение пароля'),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
            
        self.fields['username'].help_text = _(
            'Обязательное поле. Не более 150 символов. Только буквы, цифры и @/./+/-/_.'
        )
            
        self.fields['password1'].help_text = _(
            '• Ваш пароль должен содержать как минимум 3 символа.'
        )


class UserUpdateForm(UserRegisterForm):
    password = None

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
        ]
        labels = {
            'first_name': _('Имя'),
            'last_name': _('Фамилия'),
            'username': _('Имя пользователя'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].validators = []

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username:
            existing_user = User.objects.filter(username=username).first()
            if existing_user and existing_user.pk != self.instance.pk:
                raise forms.ValidationError('Пользователь с таким именем пользователя уже существует')
        return username

class CustomUserLoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Имя пользователя',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
