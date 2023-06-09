from django.urls import path
from . import views


app_name = 'chat'


urlpatterns = [
    # path('', views.ChatAPI.as_view(), name="ChatAPI"),
    # path('direct/<uuid:receiver_id>/', views.ChatAPI.as_view(), name="directMessage"),

    path('', views.index, name="index"),
    path('direct/<uuid:receiver_id>/', views.directMessage, name="directMessage"),

    path('group/', views.createGroup, name="createGroup"),
    path('group/<str:group_id>/', views.groupMessage, name="groupMessage"),
]