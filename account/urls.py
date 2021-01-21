from django.urls import path
from .views import profile, editprofile
# for static files
from django.contrib.staticfiles.urls import static
from django.conf import settings

urlpatterns = [
    path('', profile, name="profile"),
    path('edit', editprofile, name="editprofile")] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)