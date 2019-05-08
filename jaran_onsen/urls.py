from django.urls import path
from . import views

urlpatterns = [
	path('jaran_onsen/', views.jaran_onsen_list, name='jaran_onsen_list'),
	path('jaran_onsen/<int:onsen_id>/', views.jaran_onsen_detail, name='jaran_onsen_detail'),
    path('jaran_onsen/api/new', views.jaran_onsen_api, name='jaran_onsen_api'),
	#path('jaran_onsen/api/new_onsens', views.jaran_onsens_added, name='jaran_onsens_added'),
]
