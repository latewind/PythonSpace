from django.views.generic import TemplateView


class HomePageView(TemplateView):
    template_name = "honey/home.html"



class TestPageView(TemplateView):
    template_name = "honey/test.html"
