from django import forms
from django.core.files.images import get_image_dimensions

from network.models import User


class EditAccountForm(forms.ModelForm):
    username = forms.CharField(
        required=False,
        widget = forms.TextInput(attrs={
            'class': 'form-control',
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
        label = "New Post",
        max_length = 500,
        required = True,
        widget = forms.Textarea(attrs={
            'rows':3
        })
    )


class RegisterAccountForm(forms.Form):
    username = forms.CharField(
        label = "Username",
        max_length = 20,
        required = True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Up to 20 characters, alphanumeric',
            'class': 'form-control',
            'autofocus': True,
        })
    )
    displayname = forms.CharField(
        label = "Display Name",
        max_length = 50,
        required = True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Up to 50 characters',
            'class': 'form-control',
        })
    )
    email = forms.EmailField(
        label = "Email",
        required = True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
        })
    )
    password = forms.CharField(
        label = "Password",
        required = True,
        widget = forms.PasswordInput(attrs={
            'class': 'form-control'
        })
    )
    confirmation = forms.CharField(
        label = "Confirm Password",
        required = True,
        widget = forms.PasswordInput(attrs={
            'class': 'form-control',
        })
    )


# TODO this is some stuff i copied from stackoverflow
# see what this does and if i can use it to better implement avatars
# class UserProfileForm(forms.ModelForm):
#     class Meta:
#         model = User

#     def clean_avatar(self):
#         avatar = self.cleaned_data['avatar']

#         try:
#             w, h = get_image_dimensions(avatar)

#             #validate dimensions
#             max_width = max_height = 100
#             if w > max_width or h > max_height:
#                 raise forms.ValidationError(
#                     u'Please use an image that is '
#                      '%s x %s pixels or smaller.' % (max_width, max_height))

#             #validate content type
#             main, sub = avatar.content_type.split('/')
#             if not (main == 'image' and sub in ['jpeg', 'pjpeg', 'gif', 'png']):
#                 raise forms.ValidationError(u'Please use a JPEG, '
#                     'GIF or PNG image.')

#             #validate file size
#             if len(avatar) > (20 * 1024):
#                 raise forms.ValidationError(
#                     u'Avatar file size may not exceed 20k.')

#         except AttributeError:
#             """
#             Handles case when we are updating the user profile
#             and do not supply a new avatar
#             """
#             pass

#         return avatar