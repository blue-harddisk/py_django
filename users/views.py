import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect


# Create your views here.
def index(request):
    """访问首页的视图"""
    return render(request, "users/ThinkPad.html")


def news(request, category, page):
    """接收参数(path)实验"""
    return HttpResponse("显示新闻:%s,%s" % (category, page))


def news2(request):
    """接收参数(查询字符串)实验"""

    category = request.GET.get('category')
    page = request.GET.get('page')
    a = request.GET.getlist('a')

    return HttpResponse("显示新闻:%s,%s<br>a:%s" % (category, page, a))


def news3(request):
    """接收参数(post,表单,键值对)实验"""

    category = request.POST.get('category')
    page = request.POST.get('page')
    a = request.POST.getlist('a')
    return HttpResponse("显示新闻:%s,%s<br>a:%s" % (category, page, a))


def news4(request):
    """接收参数(post,json)实验"""
    # 获取json字符串
    json_byt = request.body
    json_str = json_byt.decode()  # bytes -> str

    # 解析json,转字典
    dict_data = json.loads(json_str)
    category = dict_data.get('category')
    page = dict_data.get('page')

    return HttpResponse("显示新闻:%s,%s" % (category, page))


def news5(request):
    """接收参数(请求头)实验"""

    category = request.META.get('HTTP_CATEGORY')
    page = request.META.get('HTTP_PAGE')
    remote_add = request.META.get("REMOTE_ADDR")
    return HttpResponse("显示新闻:%s,%s,ip:%s" % (category, page, remote_add))


def come1(request):
    """使用响应对象"""
    # response = JsonResponse({'city': 'beijing', 'subject': 'python'})

    # JsonResponse参数是非字典类型的,需要带上safe=False
    response = JsonResponse([{'a': 'xm', 'b': 'ww'}], safe=False)
    return response


def come2(request):
    """重定向"""
    return redirect('/users/index')


def set_cookie(request):
    """保存cookie键值对数据"""
    response = HttpResponse('保存cookie数据成功')
    response.set_cookie('user_id', 5501009171)
    response.set_cookie('user_name', 'loser')
    return response


def get_cookie(request):
    """读取cookie键值对数据"""
    user_id = request.COOKIES.get('user_id')
    user_name = request.COOKIES.get('user_name')
    text = 'user_id = %s, user_name = %s' % (user_id, user_name)
    return HttpResponse(text)


def set_session(request):
    """保存session键值对数据"""
    request.session['user_id'] = 120
    request.session['user_name'] = 'woman'
    return HttpResponse('保存session成功')


def get_session(request):
    """读取session键值对数据"""
    user_id = request.session.get('user_id')
    user_name = request.session.get('user_name')
    text = 'user_id = %s, user_name = %s' % (user_id, user_name)
    return HttpResponse(text)