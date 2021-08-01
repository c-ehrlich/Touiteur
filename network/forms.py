from django import forms
from django.core.files.images import get_image_dimensions

from django.utils.translation import ugettext as _
from django.utils.translation import ugettext_lazy as _lazy

from network.models import Post, User


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

    class Meta:
        model = User
        fields = ['username', 'displayname', 'bio', 'email', 'avatar']


class NewPostForm(forms.Form):
    text = forms.CharField(
        # label = "New Post",
        max_length = 140,
        required = True,
        widget = forms.Textarea(attrs={
            'rows':4,
            'class': 'form-control',
            'id': 'compose-form-post-text',
            'placeholder': "What's Happening?"
        })
    )
    # image = forms.ImageField(
    #     required = False,
    #     widget = forms.FileInput(attrs={
    #         'class': 'form-control',
    #         'id': 'compose-form-image',
    #     })
    # )

    class Meta:
        model = Post
        fields = ['text', 'image']


class RegisterAccountForm(forms.Form):
    username = forms.CharField(
        label = "Username",
        max_length = 20,
        required = True,
        widget=forms.TextInput(attrs={
            'placeholder': _('Up to 20 characters, alphanumeric'),
            'class': 'form-control reg-login-form-item form-control-left-padding-for-at-sign',
            'autofocus': True,
        })
    )
    displayname = forms.CharField(
        label = "Display Name",
        max_length = 50,
        required = True,
        widget=forms.TextInput(attrs={
            'placeholder': _('Up to 50 characters'),
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
        fields = ['bio', 'avatar',]

class RegisterAccountStage3Form(forms.ModelForm):
    # Display settings
    theme = forms.CharField(
        label = "Theme",
        required = True,
        # default = "_theme_light",
        widget = forms.Select(
            choices = User.THEMES,
            # attrs = {
            #     'class': 'form-control',
            # }
        )
    )
    language = forms.CharField(
        label = "Language",
        required = True,
        # default = "en_US",
        widget = forms.Select(
            choices = User.LANGUAGES,
            # attrs = {
            #     'class': 'form-control',
            # }
        )
    )

    show_liked_posts = forms.BooleanField(
        label = "Show Liked Posts",
        help_text = "Decide whether other users can see which posts you have liked.",
        required = False,
        # default = True,
        widget = forms.CheckboxInput(attrs={
            'class': 'form-control form-checkbox',
        })
    )

    class Meta:
        model = User
        fields = ['theme', 'language', 'show_liked_posts',]
