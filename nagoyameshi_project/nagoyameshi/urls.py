from django.urls import path

# views.pyをimportする。
from . import views


app_name    = "nagoyameshi"
urlpatterns = [
    path("", views.index, name="index"),
    path("restaurant/", views.restaurant, name="restaurant" ),

]