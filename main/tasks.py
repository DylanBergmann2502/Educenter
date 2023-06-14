from celery import shared_task
from celery.utils.log import get_task_logger
from .email import send_contact_email


logger = get_task_logger(__name__)


@shared_task(name="send_contact_email_task")
def send_contact_email_task(name, email, subject):
    logger.info("Contact email sent")
    return send_contact_email(name, email, subject)






# from __future__ import absolute_import, unicode_literals
#
# from celery import shared_task
#
# @shared_task
# def add2(x, y):
#     return x + y