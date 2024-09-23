from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import MemberView

urlpatterns = [
    path('member/register', MemberView.as_view(), name='member-register'),
]