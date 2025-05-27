from django.views.generic import TemplateView

class MainPage(TemplateView):
    template_name = 'pages/index.html'

class AboutView(TemplateView):
    template_name = 'pages/about.html'

class ProjectsView(TemplateView):
    template_name = 'pages/projects.html'

class ContactView(TemplateView):
    template_name = 'pages/contact.html'