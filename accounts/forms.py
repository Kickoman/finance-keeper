from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


class SigninForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'USERNAME',
            },
        ),
        max_length=25
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'PASSWORD',
            },
            render_value=True
        )
    )


class SignupForm(forms.Form):
    username = forms.CharField(
        label='Username',
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
        ),
        max_length=25
    )

    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(
            attrs={'class': 'form-control'},
            render_value=True
        )
    )

    # password confirmation
    password_conf = forms.CharField(
        label='Confirm password',
        widget=forms.PasswordInput(
            attrs={'class': 'form-control'},
            render_value=True
        )
    )

    @staticmethod
    def check_username(username):
        return User.objects.filter(username=username).exists()


    def clean(self):
        cd = self.cleaned_data

        password1 = cd.get('password')
        password2 = cd.get('password_conf')

        if password1 != password2:
            raise ValidationError("Passwords didn't match")

        if self.check_username(cd.get('username')):
            raise ValidationError('This username is already taken')

        return cd