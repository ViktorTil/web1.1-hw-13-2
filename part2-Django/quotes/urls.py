from django.urls import path, re_path

from . import views

app_name = "quotes"

urlpatterns = [
    path('', views.main, name = "root"),
    re_path(r'author/\w+', views.get_author_info, name='author'),
    re_path(r'tag/\w+', views.get_tag_quotes, name='tag'),
    path('add_author/', views.upload_author, name='add_author'),
    path('add_quote/', views.upload_quote, name='add_quote'),
    path('<int:page>', views.main, name = "root_paginate"),
    path('add_tag/', views.upload_tag, name = 'add_tag')
    
]