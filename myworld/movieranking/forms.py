from django import forms
from .models import Comment, CustomUser
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        
class CustomUserCreationForm(UserCreationForm):
    security_question = forms.CharField(max_length=255, required=True)
    security_answer = forms.CharField(max_length=255, required=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'security_question', 'security_answer', 'password1', 'password2')
        
        
# class ForgotPasswordForm(forms.Form):
#     email = forms.EmailField(label='Email', required=True)
    
# class SecurityQuestionForm(forms.Form):
#     security_answer = forms.CharField(label='Security Answer', required=True)


# class MyPasswordResetForm(PasswordResetForm):
#     new_password2 = forms.CharField(
#         label="Confirm New Password",
#         widget=forms.PasswordInput,
#     )

#     def clean_new_password2(self):
#         cd = self.cleaned_data
#         if cd['new_password'] != cd['new_password2']:
#             raise forms.ValidationError("Passwords don't match.")
#         return cd['new_password2']
