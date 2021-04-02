from django import forms
from .models import TodoModel

class TodoForm(forms.ModelForm):
	class Meta:
		model = TodoModel
		fields = ['task']
		widgets = {
          'task': forms.Textarea(attrs={'rows':8, 'cols':55, 'style':'resize:none; -webkit-border-radius: 5px; -moz-border-radius: 5px; border-radius: 5px;', 'placeholder': 'Create Task'}),
        }

