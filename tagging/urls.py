from django.urls import path
from . import views

urlpatterns = [
    path('', views.initialize_tags, name='initialize_tags'),
    path('tag-content/', views.tag_content, name='tag_content'),
   path('content_detail/<int:id>/', views.tagged_content_detail, name='tagged_content_detail'),
   path('delete_content/<int:id>/', views.delete_tagged_content, name='delete_tagged_content'),
    path('history/', views.tagged_content_history, name='tagged_content_history'),
    
   


]