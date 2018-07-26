from rest_framework import serializers

from users.models import BookInfo, HeroInfo


# 初探drf的魅力
# class BookInfoSerializer(serializers.ModelSerializer):
#     """图书数据序列化器"""
#
#     class Meta:
#         model = BookInfo
#         fields = '__all__'


# # 使用序列化器
# class BookInfoSerializer(serializers.Serializer):
#     """图书数据序列化器"""
#     id = serializers.CharField(label='ID', read_only=True)
#     btitle = serializers.CharField(label='名称', max_length=20)
#     bpub_date = serializers.DateField(label='发布时间', required=False)
#     bread = serializers.IntegerField(label='阅读量', required=False)
#     bcomment = serializers.IntegerField(label='评论量', required=False)
#     bimage = serializers.ImageField(label='图片', required=False)
#     heroinfo_set = serializers.PrimaryKeyRelatedField(read_only=True, many=True)  # 新增
#
#     # def validate_btitle(self, value):
#     #     if 'django' not in value.lower():
#     #         raise serializers.ValidationError("图书不是关于Django的")
#     #     return value
#
#     # def validate(self, attrs):
#     #     bread = attrs.get('bread')
#     #     bcomment = attrs.get('bcomment')
#     #     if bread < bcomment:
#     #         raise serializers.ValidationError('阅读量小于评论量')
#     #     return attrs
#
#     def create(self, validated_data):
#         """新建"""
#         return BookInfo.objects.create(**validated_data)
#
#     def update(self, instance, validated_data):
#         """更新，instance为要更新的对象实例"""
#         instance.btitle = validated_data.get('btitle', instance.btitle)
#         instance.bpub_date = validated_data.get('bpub_date', instance.bpub_date)
#         instance.bread = validated_data.get('bread', instance.bread)
#         instance.bcomment = validated_data.get('bcomment', instance.bcomment)
#         instance.save()
#         return instance
#
# # 使用序列化器
# class HeroInfoSerializer(serializers.Serializer):
#     """英雄数据序列化器"""
#     GENDER_CHOICES = (
#         (0, 'male'),
#         (1, 'female')
#     )
#     id = serializers.IntegerField(label='ID', read_only=True)
#     hname = serializers.CharField(label='名字', max_length=20)
#     hgender = serializers.ChoiceField(label= '性别', choices=GENDER_CHOICES, required=False)
#     hcomment = serializers.CharField(label='描述信息', required=False, max_length=200, allow_null=True)
#     # hbook = serializers.PrimaryKeyRelatedField(label='图书', read_only=True)
#     # hbook = serializers.StringRelatedField(label='图书')
#     # hbook = serializers.HyperlinkedRelatedField(label='图书', read_only=True, view_name='books-detail')  # 暂时还没有定义视图，此方式不再演示。
#     # hbook = serializers.SlugRelatedField(label='图书', read_only=True, slug_field='bpub_date')
#     hbook = BookInfoSerializer()

# 模型类序列化器ModelSerializer

class BookInfoSerializer(serializers.ModelSerializer):
    """图书数据序列化器"""

    class Meta:
        model = BookInfo
        # __all__表名包含所有字段
        fields = '__all__'

        # 使用fields来明确字段
        # fields = ('id', 'btitle', 'bpub_date')

        # 使用exclude可以明确排除掉哪些字段
        # exclude = ('bimage',)

        #
        extra_kwargs = {
            'bread': {'min_value': 0, 'required': True},
            'bcomment': {'min_value': 0, 'required': True}
        }


class HeroInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeroInfo
        # fields = '__all__'
        fields = ('id', 'hname', 'hgender', 'hcomment', 'hbook')

        # read_only_fields指明只读字段，即仅用于序列化输出的字段
        read_only_fields = ('id', 'bread', 'bcomment')

        # 默认ModelSerializer使用主键作为关联字段，但是我们可以使用depth来简单的生成嵌套表示，depth应该是整数，表明嵌套的层级数量
        # depth = 1
