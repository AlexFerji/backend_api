from rest_framework import serializers
from star_ratings.models import Rating

from .models import Image, Category


class RatingObjectRelatedField(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['count', 'average', 'total']

    def create(self, validated_data):
        return Rating.objects.create(**validated_data)


class ImagePostSerializer(serializers.ModelSerializer):
    image_id = serializers.ReadOnlyField(label='ID', read_only=True)
    author = serializers.CharField(max_length=100, read_only=True)
    title = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=100)
    category = serializers.SlugRelatedField(slug_field='name', queryset=Category.objects)
    cover = serializers.ImageField()
    ratings = RatingObjectRelatedField(many=True, read_only=True)

    class Meta:
        model = Image
        fields = ('image_id', 'author', 'title', 'description', 'category', 'cover', 'ratings')



    def create(self, validated_data):
        image = Image.objects.create(**validated_data)
        image.save()
        Rating.objects.create(content_type_id=16, object_id=image.image_id)

        return image


class ImageSerializer(serializers.ModelSerializer):
    author = serializers.CharField(max_length=40, read_only=True)
    title = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=150)
    cover = serializers.ImageField(max_length=None, allow_empty_file=False, use_url=True, read_only=True)
    category = serializers.ReadOnlyField(source='category.name')
    user = serializers.EmailField(read_only=True)
    ratings = RatingObjectRelatedField(many=True, read_only=True)

    class Meta:
        model = Image
        fields = "__all__"



    def get_image_url(self, obj):
        request = self.context.get("request")
        return request.build_absolute_uri(obj.cover.url)
