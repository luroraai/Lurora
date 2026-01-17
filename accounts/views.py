from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordResetView
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from .forms import CustomUserCreationForm, LoginForm, ProfileUpdateForm
from django.contrib.auth.mixins import LoginRequiredMixin
from stories.models import Stories, Scenes
from stories.tables import StoryBasicTable


# from .forms import LoginForm, RegisterForm


class CustomLoginView(LoginView):
    form_class = AuthenticationForm
    template_name = 'accounts/login.html'
    success_url = reverse_lazy('accounts:dashboard')
    redirect_authenticated_user = True


class ProfileView(TemplateView, LoginRequiredMixin):
    template_name = 'accounts/profile.html'
    form_class = ProfileUpdateForm
    success_url = reverse_lazy('accounts:profile')


@login_required(login_url='accounts:index')
def profile(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account information has been updated!')
            return redirect('accounts:profile')
    else:
        form = ProfileUpdateForm(instance=request.user)

    context = {
        'form': form,

    }
    return render(request, 'accounts/profile.html', context)


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('accounts:dashboard')
        else:
            for error in form.errors.values():
                messages.error(request, error)
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})


@login_required
def dashboard(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
    else:
        form = CustomUserCreationForm(instance=request.user)
    stories = Stories.objects.filter(author=request.user).order_by('-created_at').all()
    stories_count = stories.count()
    table = StoryBasicTable(stories)
    context = {
        'form': form,
        'stories': stories,
        'stories_count': stories_count,
        'table': table,
        'title': 'Dashboard'
    }
    return render(request, 'accounts/dashboard.html', context)


def logout_view(request):
    logout(request)
    return redirect('accounts:dashboard')
