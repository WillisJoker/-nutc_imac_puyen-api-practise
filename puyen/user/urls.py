"""puyen URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('register/', register),
    path('auth/', login),
    path('verification/send/', send),
    path('verification/check/', check),
    path('password/forgot/', forgot),
    path('password/reset/', reset),
    path('user/', userset),
    path('register/check/', recheck),
    path('user/default/', default),
    path('user/setting/', setting),
    path('user/blood/pressure/', pressure),
    path('user/weight/', weight),
    path('user/blood/sugar/', sugar),
    path('user/records/', records),
    path('user/a1c/', a1c),
    path('user/drug-used/', drug_used),
    path('user/medical/', medical),
    path('user/diet/', diet),
    path('user/last-upload/', last_upload),
    path('user/diary/', diary_get),
    path('friend/code/', friend_id_get),
    path('friend/send/', friend_id_send),
    path('friend/requests/', friend_id_requests),
    path('friend/<str:accept>/accept/',  friend_accept),
    path('friend/<str:refuse>/refuse/', friend_refuse),
    path('friend/<str:uid>/remove/', friend_remove),
    path('friend/list/', friend_list),
    path('friend/remove/', friend_delete),
    path('friend/results/', friend_request_result),
    path('user/care/', care),
    path('notification/', notification),
    path('user/badge/', badge),
    path('share/', share),
    path('share/0/', share_0),
    path('share/1/', share_1),
    path('share/2/', share_2),
    path('news/', news),
    path('notification/', notification)
]
