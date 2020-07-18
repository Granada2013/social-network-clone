from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = 'index.html'


class TestView(TemplateView):
    template_name = 'test.html'


class ThanksView(TemplateView):
    template_name = 'thankyou.html'