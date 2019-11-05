from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

app_name = 'computer'
urlpatterns = [
    path('products', views.ProductListView.as_view(), name='product-list'),
    #按目录分产品的url，访问时在路由后面使用?category=1(1代表笔记本等，具体定义在模型中)，category的值和代表什么需要和前端约定
    path('products_by_category', views.ProductListByCategoryView.as_view(), name='product-list-by-category'),
    path('products_by_category_manufacturer', views.ProductListByCategoryManufacturerView.as_view(), name='product-list-by-category-manufacturer'),
    path('products/<int:pk>/', views.ProductRetrieveView.as_view(), name='product-retrieve'),
    path('user_info/', views.UserInfoView.as_view(), name='user-info'),
    path('user_profile_ru/<int:pk>/', views.UserProfileRUView.as_view(),name='user_profile_ru'),
    path('user_create/', views.UserCreateView.as_view(), name='user_create'),
    path('delivery_address_lc', views.DeliveryAddressLCView.as_view(), name='delivery_address_lc'),
    path('delivery_address_rud/<int:pk>/', views.DeliveryAddressRUDView.as_view(), name='delivery_address_rud'),

]



#允许以.json的形式访问url
urlpatterns = format_suffix_patterns(urlpatterns) 