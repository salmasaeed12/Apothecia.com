from ..database import Base
from tortoise import fields, models

class Supplier(models.Model):
    id = fields.IntField(pk=True)  # Primary key
    name = fields.CharField(max_length=255)
    contact_person = fields.CharField(max_length=255)
    phone = fields.CharField(max_length=50, null=True)
    email = fields.CharField(max_length=255, null=True)
    address = fields.TextField(null=True)

    inventory_entries = fields.ReverseRelation['Inventory']

    class Meta:
        table = 'suppliers'

