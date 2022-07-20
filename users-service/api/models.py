""" Module of all services models """
from tortoise import Model, fields
from tortoise.contrib.pydantic import pydantic_model_creator

from consts import DBUtils


class Location(Model):
    """ Location model that describes where user lives """
    home_number = fields.IntField(default=1)
    street = fields.CharField(max_length=DBUtils.MAX_CHARS_LENGTH.value)
    city = fields.CharField(max_length=DBUtils.MAX_CHARS_LENGTH.value)
    country_code = fields.CharField(max_length=DBUtils.MAX_CODES_LENGTH.value)
    postal_code = fields.CharField(max_length=DBUtils.MAX_CODES_LENGTH.value)

    def __str__(self) -> str:
        """ :returns: Override str of model and return assemble of values. """
        return (f"{self.street} {self.home_number}, {self.city}, "
                f"{self.country_code}")


class User(Model):
    """ General User in the application """
    id = fields.IntField(pk=True)
    full_name = fields.CharField(max_length=DBUtils.MAX_CHARS_LENGTH.value)
    created_at = fields.DatetimeField(auto_now_add=True)
    address = fields.OneToOneField(model_name="Location", related_name="user")

    class Meta:
        unique_together = ("full_name", "address")

    def __str__(self) -> str:
        """ :returns: Override str of model and return user name. """
        return self.full_name


UserIn_Pydantic = pydantic_model_creator(User,
                                         exclude_readonly=True,
                                         exclude=("created_at", ))
UserOut_Pydantic = pydantic_model_creator(User)
