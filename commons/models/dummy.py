from django.db import models

from commons.base_model import BaseModel


class DummyItem(BaseModel):
    description = models.CharField(max_length=256)

    class Meta:
        db_table = "dummy_item"
        verbose_name = "Dummy Item"