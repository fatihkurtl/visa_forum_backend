from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('', views.ThreadsView.as_view(), name='thread-list'),
    path('<int:pk>/', views.ThreadsDetailView.as_view(), name='thread-detail'),
    path('categories/', views.ThreadsCategoriesView.as_view(), name='thread-categories'),
    path('create/', views.ThreadsCreateView.as_view(), name='thread-create'),
    path('<int:pk>/add/comment/', views.ThreadsAddCommentView.as_view(), name='thread-add-comment'),
    path('<int:pk>/add/reply/', views.ThreadsAddReplyView.as_view(), name='thread-add-reply'),  
]

urlpatterns = format_suffix_patterns(urlpatterns)