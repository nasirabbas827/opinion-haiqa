from django import forms
from .models import user_register

class user_registerForm(forms.ModelForm):
    class Meta:
        model = user_register
        fields = ['profile_picture', 'full_name', 'username', 'email', 'password', 'gender', 'age']
        widgets = {
            'password': forms.PasswordInput(),
        }

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)



from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 4}),
        }

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = user_register
        fields = ['profile_picture', 'full_name', 'email', 'gender', 'age']