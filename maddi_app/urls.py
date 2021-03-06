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
  path("user/delete/<int:id>", views.delete_user_view, name="delete_user"),
  path("news", views.news, name="news"),
  path("news/create", views.create_news_view, name="create_news"),
  path("news/update/<int:id>", views.update_news_view, name="update_news"),
  path("news/delete/<int:id>", views.delete_news_view, name="delete_news"),
  path("about", views.about, name="about"),
  path("cart", views.cart, name="cart"),
  path("add_to_cart", views.add_to_cart, name="add_to_cart"),
  path("cart/update", views.update_cart_view, name="update_cart"),
  path("cart/delete/<int:id>", views.delete_cart_view, name="delete_cart"),
  path("checkout", views.checkout, name="checkout"),
  path("payment_method", views.payment_method, name="payment_method"),
  path("purchase", views.purchase, name="purchase"),
  path("purchase/<int:id>", views.retrieve_purchase_view, name="retrieve_purchase"),
  path("process_payment_proof/<int:id>", views.process_payment_proof_view, name="process_payment_proof"),
  path("complete_purchase/<int:id>", views.complete_purchase_view, name="complete_purchase"),
  path("cancel_purchase/<int:id>", views.cancel_purchase_view, name="cancel_purchase"),
  path("report_weekly", views.report_weekly, name="report_weekly"),
  path("report_monthly", views.report_monthly, name="report_monthly"),
  path("report_yearly", views.report_yearly, name="report_yearly"),
  path("profile", views.profile_view, name="profile"),
  path("login", views.login_view, name="login"),
  path("register", views.register_view, name="register"),
  path("logout", views.logout_view, name="logout"),
  path("provinces/", views.provinces, name="provinces"),
  path("cities/", views.cities, name="cities"),
  path("cities/<int:id>/", views.cities, name="province_cities"),
  path("city/<int:id>/", views.city, name="city"),
  path("cost/<int:id>/", views.cost, name="cost"),
  path("chart_maddi_weekly", views.chart_maddi_weekly, name="chart_maddi_weekly"),
  path("chart_maddi_monthly", views.chart_maddi_monthly, name="chart_maddi_monthly"),
  path("chart_maddi_yearly", views.chart_maddi_yearly, name="chart_maddi_yearly"),
]