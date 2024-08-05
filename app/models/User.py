from ..database import Base
from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator
from enum import Enum

class UserRole(str, Enum):
    admin = "admin"
    user = "user"

class User(models.Model):
    id = fields.IntField(pk=True)  # Primary key
    first_name = fields.CharField(max_length=100)
    last_name = fields.CharField(max_length=100)
    email = fields.CharField(max_length=100)
    password_hash = fields.CharField(max_length=100)
    phone = fields.CharField(max_length=20, null=True)
    address = fields.TextField(null=True)
    role = fields.CharEnumField(UserRole, default=UserRole.user)

    orders = fields.ReverseRelation['Order']

    class Meta:
        table = 'users'

# Optional: Pydantic model for User
User_Pydantic = pydantic_model_creator(User, name="User")
user_pydanticIn = pydantic_model_creator(User, name="UserIn", exclude_readonly=True)
user_pydanticOut = pydantic_model_creator(User, name="UserOut", exclude=("password"))