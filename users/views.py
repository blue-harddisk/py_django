from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def index(request):
    """访问首页的视图"""
    return render(request, "users/ThinkPad.html")

def news(request, category, page):
    """接收参数实验"""
    return HttpResponse("显示新闻:%s,%s" %(category, page))
