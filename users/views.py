from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, TemplateView, UpdateView
from django.urls import reverse_lazy, reverse
from django.core.mail import send_mail
from django.conf import settings
from .models import User
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.views.generic.edit import FormView
from .forms import UserProfileForm
from .utils import account_activation_token
from django.http import HttpResponse
from .forms import SignUpForm

class SignUpView(CreateView):
    model = User
    form_class = SignUpForm
    template_name = 'users/signup.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        try:
            if user.email:  
                token = account_activation_token.make_token(user)
                uid = user.pk
                domain = self.request.get_host()
                link = f"http://{domain}{reverse('activate_account', kwargs={'uid': uid, 'token': token})}"
                send_mail(
                    'Verify Your Email',
                    f'Please click the link to activate your account: {link}',
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email],
                    fail_silently=False,
                )
                messages.success(self.request, 'Registration successful! Please check your email to verify.')
            else:
                messages.success(self.request, 'Registration successful! Please contact support to activate your account.')
        except Exception as e:
            messages.error(self.request, f'Failed to send verification email: {str(e)}')
        return super().form_valid(form)

class CustomLoginView(LoginView):
    template_name = 'users/login.html'

    def get_success_url(self):
        user = self.request.user
        print(f"User: {user.username}, Role: {user.role}")  
        if user.role == 'admin':
            return reverse_lazy('admin_dashboard')
        elif user.role == 'manager':
            return reverse_lazy('manager_dashboard')
        return reverse_lazy('client_dashboard')


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'users/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = UserProfileForm(instance=self.request.user)
        context['is_editing'] = self.request.session.get('is_editing', False)
        return context

    def post(self, request, *args, **kwargs):
        if 'edit' in request.POST:
            request.session['is_editing'] = True
            return redirect('profile')
        elif 'save' in request.POST:
            form = UserProfileForm(request.POST, request.FILES, instance=request.user)
            if form.is_valid():
                form.save()
                request.session['is_editing'] = False
                messages.success(request, 'Profile updated successfully!')
                return redirect('profile')
        elif 'cancel' in request.POST:
            request.session['is_editing'] = False
            return redirect('profile')
        return self.get(request, *args, **kwargs)

class MyEventsView(LoginRequiredMixin, TemplateView):
    template_name = 'users/my_events.html'

def activate_account(request, uid, token):
    user = get_object_or_404(User, pk=uid)
    if account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Account activated successfully! You can now log in.')
        return redirect('login')
    else:
        messages.error(request, 'Invalid activation link.')
        return redirect('signup')