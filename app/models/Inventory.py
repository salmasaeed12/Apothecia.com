from ..database import Base
from tortoise import fields, models

class Inventory(models.Model):
    id = fields.IntField(pk=True)  # Primary key
    product = fields.ForeignKeyField('models.Product', related_name='inventory_entries')
    supplier = fields.ForeignKeyField('models.Supplier', related_name='inventory_entries')
    quantity = fields.IntField()
    received_date = fields.DatetimeField()

    class Meta:
        table = 'inventory'