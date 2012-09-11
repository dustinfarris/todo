from django import forms
from django.contrib.auth import forms as auth_forms


class NewUserForm(auth_forms.UserCreationForm):
  pass
  

class EditUserForm(auth_forms.UserChangeForm):
  _method = forms.CharField(widget=forms.HiddenInput(), initial='put')
  
  # class Meta:
  #   fields = ('username', 'first_name', 'last_name', 'email', '_method',)