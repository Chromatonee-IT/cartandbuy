from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.urls import re_path as url
from django.views.static import serve
from django.contrib.auth import views as auth_views


urlpatterns = [
    url(r'^media/(?P<path>.*)$', serve,{'document_root':settings.MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$', serve,{'document_root':settings.STATIC_ROOT}),
    path('vendor/',views.home,name='v_home'),
    path('terms_and_conditions/',views.terms_and_conditions,name='terms_and_conditions'),
    path('v_dashboard/',views.dashboard,name='v_dashboard'),
    path('admin_dashboard/',views.dashboard,name='v_dashboard'),
    path('store_details/',views.vendor_profile,name='store_details'),
    path('products/',views.all_products,name='products'),
    path('orders_vendor/',views.all_orders,name='orders_vendor'),
    path('order_details/<int:id>',views.order_details,name='order_details'),
    path('customers/',views.customers,name='customers'),
    path('customer_details/<int:id>',views.customer_details,name='customer_details'),
    path('sales_promotions/',views.sales_promotions,name='sales_promotions'),
    path('coupon_edit/<int:id>',views.coupon_edit,name='coupon_edit'),
    path('coupon_add/',views.coupon_add,name='coupon_add'),
    path('coupon_delete/<int:id>',views.coupon_delete,name='coupon_delete'),
    path('all_invoices/',views.all_invoices,name='all_invoices'),
    path('create_invoice/',views.create_invoice,name='create_invoice'),
    path('update_invoice/<int:id>',views.update_invoice,name='update_invoice'),
    path('all_report/',views.all_report,name='all_report'),
    path('help/',views.help,name='help'),
    path('product_add/',views.product_add,name='product_add'),
    path('add_product_variant/<int:id>',views.add_product_variant,name='add_product_variant'),
    path('update_product_variant/',views.update_product_variant,name='update_product_variant'),
    path('product_details/<str:id>',views.product_details,name='product_details'),
    path('delete_variant/<int:id>',views.delete_variant,name='delete_variant'),
    path('v_login/',views.vendor_login,name='v_login'),
    path('vendor_register/',views.v_register,name='v_register'),
    path('vendor_register/<str:ref_code>',views.v_register,name='v_register'),
    path('waiting_email_verification/',views.waiting_email_verification,name='waiting_email_verification'),
    path('verify_email/',views.verify_email,name='verify_email'),
    path('v_register_type/',views.v_register_type,name='v_register_type'),
    path('v_register_gst/',views.v_register_gst,name='v_register_gst'),
    path('v_register_aadhaar/',views.v_register_aadhaar,name='v_register_aadhaar'),
    path('vendor_logout/',views.vendor_logout,name='vendor_logout'),

    path('vendor_reset_email/',views.vendor_reset_email,name='vendor_reset_email'),
    path('vendor_resetpassword/',views.vendor_resetpassword,name='vendor_resetpassword'),
    path('resend_otp_vendor/',views.resend_otp_vendor,name='resend_otp_vendor'),
    path('vendor_setpassword/',views.vendor_setpassword,name='vendor_setpassword'),
    path('toggle-product/<int:product_id>/', views.toggle_product, name='toggle_product'),
    path('add_product_variant/<int:var_id>/', views.toggle_product, name='add_product_variant'),
    path('generate_invoice/<int:id>', views.generate_invoice, name='generate_invoice'),

    path('vendor_admin_login/', views.vendor_admin_login, name='vendor_admin_login'),
    path('vendor_admin/', views.vendor_admin, name='vendor_admin'),
    path('vendor_admin_all/', views.vendor_admin_all, name='vendor_admin_all'),
    path('vendor_gst/<int:id>', views.vendor_gst, name='vendor_gst'),
    path('vendor_aadhaar/<int:id>', views.vendor_aadhaar, name='vendor_aadhaar'),
    ]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)