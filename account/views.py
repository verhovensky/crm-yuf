from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from account.forms import UserEditForm, RegisterUserForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views.generic import DetailView, TemplateView
from .decorators import authenticated_user

User = get_user_model()


@authenticated_user
def user_login(request):
    if request.method == "POST":
        u = request.POST.get("username")
        p = request.POST.get("password")
        user = authenticate(request,
                            username=u,
                            password=p)
        if user is not None and user.is_active:
            login(request, user)
            if request.POST["next"] is not None:
                return redirect(request.POST["next"])
            else:
                return redirect("home:homepage")
        else:
            messages.warning(
                request, "Имя пользователя или пароль неверны!")
    next_page = request.GET.get("next")
    context = {"next": next_page}
    return render(request, "account/login.html", context)


def user_logout(request):
    logout(request)
    return redirect("home:homepage")


@authenticated_user
def user_register(request):
    form_user = RegisterUserForm

    if request.method == "POST":
        form_user = RegisterUserForm(request.POST)
        if form_user.is_valid():
            user = form_user.save()
            sellers_group = Group.objects.get(
                name="Sellers")
            sellers_group.user_set.add(user)
            messages.success(request,
                             f"Пользователь {user.username} "
                             f"успешно создан")
            return redirect("home:homepage")
        else:
            messages.info(request, f"{form_user.errors}")

    context = {"form_user": form_user}
    return render(request, "account/register.html", context)


class ProfileView(LoginRequiredMixin, DetailView):
    template_name = "account/account_detail.html"
    extra_context = {"page_title": "Мой профиль"}

    def get_object(self, queryset=None):
        return User.objects.get(pk=self.request.user.pk)


class EditProfile(LoginRequiredMixin, TemplateView):
    extra_context = {"page_title": "Изменить профиль"}
    template_name = "account/account_form.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(
            user_form=UserEditForm(initial={
                "first_name": self.request.user.first_name,
                "last_name": self.request.user.last_name,
                "email": self.request.user.email,
                "date_of_birth": self.request.user.date_of_birth,
                "phone_number": self.request.user.phone_number,
                "photo": self.request.user.photo}))
        return render(request,
                      template_name="account/account_form.html",
                      context=context)

    def post(self, request, *args, **kwargs):

        user_form = UserEditForm(request.POST,
                                 instance=request.user)
        context = self.get_context_data(user_form=user_form)
        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(
                reverse_lazy("account:profile"))
        return self.render_to_response(context)
