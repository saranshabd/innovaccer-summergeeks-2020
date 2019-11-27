import re
import boto3
from django.core.mail import send_mail
from innovaccer.settings import EMAIL_HOST_USER
from datetime import datetime
import logging


# configure AWS client
sns_client = boto3.Session(profile_name='sns').client('sns')

logger = logging.getLogger(__name__)


class EntryMgmtUtils:

    '''Public Utility Methods'''

    @staticmethod
    def is_valid_email(email: str) -> bool:
        """validate email address format"""

        regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
        return re.search(regex, email)

    @staticmethod
    def is_valid_phone(phone: str) -> bool:
        """validate phone numbers format (without extension code)"""

        regex = '^[0-9]{10}$'
        return re.search(regex, phone)

    @staticmethod
    def notify_host(email: str, phone_number: str, visitor: dict) -> None:

        EntryMgmtUtils.__notify_host_email(email, visitor)

        EntryMgmtUtils.__notify_host_phone_number(phone_number, visitor)

    @staticmethod
    def notify_visitor(record: dict) -> None:

        # current timestamp
        currtime = datetime.now()

        # configure email properties
        subject = 'Visit Complete'
        message = ('Name=%s,\nPhone Number=%s,\nCheck-in Time=%s,' +
                   '\nCheck-out Time=%s,\nHost Name=%s,\nAddress Visited=%s\n') % (
            record['visitor_name'], record['visitor_phone_number'],
            str(record['check_in']), str(currtime.strftime('%d/%m/%Y %H:%M')),
            record['host_name'], 'Permanent Address')

        # send email
        send_mail(
            subject=subject,
            message=message,
            from_email=EMAIL_HOST_USER,
            recipient_list=[record['visitor_email']],
            fail_silently=False
        )

        logger.info('notification email sent to visitor email address')

    '''Private Helper Methods'''

    @staticmethod
    def __notify_host_email(email: str, visitor: dict) -> None:
        """send notification email to the host about the visitor"""

        # configure email properties
        subject = 'New Visitor'
        message = 'Name=%s,\nEmail=%s,\nPhone Number=%s' % (
            visitor['name'], visitor['email'], visitor['phone_number'])

        # send email
        send_mail(
            subject=subject,
            message=message,
            from_email=EMAIL_HOST_USER,
            recipient_list=[visitor['email']],
            fail_silently=False
        )

        logger.info('notification email sent to host email address')

    @staticmethod
    def __notify_host_phone_number(phone_number: str, visitor: dict) -> None:
        """send notification SMS to the host about the visitor"""

        # configure SMS Message
        message = 'New Visitor\nName=%s,\nEmail=%s,\nPhone Number=%s' % (
            visitor['name'], visitor['email'], visitor['phone_number'])

        # send SMS
        sns_client.publish(
            PhoneNumber=f'+91{phone_number}',
            Message=message,
            MessageAttributes={
                'AWS.SNS.SMS.SMSType': {
                    'DataType': 'String',
                    'StringValue': 'Transactional'
                }
            }
        )

        logger.info('notification SMS sent to host phone number')
