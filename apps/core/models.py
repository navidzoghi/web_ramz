from django.db import models
import uuid

from apps.core.managers import ActiveManger


class AbstractModel(models.Model):
    """
    Abstract base model with common fields for all models.
    """
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    objects = ActiveManger()

    class Meta:
        abstract = True

    def soft_delete(self):
        """Soft delete the object"""
        self.is_deleted = True
        self.is_active = False
        self.save()
