from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from .forms import UserEditForm, ProfileEditForm, RegisterUserForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views.generic import DetailView, TemplateView


def user_login(request):
    if request.method == 'POST':
        u = request.POST.get('username')
        p = request.POST.get('password')

        user = authenticate(request, username=u, password=p)

        if user is not None and user.is_active:
            login(request, user)
            if request.POST['next'] is not None:
                return redirect(request.POST['next'])
            else:
                return redirect('home:homepage')
        else:
            messages.info(request, 'Имя пользователя или пароль неверны!')

    next_page = request.GET.get('next')
    context = {'next': next_page}

    return render(request, 'account/login.html', context)


def user_logout(request):
    logout(request)
    return redirect('home:homepage')


def user_register(request):
    form_user = RegisterUserForm

    if request.method == 'POST':
        form_user = RegisterUserForm(request.POST)
        if form_user.is_valid():
            form_user.save()
            user = form_user.cleaned_data.get('username')
            messages.success(request, f'Пользователь {user} успешно создан')
            # Redirect to dashboard
            return redirect('home:homepage')
        else:
            messages.info(request, f'{form_user.errors}')

    context = {'form_user': form_user}
    return render(request, 'account/register.html', context)


class ProfileView(LoginRequiredMixin, DetailView):
    template_name = 'account/account_detail.html'
    extra_context = {'page_title': 'Мой профиль'}

    def get_object(self, queryset=None):
        return User.objects.get(pk=self.request.user.pk)


class EditProfile(LoginRequiredMixin, TemplateView):
    extra_context = {'page_title': 'Изменить профиль'}
    template_name = 'account/account_form.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(user_form=UserEditForm
                                       (initial={'first_name': self.request.user.first_name,
                                                 'last_name': self.request.user.last_name,
                                                 'email': self.request.user.email}),
                                        profile_form=ProfileEditForm
                                        (initial={'date_of_birth':
                                                   self.request.user.userprofile.date_of_birth,
                                                  'phone_number': self.request.user.userprofile.phone_number,
                                                  'photo': self.request.user.userprofile.photo}))
        return render(request,
                      template_name='account/account_form.html',
                      context=context)

    def post(self, request, *args, **kwargs):

        user_form = UserEditForm(request.POST,
                                 instance=request.user)

        profile_form = ProfileEditForm(request.POST,
                                       request.FILES,
                                       instance=request.user.userprofile)

        context = self.get_context_data(user_form=user_form,
                                        profile_form=profile_form)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return HttpResponseRedirect(reverse_lazy('account:profile'))

        return self.render_to_response(context)
