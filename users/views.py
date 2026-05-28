from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import DetailView, FormView

from users.forms import LoginForm
from users.models import User


class PerfilView(LoginRequiredMixin, DetailView):
    template_name = 'users/mi_perfil.html'
    context_object_name = 'perfil'
    model = User

    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['es_propio'] = self.request.user.is_authenticated and self.request.user == self.get_object()
        return context

class LoginModifiedView(FormView):
    template_name = 'registration/login.html'
    form_class = LoginForm

    def get_success_url(self):
        user = self.request.user.username
        return reverse('users:perfil', kwargs={'username': user})

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            login(self.request, user)

            next_url = self.request.GET.get('next')
            if next_url:
                return redirect(next_url)
            return super().form_valid(form)

        messages.error(self.request, 'Credenciales incorrectas')
        return super().form_invalid(form)

