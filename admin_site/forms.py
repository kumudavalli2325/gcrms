from django import forms
from admin_site.models import User
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = "__all__"



