from ..database import Base
from tortoise import fields, models

class Product(models.Model):
    id = fields.IntField(pk=True)  # Primary key
    name = fields.CharField(max_length=50)
    description = fields.TextField(null=True)
    price = fields.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = fields.IntField()
    category = fields.ForeignKeyField('models.Category', related_name='products')

    order_details = fields.ReverseRelation['OrderDetail']
    inventory_entries = fields.ReverseRelation['Inventory']
    orders = fields.ManyToManyField('models.Order', related_name='products', through='order_details')

    class Meta:
        table = 'products'

