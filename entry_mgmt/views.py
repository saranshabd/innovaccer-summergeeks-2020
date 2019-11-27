from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
import logging
from .utils import EntryMgmtUtils
from .dao import RecordDao


logger = logging.getLogger(__name__)


@api_view(['POST'])
def check_in(request):

    try:
        try:
            host = dict()
            visitor = dict()

            # extract host details from request body
            host['name'] = str(request.data['host']['name'])
            host['email'] = str(request.data['host']['email'])
            host['phone_number'] = str(request.data['host']['phone_number'])

            # extract visitor details from request body
            visitor['name'] = str(request.data['visitor']['name'])
            visitor['email'] = str(request.data['visitor']['email'])
            visitor['phone_number'] = str(
                request.data['visitor']['phone_number'])

            # check email address format
            if not EntryMgmtUtils.is_valid_email(host['email']) or \
                    not EntryMgmtUtils.is_valid_email(visitor['email']):

                # log error
                logger.warning('invalid email address(s)')

                raise KeyError()

            # check phone number format
            if not EntryMgmtUtils.is_valid_phone(host['phone_number']) or \
                    not EntryMgmtUtils.is_valid_phone(visitor['phone_number']):

                # log error
                logger.warning('invalid phone number(s)')

                raise KeyError()

        except KeyError:
            # log error
            logger.warning('400, invalid parameters passed')

            return Response(status=status.HTTP_400_BAD_REQUEST)

        # create new db entry for the visitor
        if not RecordDao.check_in(host, visitor):
            return Response({
                'duplicate': 'visitor/phone_number'
            }, status=status.HTTP_400_BAD_REQUEST)

        # notify host about the visitor (SMS and email)
        EntryMgmtUtils.notify_host(
            host['email'], host['phone_number'], visitor)

        logger.info('201, user checked in successfully')

        return Response(status=status.HTTP_201_CREATED)

    except Exception as e:
        # log exception
        logger.exception('500, unhandled exception')

        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def check_out(request):

    try:
        try:
            # extract visitor phone number from request body
            phone_number = str(request.data['phone_number'])

            # check phone number format
            if not EntryMgmtUtils.is_valid_phone(phone_number):
                # log error
                logger.warning('invalid phone number')

                raise KeyError()

        except KeyError:
            # log error
            logger.warning('400, invalid parameters passed')

            return Response(status=status.HTTP_400_BAD_REQUEST)

        # check out visitor from DB
        record = RecordDao.check_out(phone_number)
        if record is None:
            # log error
            logger.warning('404, visitor phone number does not exist in DB')

            return Response(status=status.HTTP_404_NOT_FOUND)

        # send notification email to the visitor
        EntryMgmtUtils.notify_visitor(record)

        logger.info('200, user checked out successfully')

        return Response(status=status.HTTP_200_OK)

    except Exception as e:
        # log exception
        logger.exception('500, unhandled exception')

        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
