from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import TemplateView


class HomePageView(LoginRequiredMixin, TemplateView):
    template_name = 'home/homepage.html'

    def get(self, request, *args, **kwargs):
        return render(request, template_name=self.template_name,
                      context={'page_title': 'Главная'})
