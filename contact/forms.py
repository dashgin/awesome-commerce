from django import forms
from .models import Contact
from common import widgets


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'

        widgets = {
            'full_name': widgets.StyledTextInput(attrs={"placeholder": "John Doe"}),
            'email': widgets.StyledTextInput(attrs={"placeholder": "john_doe@mail.com"}),
            'phone': widgets.StyledTextInput(attrs={"placeholder": "123-456-7890"}),
            'message': widgets.StyledTextarea(attrs={"placeholder": "Type your message here"}),
        }