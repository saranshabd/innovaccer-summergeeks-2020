from django.db.utils import IntegrityError
from .models import Record
from .serializers import RecordSerializer
from datetime import datetime
import logging


logger = logging.getLogger(__name__)


class RecordDao:

    @staticmethod
    def check_in(host: dict, visitor: dict) -> bool:
        """create new database entry for a visitor"""

        # current timestamp
        currtime = datetime.now()

        new_record = Record(
            host_name=host['name'],
            host_email=host['email'],
            host_phone_number=host['phone_number'],
            host_address=host['address'],
            visitor_name=visitor['name'],
            visitor_email=visitor['email'],
            visitor_phone_number=visitor['phone_number'],
            check_in=currtime
        )

        try:
            new_record.save()  # save record in DB

        except IntegrityError:
            # log error
            logger.warning(
                'tried to create new entry with existing visitor phone number')

            return False

        else:
            logger.info('created new visitor entry in DB')

            return True

    @staticmethod
    def check_out(visitor_phone_number) -> dict:
        """delete database entry for an existing visitor record"""

        try:
            # get visitor's record from DB
            record = Record.objects.get(
                visitor_phone_number=visitor_phone_number)

        except Record.DoesNotExist:

            return None

        else:
            data = RecordSerializer(record).data

            # delete record from DB
            record.delete()

            logger.info('visitor record deleted from DB')

            return data
