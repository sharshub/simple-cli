from simpl.models import ModelBase, Merchant, Payment, User
from simpl.reports import ReportBase
import re
from decimal import Decimal

IDENTIFIERS = {cls.identifier: cls for cls in ModelBase.__subclasses__()}
REPORTS = {cls.report_name: cls for cls in ReportBase.__subclasses__()}


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
    _report = args[0]

    if not _report in REPORTS:
        raise Exception(
            "Unknown report, valid reports are {reports}".format(
                reports=", ".join(REPORTS)
            )
        )

    cls = REPORTS[_report]
    return cls.generate(*args[1:])
