from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import AnonymousUser
from django.http import JsonResponse, HttpResponse, QueryDict
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from .tasks import send_verify_mail
from .my_util import get_unique_str,get_cart_money
from .models import *
from django.core.cache import caches
# Create your views here.
# 获得缓存
cache = caches['confirm']
def home(req):
    wheels = Wheel.objects.all()
    menus = Nav.objects.all()
    mustbuy = MustBuy.objects.all()
    shops = Shop.objects.all()
    mainshows = MainShop.objects.all()
    result = {
        "title":"首页",
        "wheels":wheels,
        "menus":menus,
        "mustbuy":mustbuy,
        "shop0":shops[0],
        "shop1_3":shops[1:3],
        "shop3_7":shops[3:7],
        "shop_last":shops[7:],
        "mainshows":mainshows
    }
    return render(req,'home/home.html',result)

def market(req):
    return redirect(reverse("app:market_params",args=("104749","0",0)))

def market_with_params(req,type_id,sub_type_id,order_type):
    # 获取所有的一级分类
    types = FoodTypes.objects.all()
    # 获取二级分类数据
    current_cate = types.filter(typeid=type_id)[0]
    childtypenames = current_cate.childtypenames.split("#")
    # sub_types = []
    # for i in childtypenames:
    #     i.split(':')
    #     sub_types.append(tmp)
    sub_types = [i.split(':') for i in childtypenames]
    # 根据typeid搜索商品信息
    goods = Goods.objects.filter(
        categoryid=int(type_id)
    )
    # 根据二级分类的id查询商品的数据
    if sub_type_id == "0":
        pass
    else:
        goods = goods.filter(childcid=int(sub_type_id))
        # 添加num属性
        # 知道以后购物车商品里对应的数量
    user = req.user
    if isinstance(user,MyUser):
        temp_dict={}
    #     去购物车查数据
        cart_nums = Cart.objects.filter(user=user)
        for i in cart_nums:
            temp_dict[i.goods.id]=i.num
            print(temp_dict)
        for i in goods:
            # 添加商品数量
            i.num = temp_dict.get(i.id) if temp_dict.get(i.id) else 0
    # 排序
        '''
        0不
        1价格
        2销量
        '''
        NO_SORT = 0
        PRICR_SORT = 1
        SALES_SORT = 2
        if int(order_type) == 0:
            pass
        elif int(order_type) == 1:
            goods = goods.order_by("price")
        else:
            goods = goods.order_by("productnum")
    result = {
        "title": "闪购",
        "types": types,
        "goods":goods,
        "current_type_id":type_id,
        "sub_types":sub_types,
        "current_sub_type_id":sub_type_id,
        "order_type":int(order_type)
    }
    return render(req, "market/market.html", result)

@login_required(login_url="/app/login")
def cart(req):
    user = req.user
    # 根据用户去购物车数据表搜索该用户的数据
    data =  Cart.objects.filter(user_id=user.id)
    # 算钱
    sum_money = get_cart_money(data)
    # 判断全选按钮的状态(有购物车商品 并且 没有 未被选中的商品
    if data.exists() and not data.filter(is_selected=False).exists():
        is_all_select = True
    else:
        is_all_select = False
    result = {
        "title": "购物车",
        "uname":user.username,
        "phone":user.phone if user.phone else "暂无",
        "address":user.address if user.address else "暂无",
        "cart_items":data,
        "sum_money":sum_money,
        "is_all_select":is_all_select
    }
    return render(req,"cart/cart.html",result)

# 帮我们检查用户是不是登录了
# @login_required(login_url="/axf/login")
def mine(req):
    btns = MinBtns.objects.filter(is_used=True)
    # 拿当前的用户
    user = req.user
    is_login = True
    if isinstance(user, AnonymousUser):
        is_login = False
    u_name = user.username if is_login else ""
    icon = "http://" + req.get_host() + "/static/uploads/" + user.icon.url if is_login else ""
    result = {
        "title": "我的",
        "btns": btns,
        "is_login": is_login,
        "u_name": u_name,
        "icon": icon
    }
    return render(req, "mine/mine.html", result)

