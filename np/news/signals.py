from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import m2m_changed, pre_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from .tasks import notify_subscribers
from .models import Post


# TODO: При m2m_changed и 'post_add' возможна повторная отправка
# сигнала при добавлении в существующий пост новой категории
@receiver(m2m_changed, sender=Post.category.through)
def signal_post_add(sender, instance, action, **kwargs):
    """
    Как только в новом посте появляются категории, запускаем таск
    """

    if action == 'post_add':
        notify_subscribers.apply_async([instance.pk],
                                       expires=432_000)


@receiver(pre_save, sender=Post)
def posting_day_limit(sender, instance, raw, **kwargs):
    """Один пользователь не может публиковать более трёх новостей в сутки"""

    pass  # TODO !
