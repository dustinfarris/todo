from django import forms

from models import Task


class NewTaskForm(forms.ModelForm):
  class Meta:
    model = Task
    exclude = ('user',)
    

class EditTaskForm(forms.ModelForm):
  _method = forms.CharField(widget=forms.HiddenInput(), initial='put')
  
  class Meta:
    model = Task
    exclude = ('user',)