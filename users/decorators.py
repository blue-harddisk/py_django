from django.http.response import HttpResponse


def check_ip(view_fun):
    """装饰器: 检测ip是否为黑名单,如果是, 禁止访问发帖界面"""

    def wrapper(request, *args, **kwargs):
        # 新增额外操作:ip是否为黑名单
        ip = request.META.get('REMOTE_ADDR')
        if ip in ['192.168.41.1']:
            return HttpResponse('禁止访问')

        return view_fun(request, *args, **kwargs)

    return wrapper
