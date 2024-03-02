from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView
from django.urls import reverse_lazy

from .models import Contact
from .forms import ContactForm


class ContactView(SuccessMessageMixin, CreateView):
    model = Contact
    form_class = ContactForm
    template_name = 'pages/contact.html'
    success_url = reverse_lazy('contact') # => /contact/
    success_message = 'Your message has been accepted'
