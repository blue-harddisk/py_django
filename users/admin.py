from django.contrib import admin
from .models import BookInfo,HeroInfo

class HeroInfoTabularInline(admin.TabularInline):
    model = HeroInfo  # 要编辑的对象
    extra = 1  # 附加编辑的数量


class BookInfoAdmin(admin.ModelAdmin):
    list_per_page = 4
    actions_on_top = True
    actions_on_bottom = True
    list_display = ['id', 'btitle', 'pub_date', 'bcomment']
    # fields = ["btitle", "bpub_date"]
    fieldsets = (
        ('基本', {'fields': ['btitle', 'bpub_date']}),
        ('高级', {
            'fields': ['bread', 'bcomment'],
            'classes': ('collapse',)  # 是否折叠显示
        })
    )
    inlines = [HeroInfoTabularInline]


class HeroInfoAdmin(admin.ModelAdmin):
    list_display = ['id', 'hname', 'hbook', 'read']
    list_filter = ['hbook', 'hgender']
    search_fields = ['hname']


admin.site.register(BookInfo, BookInfoAdmin)
admin.site.register(HeroInfo, HeroInfoAdmin)
admin.site.site_header = '传智书城'
admin.site.site_title = '传智书城MIS'
admin.site.index_title = '欢迎使用传智书城MIS'