class RegisterAPI(View):
    def get(self,req):
        return render(req,"user/register.html")

    def post(self,req):
        #解析参数
        params = req.POST
        icon = req.FILES.get("u_icon")
        name = params.get("u_name")
        pwd = params.get("u_pwd")

        confirm_pwd = params.get("u_confirm_pwd")
        email = params.get("email")
        # 校验密码
        if pwd and confirm_pwd and pwd==confirm_pwd:
            #判断用户名是否可用
            if MyUser.objects.filter(username=name).exists():
                return render(req,"user/register.html",{"help_msg":"该用户已经存在"})
            else:
                user =  MyUser.objects.create_user(
                    username=name,
                    password=pwd,
                    email=email,
                    is_active=False,
                    icon=icon
                )
                # 生成验证链接
                url = "http://" + req.get_host() +"/app/confirm/" + get_unique_str()
                # 发送邮件 异步调用
                send_verify_mail.delay(url,user.id,email)
                # 设置缓存 返回登录页面
                return render(req,"user/login.html")

class LoginAPI(View):
    def get(self,req):
        return render(req,'user/login.html')
    def post(self,req):
#             解析参数
        params =req.POST
        name = params.get("name")
        pwd = params.get("pwd")
        # print(name,pwd)

        if not name or not pwd:
            data = {
                "code":2,
                "msg":"账号和密码不能为空",
                "data":""
            }
            return JsonResponse(data)
#             使用用户名密码校验用户
        user = authenticate(username=name,password=pwd)
#             校验数据
# 如果校验成功就登录
#         print(user)
        if user:
            login(req,user)
            data = {
                'code':1,
                'msg':"ok",
                "data":"/app/mine"
            }
            return JsonResponse(data)
# 失败的话就返回错误提示
        else:
            data = {
                "code":3,
                "msg":"账号或者密码错误",
                "data":""
            }
            return JsonResponse(data)

class LogoutAPI(View):
    def get(self,req):
        # 调用了系统的logout函数
        logout(req)
        return redirect('/app/mine')

# 确认
def confirm(req,uuid_str):
    #1去缓存拿一下数据
    user_id = cache.get(uuid_str)
    print(uuid_str)
    print(user_id)
    #2如果拿到，修改is_active字段
    if user_id:
        user = MyUser.objects.get(pk=int(user_id))
        # is_active通常是指对象是否激活、启用、可用、正常状态
        user.is_active = True
        user.save()
        return redirect("/app/login")
        #3如果没拿到，就返回验证失败
    else:
        return HttpResponse("<h2>链接失效</h2>")

class CartStatusAPI(View):
    def patch(self,req):
        params = QueryDict(req.body)
        c_id = int(params.get("c_id"))
        user = req.user
        # 先拿到跟这个人有关的购物车数据
        cart_items = Cart.objects.filter(user_id=user.id)
        #拿到c_id对应的数据
        cart_data = cart_items.get(id=c_id)
        #状态修改
        cart_data.is_selected = not cart_data.is_selected
        cart_data.save()
        #算钱
        sum_money = get_cart_money(cart_items)
        #判断是否全选
        if cart_items.filter(is_selected=False).exists():
            is_all_select = False
        else:
            is_all_select = True
        #返回数据
        result = {
            "code":1,
            "msg":"ok",
            "data":{
                "is_select_all":is_all_select,
                "sum_money":sum_money,
                "status":cart_data.is_selected
            }
        }
        return JsonResponse(result)

class CartAllStatusAPI(View):
    def put(self,req):
        user = req.user
        # 判断操作
        cart_items = Cart.objects.filter(user_id=user.id)
        is_select_all=False
        # 由于当前处如未选中的状态，那么我们要将所有未选中商品的状态取反
        if cart_items.exists() and cart_items.filter(is_selected=False).exists():
            is_select_all = True
            # for i in cart_items.filter(is_selected=False):
            #     i.is_selected = True
            #     i.save()
            cart_items.filter(is_selected=False).update(is_selected=True)
            # is_select_all = True
            # 算钱
            sum_money = get_cart_money(cart_items)
        else:
            # 将所有选中的商品状态取反
            cart_items.update(is_selected=False)
            # 由于是全不选的状态
            sum_money = 0

        result={
            "code":1,
            "msg":"ok",
            "data":{
                "sum_money":sum_money,
                "all_select":is_select_all
            }
        }
        return JsonResponse(result)

def check_uname(req):
    uname = req.GET.get("uname")
