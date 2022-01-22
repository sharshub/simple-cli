from simpl.models import BaseModel

IDENTIFIERS = {cls.identifier: cls for cls in BaseModel.__subclasses__()}


def controller(func):
    def wrap(arg):
        try:
            args = arg.split(" ")
            cls_identifier = args[0]
            if not cls_identifier in IDENTIFIERS:
                raise Exception(
                    "Not a valid data identifier, valid data identifiers are: {identifiers}".format(
                        identifiers=", ".join(IDENTIFIERS)
                    )
                )
            cls = IDENTIFIERS[cls_identifier]
            return func(cls, args[1:])
        except Exception as e:
            print("ERROR:", e)

    return wrap


@controller
def create(cls, args):
    return cls.create_with_args(*args)
