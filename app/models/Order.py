from ..database import Base
from tortoise import fields, models

class Order(models.Model):
    id = fields.IntField(pk=True)  # Primary key
    user = fields.ForeignKeyField('models.User', related_name='orders')
    order_date = fields.DatetimeField()
    status = fields.CharField(max_length=50)

    order_details = fields.ReverseRelation['OrderDetail']

    class Meta:
        table = 'orders'


class OrderDetail(models.Model):
    id = fields.IntField(pk=True)  # Primary key
    order = fields.ForeignKeyField('models.Order', related_name='order_details')
    product = fields.ForeignKeyField('models.Product', related_name='order_details')
    quantity = fields.IntField()
    price = fields.DecimalField(max_digits=10, decimal_places=2)
    total_price = fields.FloatField(null=True)

    class Meta:
        table = 'order_details'
