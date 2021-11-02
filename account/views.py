from django.contrib.auth.models import User
from .forms import UserEditForm, ProfileEditForm
# login required mixin
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.generic import TemplateView, UpdateView


@method_decorator(login_required, name='dispatch')
class ProfileView(TemplateView):
    template_name = 'account/dashboard.html'
    title = 'Мой профиль'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = User.objects.get(pk=self.request.user.pk)
        return context

    def get(self, request, *args, **kwargs):
        return render(request, template_name=self.template_name,
                      context={'page_title': self.title})


@method_decorator(login_required, name='dispatch')
class EditProfile(UpdateView):
    template_name = 'account/editprofile.html'
    title = 'Изменить профиль'
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
            return render(request, template_name='account/dashboard.html',
                          context={'page_title': 'Мой профиль'})
