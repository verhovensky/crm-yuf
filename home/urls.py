from django.urls import path
from .views import HomePageView
# for static files
from django.contrib.staticfiles.urls import static
from django.conf import settings

app_name = 'home'

urlpatterns = [
    path('', HomePageView.as_view(), name="homepage"),
    #path('dashboard/', MainDashView.as_view(), name="dashboard"),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)