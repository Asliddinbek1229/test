from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views import View

from .forms import LoginForm, UserRegisterForm, UserEditForm, ProfileEditForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView, UpdateView

from .models import Profile


# Create your views here.


def user_login(request):
    global context
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            # print(data)
            user = authenticate(
                request,
                username=data['username'],
                password=data['password']
            ) #Databasedan userni qidiradi
            # print(user)
            # print(request.POST)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Muvaffaqiyatli login amalga oshirildi')
                else:
                    return HttpResponse('Sizning profilingiz faol holatda emas!')

            else:
                return HttpResponse('Login va parolda xatolik bor')

    else:
        form = LoginForm()
        context = {
            'form': form
        }

    return render(request, 'registration/login.html', context)


def user_logout(request):
    logout(request)
    return redirect('home')


@login_required(login_url='login')
def dashboard_view(request):
    user = request.user
    profil = Profile.objects.get(user=user)
    context = {
        'user': user,
        'profil': profil
    }
    return render(request, 'pages/dashboard.html', context)


def user_register(request):
    if request.method == 'POST':
        user_form = UserRegisterForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(
                user_form.cleaned_data['password']
            )
            new_user.save()
            Profile.objects.create(user=new_user)
            context = {
                'new_user': new_user
            }
            return render(request, 'accounts/user_register_done.html', context=context)

    else:
        user_form = UserRegisterForm()
        context = {
            'user_form': user_form
        }
        return render(request, 'accounts/user_register.html', context)


class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'accounts/user_register.html'


@login_required(login_url='login')
def edit_user_view(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('dashboard')

    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)

    return render(request, 'accounts/profile_edit.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


class EditUserView(View):
    def get(self, request):
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)

        return render(request, 'accounts/profile_edit.html', {
            'user_form': user_form,
            'profile_form': profile_form})

    def post(self, request):
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('dashboard')