from django.urls import path,include
from . import views
urlpatterns = [
 path('',views.index,name="index"),
 path('signup/',views.sign_up,name="signup"),
 path('signin/',views.sign_in,name="signin"),
 path('logout/',views.Logout,name="logout"),
 path('full/',views.full,name="full"),
 path('card/',views.card,name="card"),
 path('add-cart/',views.add_cart,name="add_cart"),
 path('remove-cart/',views.remove_cart,name="remove_cart"),
 path('place-order/',views.place_order,name="place_order"),
 path('buy/<int:pk>/',views.buy,name="buy"),
 path('all-order/',views.buy_cart,name="all_order"),
 path('order-views/',views.order_view,name="order_views"),
 path('product-buy/',views.product_buy,name="product_buy"),
 path('my-address/',views.my_address,name="my_address"),
 path('delet-address/<int:pk>/',views.delet_address,name="delet_address"),
 path('update-address/',views.update_address,name="update_address"),
 path('searching-elements/',views.searching,name="search"),
  path('all/',views.cat_all,name="all"),
  path('test/',views.test,name="test"),
 
]