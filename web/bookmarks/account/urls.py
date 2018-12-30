from django.conf.urls import url
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from django.contrib.auth.views import logout_then_login
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.views import PasswordChangeDoneView
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.views import PasswordResetDoneView
from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib.auth.views import PasswordResetCompleteView
from . import views

urlpatterns = [
    # url(r'^login/$', views.user_login, name='user_login'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^logout-then-login/$', logout_then_login, name='logout_then_login'),
    url(r'^password-change/$', PasswordChangeView.as_view(), name='password_change'),
    url(r'^password-change/done/$', PasswordChangeDoneView.as_view(), name='password_change_done'),
    url(r'^password-reset/$',
        PasswordResetView.as_view(),
        name='password_reset'),
    url(r'^password-reset/done/$',
        PasswordResetDoneView.as_view(),
        name='password_reset_done'),
    url(r'^password-reset/confirm/(?P<uidb64>[-\w]+)/(?P<token>[-\w]+)/$',
        PasswordResetConfirmView.as_view(),
        name='password_reset_confirm'),
    url(r'^password-reset/complete/$',
        PasswordResetCompleteView,
        name='password_reset_complete'),
    url(r'^$', views.dashboard, name='dashboard'),
    url(r'^edit', views.edit, name='edit'),
    url(r'^register', views.register, name='register'),

    url(r'^users/$', views.user_list, name='user_list'),
    url(r'^users/detail/(?P<username>[-\w]+)/$',
        views.user_detail,
        name='user_detail'),
    url(r'^users/follow/$', views.user_follow, name='user_follow'),

    url(r'^admin/login/$', views.admin_login, name='admin_login'),

]
