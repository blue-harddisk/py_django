import json

from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def index(request):
    """访问首页的视图"""
    return render(request, "users/ThinkPad.html")

def news(request, category, page):
    """接收参数(path)实验"""
    return HttpResponse("显示新闻:%s,%s" %(category, page))

def news2(request):
    """接收参数(查询字符串)实验"""

    category = request.GET.get('category')
    page = request.GET.get('page')
    a = request.GET.getlist('a')

    return HttpResponse("显示新闻:%s,%s<br>a:%s" %(category, page, a))

def news3(request):
    """接收参数(post,表单,键值对)实验"""

    category = request.POST.get('category')
    page = request.POST.get('page')
    a = request.POST.getlist('a')

    return HttpResponse("显示新闻:%s,%s<br>a:%s" %(category, page, a))

def news4(request):
    """接收参数(post,json)实验"""
    # 获取json字符串
    json_str = request.body
    json_str = json_str.decode()  # bytes -> str

    # 解析json
    dict_data = json.loads(json_str)
    category = dict_data.get('category')
    page = dict_data.get('page')

    return HttpResponse("显示新闻:%s,%s" %(category, page))


def news5(request):
    """接收参数(请求头)实验"""

    category = request.META.get('HTTP_CATEGORY')
    page = request.META.get('HTTP_PAGE')
    remote_add = request.META.get("REMOTE_ADDR")
    return HttpResponse("显示新闻:%s,%s,ip:%s" %(category, page, remote_add))