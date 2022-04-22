import peewee as orm
from utils.reports import ReportBase
from src.models import Merchant, Transaction, User


class DiscountReport(ReportBase):
    report_name = "discount"

    @classmethod
    def generate(cls, *args):
        assert len(args) >= 1, "Merchant name required for generating discount report"
        merchant_name = args[0]
        if not Merchant.select().where(Merchant.name == merchant_name).exists():
            raise Exception(
                "Merchant {merchant_name} not found".format(merchant_name=merchant_name)
            )
        merchant = Merchant.get(name=merchant_name)

        result = (
            Transaction.select(orm.fn.SUM(Transaction.merchant_discount))
            .where(Transaction.merchant == merchant)
            .scalar()
        ) or 0

        return result


class DuesReport(ReportBase):
    report_name = "dues"

    @classmethod
    def generate(cls, *args):
        assert len(args) >= 1, "User name required for generating dues report"
        user_name = args[0]
        if not User.select().where(User.name == user_name).exists():
            raise Exception("User {user_name} not found".format(user_name=user_name))
        user = User.get(name=user_name)
        return user.dues


class UsersAtCreditLimitReport(ReportBase):
    report_name = "users-at-credit-limit"

    @classmethod
    def generate(cls, *args):
        users = User.select().where(User.credit_limit == User.dues)
        if len(users) == 0:
            return "No users at credit limit"
        else:
            return "\n".join(user.name for user in users)


class TotalDuesReport(ReportBase):
    report_name = "total-dues"

    @classmethod
    def generate(cls, *args):
        users = User.select().where(User.dues > 0)
        if len(users) == 0:
            return "No dues!"
        return "\n".join(
            "{name}: {dues}".format(name=user.name, dues=user.dues) for user in users
        )
