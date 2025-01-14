"""
A `shared.models` model that contains all shared models
"""
import uuid

from django.db import models


class AbstractModel(models.Model):
    """
    An abstract base model that provides common fields for all models.

    Fields:
    - id (UUIDField): A unique identifier for each instance, automatically generated.
    - created_at (DateTimeField): The timestamp when the instance was created, set automatically.
    - updated_at (DateTimeField): The timestamp when the instance was last updated,
        updated automatically.

    This class is intended to be used as a base class for other models, providing a
    consistent structure for commonly used fields. As an abstract model, it will not
    create a separate database table.

    Meta:
        abstract (bool): Set to True, indicating this model is abstract.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:  # pylint: disable=too-few-public-methods
        """A metaclass to set this model to be abstract"""
        abstract = True
