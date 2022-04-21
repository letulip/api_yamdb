from django.db.models import Avg

from rest_framework import serializers

from reviews.models import Category, Genre, Title, Review, Comment


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        exclude = ('id',)
        model = Category


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        exclude = ('id',)
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(
        read_only=True,
        many=True
    )
    rating = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category'
        )

    def get_rating(self, obj):
        rate = Review.objects.filter(title_id=obj.id).aggregate(Avg('score'))
        for rating in rate.values():
            if rating:
                return int(rating)


class TitlePostSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field="slug",
        many=True,
        queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field="slug",
        many=False,
        queryset=Category.objects.all()
    )

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'description',
            'genre',
            'category'
        )


class ReviewSerializer(serializers.ModelSerializer):

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )
    # title = serializers.PrimaryKeyRelatedField(
    #     read_only=True,
    #     default=TitleSerializer()
    # )

    class Meta:
        # exclude = ('id',)
        fields = (
            'id',
            'text',
            'author',
            'score',
            'pub_date',
            # 'title'
        )
        model = Review


# class RatingSerializer(serializers.ModelSerializer):
#
#    class Meta:
#        fields = '__all__'
#        model = Rating


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Comment
