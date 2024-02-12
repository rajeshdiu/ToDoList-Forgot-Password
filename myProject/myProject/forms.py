from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from myApp.models import *

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = Custom_User
        fields = UserCreationForm.Meta.fields + ('display_name', 'email','city')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for field_name in self.fields:
            self.fields[field_name].help_text = None

class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = Custom_User  
        fields = ['email', 'password']

class TaskForm(forms.ModelForm):
    class Meta:
        model = myTaskModel
        fields = ['title', 'description', 'due_date', 'priority', 'category', 'notes']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }

class SearchForm(forms.Form):
    query = forms.CharField(max_length=100, label='Search for tasks')

class TaskCategoryForm(forms.ModelForm):
    class Meta:
        model = TaskCategory
        fields = ['name']
