from django.db import models
from uuid import uuid4


class Record(models.Model):

    # record information
    record_id = models.UUIDField(
        primary_key=True, default=uuid4, editable=False)
    check_in = models.DateTimeField(null=True)

    # host information
    host_name = models.TextField()
    host_email = models.TextField()
    host_phone_number = models.TextField()

    # visitor information
    visitor_name = models.TextField()
    visitor_email = models.TextField()
    visitor_phone_number = models.TextField(unique=True)

    def __str__(self):
        return str(self.record_id)
