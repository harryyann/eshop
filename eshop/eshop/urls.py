"""eshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
#引入settings文件和static方法
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.authtoken import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('computer/', include('computerapp.urls', namespace='computer')),
    
]
 
#实现登录和token验证
urlpatterns += [
    path('api-auth', include('rest_framework.urls', namespace='rest_framework')), #实现登录的功能
    path('api-token-auth/', views.obtain_auth_token), #实现支持token的生成
]

#django的调试模式下，前端jquery访问默认无法找到media文件的位置，使用以下语句可以让django在调试模式下找到media
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
