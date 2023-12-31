from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.db import models
from django.db.models import Sum
from django.urls import reverse

User = get_user_model()


class Author(models.Model):
    """Объекты всех авторов"""

    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="author")
    rating = models.IntegerField(default=0)

    def update_rating(self):
        """
        Обновляет рейтинг текущего автора:
        - суммарный рейтинг каждой статьи автора умножается на 3;
        - суммарный рейтинг всех комментариев автора;
        - суммарный рейтинг всех комментариев к статьям автора.
        """
        a = Post.objects.filter(author=self).aggregate(Sum('rating'))
        b = Comment.objects.filter(user=self.user).aggregate(Sum('rating'))
        c = Post.objects.filter(author=self).aggregate(Sum('rating'))
        self.rating = 3*a['rating__sum'] + b['rating__sum'] + c['rating__sum']
        self.save()

    def __str__(self):
        return f"{self.user.first_name} @{self.user.username} {self.user.last_name}"


class Category(models.Model):
    """Категории новостей/статей: (спорт, политика, образование и т.д.)"""

    category = models.CharField(max_length=64, unique=True)
    subscribers = models.ManyToManyField(User, through='CategoryUser')

    class Meta:
        ordering = ['category']

    def __str__(self):
        return self.category


class Post(models.Model):
    """Статьи и новости, которые создают пользователи"""

    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name="author", related_name="posts")
    POST_TYPES = [('article', 'Статья'), ('news', 'Новость')]
    post_type = models.CharField(choices=POST_TYPES, max_length=7, default='article')
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=255)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    class Meta:
        ordering = ['-created_at', 'title']

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):  # TODO: Убрать за ненадобностью
        """Возвращает начало статьи длиной 124 символа и …"""

        return self.text[:124] + "…" if len(self.text) > 124 else self.text[:124]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', args=[self.pk])

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.delete(f'post-{self.pk}')


class PostCategory(models.Model):
    """Промежуточная модель для связи"""

    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name="post", related_name="categories")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, verbose_name="category", null=True, related_name="posts")

    class Meta:
        ordering = ['post']


class CategoryUser(models.Model):
    """Промежуточная модель для связи"""

    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="category")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="user", related_name="categories")


class Comment(models.Model):
    """Комментарии пользователей"""

    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name="post", related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="user", related_name="comments")
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
