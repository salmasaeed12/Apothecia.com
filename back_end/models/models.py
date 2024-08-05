import pydantic
from tortoise import models, fields
from  pydantic import BaseModel
from datetime import datetime
from tortoise.contrib.pydantic import pydantic_model_creator

class Users(models.Model):
    id = fields.IntField(pk=True, index=True)
    username = fields.CharField(max_length=50, null=False, unique=True)
    password = fields.CharField(max_length=50, null=False)
    email = fields.CharField(max_length=100, null=False, unique=True)
    is_verified = fields.BooleanField(default=datetime.utcnow)
    joined_at = fields.DatetimeField(auto_now_add=True)

class Business(models.Model):
    id = fields.IntField(pk = True, index = True)
    business_name = fields.CharField(max_length = 50, null = False, unique = True)
    city = fields.CharField(max_length = 50, null = False, default = "unspecified")
    region = fields.CharField(max_length = 100, null = False, default = "unspecified")
    business_description = fields.CharField(max_length = 200, null = True)
    logo = fields.CharField(max_length = 300, null = True, default = "default.jpg")
    owner = fields.ForeignKeyField("models.Users", related_name = "businesses")

class Products(models.Model):
    id = fields.IntField(pk = True, index = True)
    name = fields.CharField(max_length = 200, null = False, index = True)
    category = fields.CharField(max_length = 100, index = True)
    original_price = fields.DecimalField(max_digits = 10, decimal_places = 2)
    new_price = fields.DecimalField(max_digits = 10, decimal_places = 2)
    persentage_discount = fields.DecimalField(max_digits = 5, decimal_places = 2)
    offer_expiration = fields.DatetimeField(default = datetime.utcnow)
    product_image = fields.CharField(max_length = 300, null = True, default = "default.jpg")
    business = fields.ForeignKeyField("models.Business", related_name = "products")

user_pydantic = pydantic_model_creator(Users, name="User", exclude=("is_verified"))
user_pydanticIn = pydantic_model_creator(Users, name="UserIn", exclude_readonly=True)
user_pydenticOut = pydantic_model_creator(Users, name="UserOut", exclude=("password"))

business_pydantic = pydantic_model_creator(Business, name = "Business")
business_pydanticIn = pydantic_model_creator(Business, name = "BusinessIn", exclude_readonly = True)

product_pydantic = pydantic_model_creator(Products, name = "Product")
product_pydanticIn = pydantic_model_creator(Products, name = "ProductIn", exclude = ("persentage_discount", "id"))