import peewee as orm
import re
from decimal import Decimal

from simpl.config import db_name

db = orm.SqliteDatabase(db_name)


class BaseMeta(orm.ModelBase):
    """Extends the metaclass of Base Model to include identifier tags in our classes"""

    def __new__(cls, name, bases, attrs):
        if not "identifier" in attrs:
            attrs["identifier"] = name.lower()
        if not hasattr(cls, "_identifiers"):
            setattr(cls, "_identifiers", {})
        if attrs["identifier"] in cls._identifiers:
            raise Exception("Two classes cannot have the same identifier")
        cls._identifiers[attrs["identifier"]] = name
        return super().__new__(cls, name, bases, attrs)


class BaseModel(orm.Model, metaclass=BaseMeta):
    class Meta:
        database = db

    @classmethod
    def get_args(cls, *args):
        raise Exception("Provide a class level implementation")

    @classmethod
    def create_with_args(cls, *args):
        raise Exception(
            "Cannot create a {identifier} from console directly".format(
                identifier=cls.identifier
            )
        )

    @classmethod
    def update_with_args(cls, *args):
        raise Exception(
            "Cannot update a {identifier} from console directly".format(
                identifier=cls.identifier
            )
        )


class User(BaseModel):
    name = orm.CharField(unique=True)
    email = orm.CharField()
    credit_limit = orm.DecimalField(constraints=[orm.Check("credit_limit >= 0")])
    dues = orm.DecimalField(default=0, constraints=[orm.Check("dues >= 0")])

    def save(self, **kwargs):
        assert (
            self.dues <= self.credit_limit
        ), "User cannot overspend beyond credit limit"
        return super().save(**kwargs)

    def __str__(self):
        return "{name} ({credit_limit})".format(
            name=self.name, credit_limit=self.credit_limit
        )

    @classmethod
    def get_args(self, *args):
        assert (
            len(args) >= 3
        ), "Incorrect number of arguments provided, req: user, email, credit_limit"
        _name = args[0]
        _email = args[1]
        try:
            _credit_limit = Decimal(args[2])
        except:
            raise Exception("Cannot convert {arg} to a number".format(arg=args[2]))
        return _name, _email, _credit_limit

    @classmethod
    def create_with_args(cls, *args):
        _name, _email, _credit_limit = cls.get_args(*args)
        return cls.create(name=_name, email=_email, credit_limit=_credit_limit)

    @classmethod
    def update_with_args(cls, *args):
        _name, _email, _credit_limit = cls.get_args(*args)
        if cls.select().where(cls.name == _name).exists():
            obj = cls.get(cls.name == _name)
            obj.email = _email
            obj.credit_limit = _credit_limit
            obj.save()
            return obj
        else:
            raise Exception("Merchant {name} does not exist".format(name=_name))


class Merchant(BaseModel):
    name = orm.CharField(unique=True)
    discount_rate = orm.DecimalField(
        constraints=[orm.Check("discount_rate >= 0"), orm.Check("discount_rate <= 100")]
    )

    def __str__(self):
        return "{name} ({discount_rate}%)".format(
            name=self.name, discount_rate=self.discount_rate
        )

    @classmethod
    def get_args(cls, *args: str):
        assert (
            len(args) >= 2
        ), "Incorrect number of arguments provided, req: merchant_name, discount"
        _name = args[0]
        _discount_rate = args[1]
        if not re.match("^[\d\.\,]+\%$", _discount_rate):
            raise Exception("Incorrect format for discount. Enter discount as: 10%")
        _discount_rate = Decimal(_discount_rate.replace(",", "").replace("%", ""))
        return _name, _discount_rate

    @classmethod
    def create_with_args(cls, *args: str):
        _name, _discount_rate = cls.get_args(*args)
        return cls.create(name=_name, discount_rate=_discount_rate)

    @classmethod
    def update_with_args(cls, *args):
        _name, _discount_rate = cls.get_args(*args)
        if cls.select().where(cls.name == _name).exists():
            obj = cls.get(cls.name == _name)
            obj.discount_rate = _discount_rate
            obj.save()
            return obj
        else:
            raise Exception("Merchant {name} does not exist".format(name=_name))


class Transaction(BaseModel):
    user = orm.ForeignKeyField(User, backref="transactions")
    merchant = orm.ForeignKeyField(Merchant, backref="transactions")
    amount = orm.DecimalField(constraints=[orm.Check("amount >= 0")])
    merchant_discount = orm.DecimalField(
        constraints=[orm.Check("merchant_discount >= 0")]
    )

    identifier = "txn"

    def save(self, **kwargs):
        with db.atomic() as transaction:
            try:
                self.user.dues += self.amount
                self.user.save()
                self.merchant_discount = (
                    self.merchant.discount_rate * self.amount / Decimal(100)
                )
                return super().save(**kwargs)

            except Exception as e:
                transaction.rollback()
                raise e

    def __str__(self):
        return "success! {user} -> {merchant} ({amount})".format(
            user=self.user.name, merchant=self.merchant.name, amount=self.amount
        )

    @classmethod
    def get_args(cls, *args: str):
        assert (
            len(args) >= 3
        ), "Incorrect number of arguments provided, req: user, merchant, amount"

        _user_name = args[0]
        _merchant_name = args[1]
        _amount = args[2]

        if not re.match("^[\d\.\,]+$", _amount):
            raise Exception("Incorrect format for amount.")

        _user = User.get(User.name == _user_name)
        _merchant = Merchant.get(Merchant.name == _merchant_name)
        _amount = Decimal(_amount.replace(",", ""))

        return _user, _merchant, _amount

    @classmethod
    def create_with_args(cls, *args):
        _user, _merchant, _amount = cls.get_args(*args)
        return cls.create(user=_user, merchant=_merchant, amount=_amount)

    @classmethod
    def update_with_args(self, *args):
        raise Exception("Updating an existing transaction is not allowed")


class Payment(BaseModel):
    user = orm.ForeignKeyField(User, backref="payments")
    amount = orm.DecimalField(constraints=[orm.Check("amount >= 0")])

    def save(self, **kwargs):
        with db.atomic() as transaction:
            assert self.user.dues <= self.amount, "Payback cannot be more than dues"
            try:
                self.user.dues -= self.amount
                self.user.save()
                return super().save(**kwargs)

            except Exception as e:
                transaction.rollback()
                raise e
