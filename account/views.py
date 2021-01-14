from .models import UserProfile
from .forms import UserEditForm, ProfileEditForm
# login required mixin
from django.contrib.auth.decorators import login_required

#from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound
from django.template import loader

# Profile display page
@login_required
def profile(request):
    title = 'Мой профиль'
    header = 'Мой профиль'
    template = loader.get_template('account/dashboard.html')
    context = {'userprofile': UserProfile, 'page_title': title, 'header_page': header}
    return HttpResponse(template.render(context, request))


@login_required
def editprofile(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.userprofile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return profile(request)
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.userprofile)
        title = 'Изменить профиль'
        header = 'Изменить профиль'
        template = loader.get_template('account/editprofile.html')
        context = {'user_form': user_form, 'profile_form': profile_form, 'page_title': title, 'header_page': header}
        return HttpResponse(template.render(context, request))