import peewee as orm

from simpl.config import db_name

db = orm.SqliteDatabase(db_name)


class ModelMeta(orm.ModelBase):
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


class ModelBase(orm.Model, metaclass=ModelMeta):
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
