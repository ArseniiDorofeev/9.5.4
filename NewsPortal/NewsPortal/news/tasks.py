from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
from .models import Subscriber, News
from django_apscheduler.models import DjangoJob
from apscheduler.schedulers.background import BackgroundScheduler


def send_weekly_newsletter():
    # Определяем даты начала и конца прошлой недели
    today = timezone.now().date()
    last_week_start = today - timedelta(days=today.weekday() + 7)
    last_week_end = today - timedelta(days=today.weekday())

    # Находим новости, добавленные за прошлую неделю
    new_news = News.objects.filter(date_added__gte=last_week_start, date_added__lte=last_week_end)

    if new_news:
        # Получаем список уникальных адресов подписчиков
        subscribers = Subscriber.objects.values_list('email', flat=True).distinct()

        # Собираем текст рассылки
        subject = "Еженедельная рассылка новостей"
        message = "Здравствуйте,\n\n"
        message += "Вот свежие новости, добавленные за прошлую неделю:\n\n"
        for news in new_news:
            message += f"- {news.title}: {news.content[:50]}...\n"
        message += "\nС уважением,\nВаш новостной портал"

        # Отправляем рассылку
        send_mail(subject, message, 'your_email@example.com', subscribers, fail_silently=False)


scheduler = BackgroundScheduler()
scheduler.add_job(send_weekly_newsletter, "cron", day_of_week="fri", hour=12)

DjangoJob.objects.all().delete()  # Очистить предыдущие задания
scheduler.start()
