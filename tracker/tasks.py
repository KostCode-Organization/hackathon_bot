"""
A `tracker.tasks` module that contains all celery tasks.
"""
from asgiref.sync import async_to_sync
from celery import shared_task

from .models import TelegramUser
from .telegram.bot import send_revision_messages
from .utils import get_user_revisions


@shared_task
def fetch_approvals(telegram_id: str) -> None:
    """
    Fetch the approvals and revisions of pull request in the repos of current user.
    Notify the user via telegram of the results

    :params telegram_id: The telegram id of the user
    :returns None
    """

    telegram_user = TelegramUser.objects.filter(telegram_id=telegram_id).first()
    if not telegram_user:
        return

    reviews = get_user_revisions(str(telegram_user.telegram_id))
    if reviews:
        async_to_sync(send_revision_messages)(telegram_user.telegram_id, reviews)
