from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class MyUser(AbstractUser):
    email = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="邮箱"
    )
    address = models.CharField(
        max_length=251,
        verbose_name="地址",
        null=True
    )
    phone = models.CharField(
        max_length=13,
        verbose_name="电话",
        null=True
    )
    icon = models.ImageField(
        default=True,
        verbose_name="头像"
    )

class BaseDate(models.Model):
    img = models.CharField(
        max_length=251
    )
    name = models.CharField(
        max_length=40
    )
    trackid = models.CharField(
        max_length=30
    )
    class Meta:
        abstract=True
class Wheel(BaseDate):
    class Meta:
        db_table ="axf_wheel"

class Nav(BaseDate):
    class Meta:
        db_table = 'axf_nav'

class MustBuy(BaseDate):
    class Meta:
        db_table = 'axf_mustbuy'

class Shop(BaseDate):
    class Meta:
        db_table = "axf_shop"

class MainShop(BaseDate):

    categoryid = models.CharField(
        max_length=100
    )
    brandname = models.CharField(
        max_length=100
    )

    img1 = models.CharField(
        max_length=255
    )
    childcid1 = models.CharField(
        max_length=100
    )
    productid1 = models.CharField(
        max_length=100
    )
    longname1 = models.CharField(
        max_length=100
    )
    price1 = models.CharField(
        max_length=100
    )
    marketprice1 = models.CharField(
        max_length=100
    )

    img2 = models.CharField(
        max_length=255
    )
    childcid2 = models.CharField(
        max_length=100
    )
    productid2 = models.CharField(
        max_length=100
    )
    longname2 = models.CharField(
        max_length=100
    )
    price2 = models.CharField(
        max_length=100
    )
    marketprice2 = models.CharField(
        max_length=100
    )
    img3 = models.CharField(
        max_length=255
    )
    childcid3 = models.CharField(
        max_length=100
    )
    productid3 = models.CharField(
        max_length=100
    )
    longname3 = models.CharField(
        max_length=100
    )
    price3 = models.CharField(
        max_length=100
    )
    marketprice3 = models.CharField(
        max_length=100
    )

    class Meta:
        db_table = "axf_mainshow"

class FoodTypes(models.Model):

    typeid = models.CharField(
        max_length=20

    )
    typename = models.CharField(
        max_length=30
    )
    childtypenames = models.CharField(
        max_length=255
    )
    typesort = models.IntegerField(

    )
    class Meta:
        db_table = "axf_foodtypes"




class Goods(models.Model):
    productid = models.CharField(
        max_length=20
    )
    productimg = models.CharField(
        max_length=255
    )
    productname = models.CharField(
        max_length=255
    )
    productlongname = models.CharField(
        max_length=190
    )
    isxf = models.BooleanField(
        default=0
    )
    pmdesc = models.IntegerField()
    specifics = models.CharField(
        max_length=40
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    marketprice = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    categoryid = models.IntegerField()
    childcid = models.IntegerField()

    childcidname = models.CharField(
        max_length=30
    )
    dealerid = models.CharField(
        max_length=30
    )
    storenums = models.IntegerField(
        verbose_name="库存"
    )
    productnum = models.IntegerField(
        verbose_name="销量"
    )

    class Meta:
        db_table = "axf_goods"

# 购物车模型
class Cart(models.Model):
    user = models.ForeignKey(
        MyUser
    )
    goods = models.ForeignKey(
        Goods
    )
    create_time = models.DateTimeField(
        auto_now=True
    )
    update_time = models.BooleanField(
        default=True
    )
    is_selected = models.BooleanField(
        default=True
    )
    num = models.IntegerField(
        default=1
    )
    class Meta:
        verbose_name="购物车"
        # 联合索引
        index_together = ["user","goods"]
class MinBtns(models.Model):
    btn = models.CharField(
        max_length=30

    )
    class_name = models.CharField(
        max_length=100
    )
    bref_url = models.CharField(
        max_length=255,
        null = True
    )
    # ·true/false 字段，此字段的默认表单控制是CheckboxInput
    is_used = models.BooleanField(
        # 默认值
        default=True,
        verbose_name="正在用"

    )
    class Meta:
        verbose_name = "按钮"

class Order(models.Model):
    ORDER_STATUS = (
        (1,"待付款"),
        (2,"已付款"),
        (3,"已发货"),
        (4,"已收货"),
        (5,"待评价"),
        (6,"已评价")
    )
    user = models.ForeignKey(
        MyUser
    )
    cerate_time = models.DateTimeField(
        auto_now_add=True
    )
    status = models.IntegerField(
        choices= ORDER_STATUS,
        default=1
    )


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order
    )
    goods = models.ForeignKey(
        Goods
    )
    num = models.IntegerField(
        verbose_name="数量"
    )
    # 小数
    buy_money = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )























