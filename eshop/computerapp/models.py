from django.db import models

# Create your models here.
from django.utils.six import python_2_unicode_compatible #这个装饰器是为了保证代码在python2中的兼容性，不用管
from django.conf import settings

@python_2_unicode_compatible
class Category(models.Model):
    '''
    商品类别：笔记本、电脑、一体机、台式机、服务器等
    '''
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True) #参数是创建对象时当时的时间
    updated = models.DateTimeField(auto_now=True) #参数是记录修改时的时间
    def __str__(self):
        return self.name

@python_2_unicode_compatible
class Manufacturer(models.Model):
    '''
    生产厂商
    '''
    name = models.CharField(max_length=200)
    description = models.TextField()
    logo = models.ImageField(blank=True, null=True, max_length=200, upload_to='manufacturer/uoloads/%Y/%m/%d/')
    created = models.DateTimeField(auto_now_add=True) #参数是创建时当时的时间
    updated = models.DateTimeField(auto_now=True) #参数是记录修改时的时间
    def __str__(self):
        return self.name

@python_2_unicode_compatible
class Product(models.Model):
    '''
    产品
    '''
    model = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    storage = models.PositiveIntegerField(default=0)
    sold = models.PositiveIntegerField(default=0)
    image = models.ImageField(max_length=200, upload_to='product/uploads/%Y/%m/%d/')
    category = models.ForeignKey(Category, related_name='product_in_category', on_delete=models.CASCADE)
    manufacturer = models.ForeignKey(Manufacturer, related_name='product_of_manufacturer', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True) #参数是创建时当时的时间
    updated = models.DateTimeField(auto_now=True) #参数是记录修改时的时间
    def __str__(self):
        return self.model

@python_2_unicode_compatible
class DeliveryAddress(models.Model):
    '''
    收货地址
    '''
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='delivery_address_of_user')
    contact_person = models.CharField(max_length=200)
    contact_mobile_number = models.CharField(max_length=200)
    delivery_address = models.TextField()
    created = models.DateTimeField(auto_now_add=True) #参数是创建时当时的时间
    updated = models.DateTimeField(auto_now=True) #参数是记录修改时的时间
    def __str__(self):
        return self.delivery_address
    
@python_2_unicode_compatible
class UserProfile(models.Model):
    '''
    用户档案
    '''
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile_of')
    #settings.AUTH_USER_MODEL指向的就是django自带的用户表
    mobile_number = models.CharField(blank=True, null=True, max_length=200)
    nickname = models.CharField(blank=True, null=True, max_length=200)
    description = models.TextField(blank=True, null=True)
    icon = models.ImageField(blank=True, null=True, max_length=200,upload_to='user/uploads/%Y/%m/%d/')
    delivery_address = models.ForeignKey(DeliveryAddress, related_name='user_default_address',on_delete=models.CASCADE,blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True) #参数是创建时当时的时间
    updated = models.DateTimeField(auto_now=True) #参数是记录修改时的时间
    def __str__(self):
        return self.delivery_address

@python_2_unicode_compatible
class Order(models.Model):
    '''
    订单，
    '''
    #通过如下的状态节点实现购物车
    STATUS_CHOICES = ( 
        ('0', 'new'), #新订单，前面是存在数据库的数据，后面是描述
        ('1', 'not paid'), #未支付订单
        ('2', 'paid'), #已支付订单
        ('3', 'transport'), #运输中订单
        ('4', 'closed'), #已完成订单
    )
    status = models.CharField(choices=STATUS_CHOICES, default='0', max_length=2) #choices参数限定住字段的可能值
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='order_of_user')
    remark = models.TextField(blank=True, null=True) #订单备注
    product = models.ForeignKey(Product, related_name='order_product', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    address = models.ForeignKey(DeliveryAddress, related_name='order_address', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True) #参数是创建时当时的时间
    updated = models.DateTimeField(auto_now=True) #参数是记录修改时的时间
    def __str__(self):
        return 'order of %d' % (self.user.id)