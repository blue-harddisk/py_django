import json
from datetime import datetime

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View
from rest_framework import status
from rest_framework.generics import GenericAPIView, ListAPIView, RetrieveAPIView
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from users.decorators import check_ip
from users.models import BookInfo
from users.serializers import BookInfoSerializer


def index(request):
    """访问首页的视图"""
    print("==index==")
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


# 方式三
# class CheckIpMixin(object):
#     """
#     Mixin: 封装(扩展)了一个功能: 检测ip黑名单
#     """
#     @method_decorator(check_ip)
#     def dispatch(self, request, *args, **kwargs):
#         # 调用View的dispatch
#         return super().dispatch(request, *args, **kwargs)
#
# class PostView(CheckIpMixin, View):
#
#     # # 方式一
#     # @method_decorator(check_ip)
#     def get(self, request):
#         """get请求： 显示发帖界面"""
#         return render(request, 'users/post_view.html')
#
#     def post(self, request):
#         """post请求： 执行发帖操作"""
#         # 代码简略
#         return HttpResponse('执行发帖操作')


# 方式二
# @method_decorator(check_ip, name='get')  # 为特定的请求方法添加
# @method_decorator(check_ip, name='dispatch')    # 为所有的请求方法添加
class PostView(View):

    # 给所有的http方法都添加装饰器
    # @method_decorator(check_ip)
    # def dispatch(self, request, *args, **kwargs):
    #     return super().dispatch(request, *args, **kwargs)

    # # 方式一
    # @method_decorator(check_ip)
    def get(self, request):
        """get请求： 显示发帖界面"""
        return render(request, 'users/post_view.html')

    def post(self, request):
        """post请求： 执行发帖操作"""
        # 代码简略
        return HttpResponse('执行发帖操作')


class BooksAPIView(View):

    def get(self, request):
        """
            查询所有图书.增加图书
            路由：GET /books/
        """
        qs = BookInfo.objects.all()
        book_list = []
        for book in qs:
            book_list.append({
                'id':book.id,
                'btitle':book.btitle,
                'bpub_date':book.bpub_date,
                'bread':book.bread,
                'bcomment':book.bcomment,
                "bimage": book.bimage.path if book.bimage else ""

            })

        return JsonResponse(book_list,safe=False)

    def post(self, request):
        """
        新增图书
        路由:POST /books/
        """
        json_byt = request.body
        json_str = json_byt.decode()
        book_dic = json.loads(json_str)

        # 此处详细的校验参数
        book = BookInfo.objects.create(
            btitle= book_dic.get('btitle'),
            bpub_date = datetime.strptime(book_dic.get('bpub_date'), '%Y-%m-%d').date(),
            bread = book_dic.get("bread"),
            bcomment = book_dic.get("bcomment")

        )

        return JsonResponse({
            'id': book.id,
            'btitle': book.btitle,
            'bpub_date': book.bpub_date,
            'bread': book.bread,
            'bcomment': book.bcomment,
        }, status=201)


class BookAPIView(View):

    def get(self, request, pk):
        """
        获取单本图书
        pk: 查询字符串,参数,书本id
        路由： GET  /books/<pk>/
        """
        try:
            book = BookInfo.objects.get(pk = pk)
        except BookInfo.DoesNotExist:
            return HttpResponse(status=404)

        return JsonResponse({
            'id': book.id,
            'btitle': book.btitle,
            'bpub_date': book.bpub_date,
            'bread': book.bread,
            'bcomment': book.bcomment,
            "bimage": book.bimage.url if book.bimage else ""
        })

    def put(self, request, pk):
        """
        修改一本书
        路由： PUT  /books/<pk>
        """

        json_byt = request.body
        json_str = json_byt.decode()
        book_dic = json.loads(json_str)

        try:
            book = BookInfo.objects.get(pk = pk)
        except BookInfo.DoesNotExist:
            return HttpResponse(status=404)

        # 此处详细的校验参数省略

        book.btitle = book_dic.get('btitle', book.btitle)
        book.bpub_date = datetime.strptime(book_dic.get('bpub_date', book.bpub_date), '%Y-%m-%d').date()
        book.bread = book_dic.get("bread", book.bread)
        book.bcomment = book_dic.get("bcomment", book.bcomment)
        book.save()

        return JsonResponse({
            'id': book.id,
            'btitle': book.btitle,
            'bpub_date': book.bpub_date,
            'bread': book.bread,
            'bcomment': book.bcomment,
        })

    def delete(self, request, pk):
        """
        删除一本书
        路由： DELETE /books/<pk>/
        """
        try:
            book = BookInfo.objects.get(pk = pk)
        except BookInfo.DoesNotExist:
            return HttpResponse(status=404)

        book.delete()
        return HttpResponse(status=204)


# class BookInfoViewSet(ModelViewSet):
#     queryset = BookInfo.objects.all()
#     serializer_class = BookInfoSerializer

"""使用rest_framework提供的APIView视图"""
# class BooksInfoAPIView(APIView):
#     """
#      获取所有图书
#      GET  /books/
#
#     """
#     def get(self, request):
#         books = BookInfo.objects.all()
#         serializer = BookInfoSerializer(books, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)


# class BookInfoAPIView(APIView):
#     """
#          获取一本图书
#          GET  /books/<pk>
#
#         """
#     def get(self,request,pk):
#         """
#         获取一本图书
#         GET  /books/<pk>
#         """
#         # 获取图书对象
#         book = BookInfo.objects.get(pk=pk)
#         # 序列化
#         serializer = BookInfoSerializer(book)
#
#         # 响应数据
#         return Response(serializer.data, status=status.HTTP_200_OK)

"""使用GenericAPIView实现API接口"""
# class BookInfoAPIView(GenericAPIView):
#     """
#       获取一本图书
#       GET  /books/<pk>
#
#     """
#     queryset = BookInfo.objects.all()
#     serializer_class = BookInfoSerializer
#
#     def get(self, request, pk):
#         book = self.get_object()
#         serializer = self.get_serializer(book)
#         return Response(serializer.data)


"""使用GenericAPIView和视图扩展类实现API接口"""
# class BooksInfoAPIView(ListModelMixin, GenericAPIView):
#     queryset = BookInfo.objects.all()
#     serializer_class = BookInfoSerializer
#
#     def get(self, request):
#         """获取所有图书"""
#         return self.list(request)
#
# class BookInfoAPIView(RetrieveModelMixin, GenericAPIView):
#     queryset = BookInfo.objects.all()
#     serializer_class = BookInfoSerializer
#
#     def get(self, request, pk):
#         """获取一本图书"""
#         return self.retrieve(request)


"""GenericAPIView的子视图类"""
class BooksInfoAPIView(ListAPIView):
#     """获取所有数据"""
    queryset = BookInfo.objects.all()
    serializer_class = BookInfoSerializer


class BookInfoAPIView(RetrieveAPIView):
    """获取一条数据"""
    queryset = BookInfo.objects.all()
    serializer_class = BookInfoSerializer