from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import Ticket

class TicketForm(forms.ModelForm):
    ''' Model from for ticket data. '''
    
    class Meta:
        model = Ticket
        # fields that will be in the form
        fields = ['date', 'n1', 'n2', 'n3', 'n4', 'n5', 'n6']
        
        

class UserCreateForm(UserCreationForm):
    ''' Extending the default Django form for registration by adding an email field'''
    email = forms.EmailField(required=False)
    
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        # saving user with email
        user = super(UserCreateForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
