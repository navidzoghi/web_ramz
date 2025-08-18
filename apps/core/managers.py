from django.db import models


class ActiveManger(models.Manager):
    def active(self):
        return super().get_queryset().filter(is_active=True, is_deleted=False)
