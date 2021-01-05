from django.urls import path

from . import views

urlpatterns = [
  path("", views.index, name="index"),
  path("shop", views.shop, name="shop"),
  path("item/create", views.create_item_view, name="create_item"),
  path("item/<int:id>", views.retrieve_item_view, name="retrieve_item"),
  path("item/update/<int:id>", views.update_item_view, name="update_item"),
  path("item/delete/<int:id>", views.delete_item_view, name="delete_item"),
  path("user", views.user, name="user"),
  path("user/create", views.create_user_view, name="create_user"),
  path("user/update/<int:id>", views.update_user_view, name="update_user"),
  path("payment", views.payment, name="payment"),
  path("journal", views.journal, name="journal"),
  path("about", views.about, name="about"),
  path("cart", views.cart, name="cart"),
  path("add_to_cart", views.add_to_cart, name="add_to_cart"),
  path("profile", views.profile_view, name="profile"),
  path("login", views.login_view, name="login"),
  path("register", views.register_view, name="register"),
  path("logout", views.logout_view, name="logout"),
  path("provinces/", views.provinces, name="provinces"),
  path("cities/", views.cities, name="cities"),
  path("cities/<int:id>/", views.cities, name="province_cities"),
  path("city/<int:id>/", views.city, name="city"),
  path("cost/<int:id>/", views.cost, name="cost"),
]