from django.urls import path
from . import views

urlpatterns = [
  #url(r'^$', views.search_page, name='search_page'),
	path('', views.search_page, name='search_page'),	
]
