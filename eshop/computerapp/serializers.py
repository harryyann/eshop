from rest_framework import serializers
from .models import Product, Manufacturer, Category, UserProfile, DeliveryAddress, Order
from django.contrib.auth.models import User


#用户模块
class UserProfileSerializer(serializers.ModelSerializer):
    '''
    使用自定义的用户档案表对用户信息进行拓展
    '''
    class Meta:
        model = UserProfile
        fields = ('id', 'user', 'mobile_number', 'nickname', 'description', 'delivery_address', 'icon', 'created', 'updated')
        read_only_fields = ('user', )

class UserInfoSerializer(serializers.ModelSerializer):
    '''
    用户信息序列器
    '''
    profile_of = UserProfileSerializer()
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'date_joined', 'profile_of',)

class UserSerializer(serializers.ModelSerializer):
    '''
    创建用户
    '''
    class Meta:
        model=User
        fields=('id','username','password','email','first_name','last_name',)
        extra_kwargs={'password':{'write_only':True}} #额外的关键字参数：fields中的password只能写入，不能显示
    def create(self, validated_data):
        '''
        在创建一条用户记录的时候执行
        注意：views中的是perform_create()
        '''
        user=User(**validated_data)#接受前端传过来的用户名和密码，已经验证数据会存在validated_data中
        user.set_password(validated_data['password'])#set_password方法会自动对传入的密码进行加密
        user.save() #user对象保存到django的User表
        user_profile=UserProfile(user=user) #将user对象保存到自定义的用户档案表UserProfile中
        user_profile.save()
        return user

class DeliveryAddressSerilizer(serializers.ModelSerializer):
    '''收货地址'''
    class Meta:
        model=DeliveryAddress
        fields=('id','user','contact_person','contact_mobile_number','delivery_address','created','updated',)
        read_only_fields = ('user',)


#产品模块
class ManufacturerSerializer(serializers.ModelSerializer):
    '''
    manufacturer序列器，用于丰富外键的显示内容，不是只显示主键
    '''
    class Meta:
        model = Manufacturer
        fields = ('id', 'name',)


class CategorySerializer(serializers.ModelSerializer):
    '''
    category序列器，用于丰富外键的显示内容，不是只显示主键
    '''
    class Meta:
        model = Category
        fields = ('id', 'name',)


class ProductListSerializer(serializers.ModelSerializer):
    '''
    产品列表序列器
    '''
    class Meta:
        model = Product
        fields = ('id', 'model', 'image', 'price', 'sold', 'category', 'manufacturer', )


class ProductRetrieveSerializer(serializers.ModelSerializer):
    '''
    产品详情序列器
    '''
    manufacturer = ManufacturerSerializer() #设置manufacturer字段显示的是name而不仅是id，初始化ManufacturerSerializer序列器，该序列器显示的是id和name
    category = CategorySerializer()
    class Meta:
        model = Product
        fields = ('id', 'model', 'image', 'price', 'sold', 'category', 'manufacturer', 'description','created','updated',)


#订单模块
class OrderListSerializer(serializers.ModelSerializer):
    product = ProductListSerializer()
    address = DeliveryAddressSerilizer()
    class Meta:
        model=Order 
        fields=('id','status','user','product','price','quantity','remark','address','created','updated',)


class OrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('id', 'status', 'user', 'product', 'price', 'quantity', 'remark', 'address', 'created', 'updated',)
        read_only_fields=('user','price','address',)


