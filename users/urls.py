from django.conf.urls import url

from users import views

urlpatterns = [
    # 配置url和视图函数，需要调用url函数，并传入参数
    # 参数1： 匹配url的正则表达式（需要用 ^ 和 $ 匹配开头和结尾）
    # 参数2： url匹配成功执行的视图函数
    url(r'^index/$', views.index),
    # path方法获取请求参数
    url(r'^news/(?P<category>\d+)/(?P<page>\d+)$', views.news),
    # 查询字符串,跟get.post方法没关系
    url(r'^news2', views.news2),
    # post,表单,键值对
    url(r'^news3', views.news3),
    # post,json
    url(r'^news4', views.news4),
    # 请求头
    url(r'^news5', views.news5),

    # response
    url(r'come1', views.come1),
    # 重定向
    url(r'come2', views.come2),

    # cookie
    url(r'^set_cookie$', views.set_cookie),
    url(r'^get_cookie$', views.get_cookie),

    # session
    url(r'^set_session$', views.set_session),
    url(r'^get_session$', views.get_session),

    # as_view
    url(r'^post2$', views.PostView.as_view()),

    # REST
    url(r'^books/$', views.BooksAPIView.as_view()),
    url(r'^books/(?P<pk>\d+)/$', views.BookAPIView.as_view())

]