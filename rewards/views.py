from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .models import QRCode

class RegisterView(CreateView):
    template_name = 'registration/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('login')

def qr_code_list(request):
    qr_codes = QRCode.objects.all()
    return render(request, 'rewards/qr_code_list.html', {'qr_codes': qr_codes})