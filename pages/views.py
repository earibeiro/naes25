from django.views.generic import TemplateView, ListView, DetailView

class MainPage(TemplateView):
    template_name = 'pages/index.html'