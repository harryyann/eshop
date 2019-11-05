from django.shortcuts import render

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.pagination import LimitOffsetPagination
from .models import Product, UserProfile, DeliveryAddress
from .serializers import ProductListSerializer, ProductRetrieveSerializer, UserInfoSerializer, UserProfileSerializer, UserSerializer, DeliveryAddressSerilizer
from rest_framework.exceptions import NotFound
# Create your views here.

#产品模块
class ProductListView(generics.ListAPIView):
    '''
    产品列表
    '''
    queryset = Product.objects.all()  #定义查询集，这里简单的查询了全部
    serializer_class = ProductListSerializer #指定view使用的是哪个序列器
    permission_classes = (permissions.AllowAny,) #设定权限为允许所有人访问，注意要加逗号

    filter_backends = (OrderingFilter, SearchFilter) #设置排序器，搜索器
    ordering_fields = ('category', 'manufacturer', 'created', 'sold',) #设置过滤器
    search_fields = ('description','model',) #设置按什么搜索
    ordering = ('-id',) #默认的排序方式

    pagination_class = LimitOffsetPagination #如果在settings中定义的分页器是PageNumberPagination，则可以在这里更改分页器的种类，允许前端可以按要求选择分页几条
    
class ProductListByCategoryView(generics.ListAPIView):
    '''
    产品按类别筛选列表
    '''
    serializer_class = ProductListSerializer
    permission_classes = (permissions.AllowAny,)
    filter_backends = (SearchFilter, OrderingFilter)
    ordering_fields = ('category', 'manufacturer', 'created', 'sold', 'storage', 'price',)
    ordering = ('id',)
    def get_queryset(self):
        '''
        重写query_set方法，用于替换上面类的queryset变量
        '''
        category = self.request.query_params.get('category', None) #取请求的查询参数category，没有就设为None
        if category is not None:
            queryset = Product.objects.filter(category=category)
        else:
            queryset =Product.objects.all()
        return queryset

class ProductListByCategoryManufacturerView(generics.ListAPIView):
    '''
    产品按类别和生产厂商筛选列表
    '''
    serializer_class = ProductListSerializer
    permission_classes = (permissions.AllowAny,)
    filter_backends = (SearchFilter, OrderingFilter)
    ordering_fields = ('category', 'manufacturer', 'created', 'sold', 'storage', 'price',)
    ordering = ('id',)
    def get_queryset(self):
        '''
        重写query_set方法，用于替换上面类的queryset变量
        '''
        category = self.request.query_params.get('category', None) #取请求的查询参数category，没有就设为None
        manufacturer = self.request.query_params.get('manufacturer', None)
        if category is not None:
            queryset = Product.objects.filter(category=category, manufacturer=manufacturer)
        else:
            queryset =Product.objects.all()
        return queryset

class ProductRetrieveView(generics.RetrieveAPIView):
    '''
    产品详情
    '''
    queryset = Product.objects.all()
    serializer_class = ProductRetrieveSerializer
    permission_classes = (permissions.AllowAny,)

#用户模块
class UserInfoView(APIView): #使用了第三级的APIView，为了只能查看自己的用户信息，不能通过输入id的方式获取其他人的用户信息
    '''
    用户基本信息
    '''
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request, format=None):
        user = self.request.user #只能把当前登录用户的user字段存起来，避免冒充漏洞
        serializer = UserInfoSerializer(user)
        return Response(serializer.data)

class UserProfileRUView(generics.RetrieveUpdateAPIView):
    '''用户其他信息'''
    serializer_class = UserProfileSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        user = self.request.user
        obj =UserProfile.objects.get(user=user)
        return obj

class UserCreateView(generics.CreateAPIView):
    '''创建用户'''
    serializer_class = UserSerializer

class DeliveryAddressLCView(generics.ListCreateAPIView):
    '''
    收货地址LC
    '''
    serializer_class = DeliveryAddressSerilizer
    permission_classes = (permissions.IsAuthenticated,)
    def get_queryset(self):
        user = self.request.user
        queryset = DeliveryAddress.objects.filter(user=user)
        return queryset
    def perform_create(self, serializer): #传入当前对象的序列器
        user = self.request.user
        s = serializer.save(user=user) #保存为当前用户
        profile = user  #profile_of在models中的user的related_name,用于反向查询
        profile.delivery_address = s
        profile.save()
    
class DeliveryAddressRUDView(generics.RetrieveUpdateDestroyAPIView):
    '''
    收货地址的RUD
    '''
    serializer_class = DeliveryAddressSerilizer
    permission_classes = (permissions.IsAuthenticated,)
    def get_object(self):
        '''
        Retrieve
        '''
        user = self.request.user
        # obj = DeliveryAddress.objects.get(user=user) #只能查当前用户的收货地址
        #
        try:
            obj = DeliveryAddress.objects.get(id=self.kwargs['pk'], user=user)
        except Exception as e:
            raise NotFound('not found')
        return obj

