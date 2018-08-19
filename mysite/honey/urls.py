from django.conf.urls import url
from . import views

app_name = 'honey'
urlpatterns = [
    url(r'^$', views.HomePageView.as_view(), name='home'),
    url(r'^test$', views.TestPageView.as_view(), name='test'),
]
