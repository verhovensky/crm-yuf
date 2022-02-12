from django.contrib.auth.models import User
from .forms import UserEditForm, ProfileEditForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import DetailView, UpdateView


class ProfileView(LoginRequiredMixin, DetailView):
    title = 'Мой профиль'
    template_name = 'account/account_detail.html'

    def get_object(self, queryset=None):
        return User.objects.get(pk=self.request.user.pk)


class EditProfile(LoginRequiredMixin, UpdateView):
    title = 'Изменить профиль'
    template_name = 'account/account_form.html'
    success_url = '/'

    def get(self, request, *args, **kwargs):
        return render(request, template_name=self.template_name,
                      context={'page_title': self.title,
                               'user_form': UserEditForm
                               (instance=request.user),
                               'profile_form': ProfileEditForm
                               (instance=request.user.userprofile)})

    def post(self, request, *args, **kwargs):
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.userprofile,
                                       data=request.POST,
                                       files=request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return render(request,
                          template_name='account/account_detail.html')
