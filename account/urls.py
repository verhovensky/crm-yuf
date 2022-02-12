from django.urls import path
from .views import ProfileView, EditProfile
# for static files
from django.contrib.staticfiles.urls import static
from django.conf import settings

app_name = 'account'

urlpatterns = [
    path('', ProfileView.as_view(), name="profile"),
    path('edit/', EditProfile.as_view(), name="edit_profile")
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
