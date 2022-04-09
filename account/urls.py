from django.urls import path, reverse_lazy
from .views import ProfileView, EditProfile, user_register, user_login, user_logout
# for static files
from django.contrib.auth import views as auth_views
from django.contrib.staticfiles.urls import static
from django.conf import settings

app_name = 'account'

urlpatterns = [
    path('', ProfileView.as_view(), name="profile"),
    path('register/', user_register, name="register"),
    path('login/', user_login, name="login"),
    path('logout/', user_logout, name="logout"),
    path('reset_password/', auth_views.PasswordResetView.as_view(
          template_name='account/password_reset.html',
          email_template_name='account/password_reset_email.html',
          success_url=reverse_lazy('account:password_reset_done')),
          name='password_reset'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(
          template_name='account/password_reset_done.html'),
          name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
          template_name='account/password_reset_form.html',
          success_url=reverse_lazy('account:password_reset_complete')),
          name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(
          template_name='account/password_reset_complete.html'),
          name='password_reset_complete'),
    path('edit/', EditProfile.as_view(), name="edit_profile"),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
