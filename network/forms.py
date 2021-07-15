from django import forms
from django.core.files.images import get_image_dimensions

from network.models import User


class EditAccountForm(forms.ModelForm):
    password = forms.CharField(
        required = True,
        # Label = "Current Password",
        widget = forms.PasswordInput(attrs={
            'class': 'form-control',
        }))
    username = forms.CharField(
        required=False,
        widget = forms.TextInput(attrs={
            'class': 'form-control form-control-left-padding-for-at-sign',
        }))
    displayname = forms.CharField(
        required=False,
        widget = forms.TextInput(attrs={
            'class': 'form-control',
        }))
    email = forms.EmailField(
        required=False,
        widget = forms.EmailInput(attrs={
            'class': 'form-control',
        }))
    bio = forms.CharField(
        required=False,
        widget = forms.Textarea(attrs={
            'rows': 3,
            'class': 'form-control',
        }))
    new_password = forms.CharField(
        required=False,
        # Label = "New Password",
        widget = forms.PasswordInput(attrs={
            'class': 'form-control',
        }))
    new_password_confirm = forms.CharField(
        required=False,
        # Label = "Confirm New Password",
        widget = forms.PasswordInput(attrs={
            'class': 'form-control',
        }))

    # password = forms.CharField(
    #     label = "New Password",
    #     required = False,
    #     widget = forms.PasswordInput(attrs={
    #         'class': 'form-control'
    #     }))
    # confirmation = forms.CharField(
    #     label = "Confirm New Password",
    #     required = False,
    #     widget = forms.PasswordInput(attrs={
    #         'class': 'form-control'
    #     }))

    # avatar = forms.ImageField(
    #     label = "Avatar",
    #     required = False,
    #     widget = forms.FileInput(attrs={
    #         'class': 'form-control'
    #     }))
    
    class Meta:
        model = User
        fields = ['username', 'displayname', 'bio', 'email', 'avatar']


class NewPostForm(forms.Form):
    post_text = forms.CharField(
        # label = "New Post",
        max_length = 500,
        required = True,
        widget = forms.Textarea(attrs={
            'rows':3,
            'class': 'form-control',
            'id': 'compose-form-post-text',
            'placeholder': "What's Happening?"
        })
    )


class RegisterAccountForm(forms.Form):
    username = forms.CharField(
        label = "Username",
        max_length = 20,
        required = True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Up to 20 characters, alphanumeric',
            'class': 'form-control reg-login-form-item form-control-left-padding-for-at-sign',
            'autofocus': True,
        })
    )
    displayname = forms.CharField(
        label = "Display Name",
        max_length = 50,
        required = True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Up to 50 characters',
            'class': 'form-control reg-login-form-item',
        })
    )
    email = forms.EmailField(
        label = "Email",
        required = True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control reg-login-form-item',
        })
    )
    password = forms.CharField(
        label = "Password",
        required = True,
        widget = forms.PasswordInput(attrs={
            'class': 'form-control reg-login-form-item',
        })
    )
    confirmation = forms.CharField(
        label = "Confirm Password",
        required = True,
        widget = forms.PasswordInput(attrs={
            'class': 'form-control reg-login-form-item',
        })
    )


class RegisterAccountStage2Form(forms.ModelForm):
    username = forms.CharField(
        required=False,
        widget = forms.TextInput(attrs={
            'class': 'form-control form-control-left-padding-for-at-sign',
        }))

    avatar = forms.ImageField(
        label = "Avatar",
        required = False,
        widget = forms.FileInput(attrs={
            'class': 'form-control',
        })
    )
    bio = forms.CharField(
        label = "Bio",
        required = False,
        widget = forms.Textarea(attrs={
            'rows': 3,
            'class': 'form-control',
        })
    )
    class Meta:
        model = User
        fields = ['username', 'email', 'bio', 'avatar']
        # exclude = ['displayname', 'email', 'password', 'confirmation']
