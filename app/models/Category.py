from ..database import Base
from tortoise import fields, models

class Category(models.Model):
    id = fields.IntField(pk=True)  # Primary key
    name = fields.CharField(max_length=50)
    description = fields.TextField(null=True)
    products = fields.ReverseRelation['Product']

    class Meta:
        table = 'categories'
