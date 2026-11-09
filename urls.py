from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from restaurant import views
urlpatterns = [
 path("admin/", admin.site.urls), path("", views.home, name="home"),
 path("menu/", views.menu, name="menu"), path("cart/", views.cart, name="cart"),
 path("order/", views.place_order, name="place_order"),
 path("reservations/", views.reservation, name="reservation"),
 path("location/", views.location, name="location"), path("about/", views.about, name="about"),
 path("add-to-cart/<int:food_id>/", views.add_to_cart, name="add_to_cart"),
 path("remove-from-cart/<int:food_id>/", views.remove_from_cart, name="remove_from_cart"),
]
if settings.DEBUG: urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
