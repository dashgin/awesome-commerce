from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView

from .models import Contact
from .forms import ContactForm


class ContactView(SuccessMessageMixin, CreateView):
    model = Contact
    form_class = ContactForm
    template_name = 'contact.html'
    success_url = '/contact/'
    success_message = 'Your message has been accepted'
