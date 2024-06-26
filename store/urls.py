from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name='home'),
    # path('populate_product/<int:n>',views.populate_product, name='populate_product'),
    path('product_search/<str:search>/',views.product_search, name='product_search'),
    path('search_product/<str:search>/',views.search_product, name='search_product'),
    path('search-products/<str:search_param>/',views.product_search_results, name='search-products'),
    path('cart/',views.cart, name='cart'),
    path('checkout/',views.checkout, name='checkout'),
    path('all_products/',views.all_products, name='all_products'),
    path('product_single/<int:id>/', views.product_single, name='product_single'),
    path('all_stores/',views.all_stores, name='all_stores'),
    path('login/',views.login_user, name='login'),
    path('login-popup/',views.login_user_popup, name='login-popup'),
    path('register/',views.register_user, name='register'),
    path('email_verification/',views.email_verify, name='email_verification'),
    path('otp-verification/',views.otp_verification_forgotpass, name='otp-verification'),
    path('resend_otp_email/',views.resend_otp_email, name='resend_otp_email'),
    path('logout/',views.logout_user, name='logout'),
    path('forgotpass/',views.forgotpass, name='forgotpass'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('orders/',views.orders_user,name='orders'),
    path('order_tracking/',views.order_tracking,name='order_tracking'),
    path('address/',views.address_user,name='address'),
    path('address-add/',views.address_user_add,name='address-add'),
    path('address-edit/<int:id>',views.address_user_edit,name='address-edit'),
    path('payment_method/',views.payment_method,name='payment_method'),
    path('my_reviews/',views.my_reviews,name='my_reviews'),
    path('referal/',views.referal,name='referal'),
    path('my_favourites/',views.my_favourites,name='my_favourites'),
    path('add_to_cart/<int:id>',views.add_to_cart,name='add_to_cart'),
    path('add_to_cart_api/<int:id>/',views.add_to_cart_api,name='add_to_cart_api'),
    path('remove_from_cart/<int:id>/',views.remove_from_cart,name='remove_from_cart'),
    path('clear_cart/',views.clear_cart,name='clear_cart'),
    path('increase_cart_count/<int:id>/',views.increase_cart_count,name='increase_cart_count'),
    path('decrease_cart_count/<int:id>/',views.decrease_cart_count,name='decrease_cart_count'),
    path('add_to_favourite/<int:id>/',views.add_to_favourite,name='add_to_favourite'),
    path('remove_from_favourite/<int:id>/',views.remove_from_favourite,name='remove_from_favourite'),
    path('all_category/',views.all_category,name='all_category'),
    path('all_category/<str:category_name>/',views.category_detail,name='all_category'),
    path('all_category/<str:category_name>/<str:midcategory_name>/',views.subcategory_detail,name='subcategory_detail'),
    path('add_browsing_data/<int:id>/',views.add_browsing_data,name='add_browsing_data'),

]
