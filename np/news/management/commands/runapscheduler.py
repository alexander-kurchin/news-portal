import logging
from datetime import datetime, timedelta

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from django_apscheduler import util
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

from news.models import Category, Post


logger = logging.getLogger(__name__)


def weekly_digest():
    """
    Если пользователь подписан на какую-либо категорию, то каждую неделю
    ему приходит на почту список новых статей, появившийся за неделю с
    гиперссылкой на них, чтобы пользователь мог перейти и прочесть
    любую из статей
    """

    logger.info('Starting job: weekly_digest.')
    mailing = dict()
    week_ago = datetime.now() - timedelta(days=7)
    base_url = 'http://127.0.0.1:8000'

    for category in Category.objects.all():
        posts = Post.objects.filter(category=category,
                                    created_at__gte=week_ago)
        if len(posts) != 0:
            for user in category.subscribers.all():
                mailing.setdefault(user, set())
                mailing[user].update(posts)

    for user, posts in mailing.items():
        post_list = '\n'.join([f'{post}: {base_url}{post.get_absolute_url()}' for post in posts])
        text_content = (f'Здравствуй, @{str(user)}. '
                        f'Новое за прошедшую неделю:\n'
                        f'{post_list}')
        html_content = render_to_string('email/weekly_digest.html',
                                        {'posts': posts, 'user': user})
        email = EmailMultiAlternatives(subject='Еженедельный Дайджест',
                                       body=text_content,
                                       to=(user.email,))
        email.attach_alternative(html_content, 'text/html')
        email.send()
    logger.info('Finished job: weekly_digest.')


@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    """
    This job deletes all apscheduler job executions older
    than `max_age` from the database.
    """

    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = 'Runs apscheduler.'

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), 'default')

        scheduler.add_job(
            weekly_digest,
            trigger=CronTrigger(day_of_week='sun'),
            id='weekly_digest',
            max_instances=1,
            replace_existing=True,
        )
        logger.info('Added job: weekly_digest.')

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(day_of_week='mon', hour='00', minute='00'),
            id='delete_old_job_executions',
            max_instances=1,
            replace_existing=True,
        )
        logger.info('Added weekly job: delete_old_job_executions.')

        try:
            logger.info('Starting scheduler...')
            scheduler.start()
        except KeyboardInterrupt:
            logger.info('Stopping scheduler...')
            scheduler.shutdown()
            logger.info('Scheduler shut down successfully!')
