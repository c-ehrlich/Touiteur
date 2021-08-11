from django import forms
from django.core.files.images import get_image_dimensions

from django.utils.translation import gettext_lazy as _

from network.models import Post, User


class EditAccountForm(forms.ModelForm):
    password = forms.CharField(
        label = _("Current Password (required)"),
        required = True,
        # Label = "Current Password",
        widget = forms.PasswordInput(attrs={
            'class': 'form-control',
        }))
    username = forms.CharField(
        label = _("New Username"),
        required=False,
        widget = forms.TextInput(attrs={
            'class': 'form-control form-control-left-padding-for-at-sign',
        }))
    displayname = forms.CharField(
        label = _("New Display Name"),
        required=False,
        widget = forms.TextInput(attrs={
            'class': 'form-control',
        }))
    email = forms.EmailField(
        label = _("New Email"),
        required=False,
        widget = forms.EmailInput(attrs={
            'class': 'form-control',
        }))
    bio = forms.CharField(
        label = _("New Bio"),
        required=False,
        widget = forms.Textarea(attrs={
            'rows': 3,
            'class': 'form-control',
        }))
    new_password = forms.CharField(
        label = _("New Password"),
        required=False,
        # Label = "New Password",
        widget = forms.PasswordInput(attrs={
            'class': 'form-control',
        }))
    new_password_confirm = forms.CharField(
        label = _("Confirm New Password"),
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
        max_length = 140,
        required = True,
        widget = forms.Textarea(attrs={
            'rows':4,
            'class': 'form-control',
            'id': 'compose-form-post-text',
            'placeholder': _("What's Happening?"),
        })
    )
    image = forms.ImageField(
        label = "post_image", #DON'T TRANSLATE THIS - IT'S NOT VISIBLE ON THE PAGE AND REQUIRED FOR A DUMB HACK
        required = False,
        widget = forms.FileInput(attrs={
            'class': 'form-control',
            'id': 'compose-form-image',
        })
    )

    class Meta:
        model = Post
        fields = ['text', 'image']


class RegisterAccountForm(forms.Form):
    username = forms.CharField(
        label = _("Username"),
        max_length = 20,
        required = True,
        widget=forms.TextInput(attrs={
            'placeholder': _('Up to 20 characters, alphanumeric'),
            'class': 'form-control reg-login-form-item form-control-left-padding-for-at-sign',
            'autofocus': True,
        })
    )
    displayname = forms.CharField(
        label = _("Display Name"),
        max_length = 50,
        required = True,
        widget=forms.TextInput(attrs={
            'placeholder': _('Up to 50 characters'),
            'class': 'form-control reg-login-form-item',
        })
    )
    email = forms.EmailField(
        label = _("Email"),
        required = True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control reg-login-form-item',
        })
    )
    password = forms.CharField(
        label = _("Password"),
        required = True,
        widget = forms.PasswordInput(attrs={
            'class': 'form-control reg-login-form-item',
        })
    )
    confirmation = forms.CharField(
        label = _("Confirm Password"),
        required = True,
        widget = forms.PasswordInput(attrs={
            'class': 'form-control reg-login-form-item',
        })
    )


class RegisterAccountStage2Form(forms.ModelForm):
    bio = forms.CharField(
        label = _("Bio"),
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
        label = _("Theme"),
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
        label = _("Language"),
        required = True,
        widget = forms.Select(
            choices = User.LANGUAGES,
            # attrs = {
            #     'class': 'form-control',
            # }
        )
    )

    show_liked_posts = forms.BooleanField(
        label = _("Show Liked Posts"),
        help_text = _("Decide whether other users can see which posts you have liked."),
        required = False,
        # default = True,
        widget = forms.CheckboxInput(attrs={
            'class': 'form-control form-checkbox',
        })
    )

    class Meta:
        model = User
        fields = ['theme', 'language', 'show_liked_posts',]
