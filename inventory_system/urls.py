from django.urls import path
from . import views

urlpatterns = [
  path("", views.index, name="index"),
  path('siteadmin/', views.admin, name='admin'),
  path("login/", views.login_view, name="login"),
  path("login_user/", views.login_user, name="login_user"),
  path('logout/', views.logout_view, name='logout'),
  path("register/", views.register, name="register"),
  path("registration/", views.registration, name="registration"),
  path("new_equipment/", views.new_equipment, name="new_equipment"),
  path("add_product/", views.add_product, name="add_product"),
  path("list_products/", views.my_products_view, name="list_products"),
  path("search/", views.search_view, name='search'),
  path("edit_product/<int:product_id>/", views.edit_product_view, name='edit_product_view'),
  path("update_product/<int:product_id>/", views.update_product, name='update_product'),
  path('delete/<int:product_id>/', views.delete_product_view, name='delete_product'),
  path('product_reservation/<int:product_id>/', views.product_reservation, name='product_reservation'),
  path('reservationRequests', views.handle_reservation_request, name='handle_reservation_request'),
  path('your-reservations/', views.your_reservations, name='your_reservations'),

  path('remove_reservation/<int:reservation_id>/', views.remove_reservation, name='remove_reservation'),
  path('adminreservation-requests/', views.reservation_requests, name='reservation_requests'),

  path('approve_reservation/<int:reservation_id>/', views.approve_reservation, name='approve_reservation'),

  path('reject_reservation/<int:reservation_id>/', views.reject_reservation, name='reject_reservation'),
  path('reservation_requests/<int:reservation_id>/reclaim/', views.reclaim_reservation, name='reclaim_reservation'),
  path('api/reservations/', views.get_filtered_reservations, name='get_filtered_reservations'),
  path('return_products/<int:reservation_id>/', views.return_products, name='return_products'),


]