#     判断数据不能是空白，然后去搜索用户
    data = {
        "code": 1,
        "data": ""
        }
    if uname and len(uname)>=3:
        if MyUser.objects.filter(username=uname).exists():
            data["msg"]="账号已经存在"
        else:
            data["msg"]="ok"
    else:
        data["msg"]="用户名过短"
    return JsonResponse(data)

class CartAPI(View):
    def post(self,req):
        # 先看用户是否登录
        user = req.user
        # 如果user是MyUser类的一个实例，说明该用户登录
        if not isinstance(user,MyUser):
            data={
                "code":2,
                "msg":"not login",
                "data":"/app/login"
            }
            return JsonResponse(data)
#        拿参数
        op_type = req.POST.get("type")
        g_id = int(req.POST.get("g_id"))
        # 先获取商品数据
        goods= Goods.objects.get(pk=g_id)

        if op_type =="add":
#             添加购物车的操作
            goods_num = 1
            if goods.storenums>1:
                cart_goods = Cart.objects.filter(
                    user=user,
                    goods=goods
                )
                if cart_goods.exists():
                # 不是第一次添加
                    cart_item = cart_goods.first()
                #原来的基础上加一
                    cart_item.num = cart_item.num+1
                    cart_item.save()
                #返回修改数量
                    goods_num = cart_item.num
                # 是第一次添加
                else:
                    #创建购物车数据
                    Cart.objects.create(
                        user=user,
                        goods=goods
                    )
                data={
                    "code":1,
                    "msg":"ok",
                    "data":goods_num
                    }
                return JsonResponse(data)
            else:
                data={
                    "code":3,
                    "msg":"库存不足",
                    "data":""
                }
                return JsonResponse(data)

        elif op_type == "sub":
            goods_num = 0
#             先去购物车拿数据
            cart_item = Cart.objects.get(
                user = user,
                goods = goods
            )
            cart_item.num-=1
            cart_item.save()
            if cart_item == 0:
                cart_item.delete()
            else:goods_num = cart_item.num
            data={
                "code":1,
                "msg":"ok",
                "data":goods_num

            }
            return JsonResponse(data)

class CartItemAPI(View):
    def post(self,req):
        user = req.user
        c_id = req.POST.get("c_id")
        # 确认购物车数据
        cart_item = Cart.objects.get(id=int(c_id))
        # 检查库存
        if cart_item.goods.storenums<1:
            data = {
                "code":2,
                "msg":"库存不足",
                "data":""
            }
            return JsonResponse(data)
        # 给商品的数量在原来的基础上加一
        cart_item.num+=1
        cart_item.save()
        # 算钱
        cart_items = Cart.objects.filter(
            user_id=user.id,is_selected=True
        )
        sum_money = get_cart_money(cart_items)
        # 返回数据
        data = {
            "code":1,
            "msg":"ok",
            "data":{
                "num":cart_item.num,
               "sum_money":sum_money
            }
        }
        return JsonResponse(data)

    def delete(self,req):
        # 用户
        user = req.user
        # 购物车商品
        c_id = QueryDict(req.body).get("c_id")
        cart_item = Cart.objects.get(pk=int(c_id))
        cart_item.num-=1
        cart_item.save()
        # 判断是不是减到0
        if cart_item.num == 0:
            goods_num = 0
            cart_item.delete()
        else:
            goods_num = cart_item.num
        # 算钱
        cart_items = Cart.objects.filter(
            user=user,
            is_selected=True
        )
        sum_money = get_cart_money(cart_items)
        data = {
            "code":1,
            "msg":"ok",
            "data":{
                "num":goods_num,
                "sum_money":sum_money
            }
        }
        return  JsonResponse(data)

# 订单
class OrderAPI(View):
    def get(self,req):
        user = req.user
        # 获取购物车里的数据
        cart_items = Cart.objects.filter(
            user_id=user.id,
            is_selected=True
        )
        if not cart_items.exists():
            return render(req, "order/order_detail.html")
        # 创建订单
        order = Order.objects.create(
            user=user
        )
        # 循环创建我们的订单数据
        for i in cart_items:
            OrderItem.objects.create(
                order=order,
                goods=i.goods,
                num=i.num,
                buy_money = i.goods.price
            )
        # 算钱
        sum_money = get_cart_money(cart_items)
        # 清空购物车内的商品
        cart_items.delete()
        data={
            "sum_money":sum_money,
            "order":order
        }
        return render(req,"order/order_detail.html",data)





















