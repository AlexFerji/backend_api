from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from user.models import CustomUser
from django.contrib.contenttypes.fields import GenericRelation
from star_ratings.models import Rating, AbstractBaseRating
from time import gmtime, strftime


def user_directory_path(instance, filename):
    # Путь куда будет осуществлена загрузка MEDIA_ROOT/user_<id>/filename

    return 'user_{0}/{1}'.format(instance.user.email, filename)


class Category (models.Model):
    name = models.CharField(max_length=64, verbose_name='')

    def __str__(self):
        return '{}'.format(self.name)


class Image(models.Model):
    image_id = models.AutoField(primary_key=True, verbose_name='image_id')
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE, verbose_name="Почта" )
    author = models.CharField(max_length=100, null=True, blank=False, verbose_name='Автору')
    title = models.CharField(max_length=100,  verbose_name="Название")
    description = models.TextField(max_length=150, null=True, verbose_name="Описание")
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    cover = models.ImageField(upload_to=user_directory_path)
    ratings = GenericRelation(Rating, related_query_name='image')

    def __str__(self):
        return '{0} -- {1} ({2}) -- {3}. {4}'.format(
            self.image_id,
            self.user.email,
            self.author,
            self.title,
            self.description,
            self.category.name,
            self.cover.url,
        )


    def save(self, *args, **kwargs):
        self.title += strftime("%Y-%m-%d %H:%M:%S", gmtime())
        super(Image, self).save(*args, **kwargs)