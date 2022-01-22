import peewee as orm

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

    def create_with_args(self, *args):
        raise Exception("Provide a class level implementation")


class User(BaseModel):
    name = orm.CharField(unique=True)
    email = orm.CharField()
    credit_limit = orm.DecimalField()

    def save(self, **kwargs):
        assert self.credit_limit >= 0, "Credit limit should be > 0"
        return super().save(**kwargs)

    @classmethod
    def create_with_args(cls, *args):
        assert (
            len(args) == 3
        ), "Incorrect number of arguments provided, req: user, email, credit_limit"
        _name = args[0]
        _email = args[1]
        try:
            _credit_limit = float(args[2])
        except:
            raise Exception("Cannot convert {arg} to a number".format(arg=args[2]))

        return _name, cls.create(name=_name, email=_email, credit_limit=_credit_limit)


class Merchant(BaseModel):
    name = orm.CharField(unique=True)
    discount_rate = orm.DecimalField()

    def save(self, **kwargs):
        assert (
            0 <= self.discount_rate <= 100
        ), "Discount rate should be between 0 and 100"
        return super().save(**kwargs)


class Transaction(BaseModel):
    user = orm.ForeignKeyField(User, backref="transactions")
    merchant = orm.ForeignKeyField(Merchant, backref="transactions")
    amount = orm.DecimalField()

    identifier = "txn"

    def save(self, **kwargs):
        assert 0 <= self.amount <= 100, "Amount should be between 0 and 100"
        return super().save(**kwargs)
