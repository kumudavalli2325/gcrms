from django import forms
from admin_site.models import User

class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = "__all__"

# class LoginForm(forms.ModelForm):
#
#     class Meta:
#         model = Login
#         fields = "__all__"



