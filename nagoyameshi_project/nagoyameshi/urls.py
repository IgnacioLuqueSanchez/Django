from django.urls import path


# views.pyをimportする。
from nagoyameshi import views



app_name    = "nagoyameshi"
urlpatterns = [
    path("", views.index, name="index"),
    path("restaurant/<int:pk>/", views.restaurant, name="restaurant" ),
    path("review/", views.revieweview, name="review"),
    #path('review/', ReviewView.as_view(), name='review'),
    path("favorite/", views.favorite, name="favorite"),
    #             ↑ <int:pk> は int型(整数型)の場合、整数をpkとして扱う。このpkをビューに引き渡す。
    # restaurant/1/ や restaurant/3/ 
  

]