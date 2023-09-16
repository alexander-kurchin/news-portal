from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import m2m_changed, pre_save
from django.dispatch import receiver
from django.template.loader import render_to_string

from .models import Post


# TODO: При m2m_changed и 'post_add' возможна повторная отправка
# при добавлении в существующий пост новой категории
@receiver(m2m_changed, sender=Post.category.through)
def notify_subscribers(sender, instance, action, **kwargs):
    """
    Если пользователь подписан на какую-либо категорию, то, как только в неё
    добавляется новая статья, её краткое содержание приходит пользователю на
    электронную почту, которую он указал при регистрации
    """

    if action == 'post_add':
        subscribers = set()
        [subscribers.update(set(category.subscribers.all())) for category in instance.category.all()]
        for user in subscribers:
            text_content = (f'Здравствуй, @{str(user)}. '
                            f'Новая статья в твоём любимом разделе!\n'
                            f'{instance.title}\n{instance.text[:50]}\n'
                            f'http://127.0.0.1:8000{instance.get_absolute_url()}')
            html_content = render_to_string('email/new_post.html',
                                            {'post': instance, 'user': user})
            email = EmailMultiAlternatives(subject=instance.title,
                                           body=text_content,
                                           to=(user.email,))
            email.attach_alternative(html_content, 'text/html')
            email.send()


@receiver(pre_save, sender=Post)
def posting_day_limit(sender, instance, raw, **kwargs):
    """Один пользователь не может публиковать более трёх новостей в сутки"""

    pass  # TODO !
