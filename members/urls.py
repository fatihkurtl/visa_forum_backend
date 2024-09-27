from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('register', views.RegisterView.as_view(), name='member-register'),
    path('login', views.LoginView.as_view(), name='member-login'),
    path('<str:username>', views.MemberDetailView.as_view(), name='member-detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)