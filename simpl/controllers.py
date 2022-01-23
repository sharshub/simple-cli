from simpl.models import BaseModel, Payment, User
import re
from decimal import Decimal

IDENTIFIERS = {cls.identifier: cls for cls in BaseModel.__subclasses__()}


def controller(func):
    def wrap(arg):
        args = arg.split(" ")
        return func(*args)

    return wrap


@controller
def create(*args):
    cls_identifier = args[0]
    if not cls_identifier in IDENTIFIERS:
        raise Exception(
            "Not a valid data identifier, valid data identifiers are: {identifiers}".format(
                identifiers=", ".join(IDENTIFIERS)
            )
        )
    cls = IDENTIFIERS[cls_identifier]
    return cls.create_with_args(*args[1:])


@controller
def update(*args):
    cls_identifier = args[0]
    if not cls_identifier in IDENTIFIERS:
        raise Exception(
            "Not a valid data identifier, valid data identifiers are: {identifiers}".format(
                identifiers=", ".join(IDENTIFIERS)
            )
        )
    cls = IDENTIFIERS[cls_identifier]
    return cls.update_with_args(*args[1:])


@controller
def payback(*args):
    assert len(args) >= 2
    user = User.get(User.name == args[0])
    amount = args[1]
    if not re.match("^[\d\.\,]+$", amount):
        raise Exception("Incorrect format for amount.")
    amount = Decimal(amount.replace(",", ""))

    payment = Payment.create(user=user, amount=amount)

    return payment


@controller
def report(*args):
    pass
