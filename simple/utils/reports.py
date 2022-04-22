class ReportMeta(type):
    """Requires that all reports have a report_name in them"""

    def __new__(cls, name, bases, attrs):
        if not "report_name" in attrs:
            raise Exception("report_name variable required")
        if not hasattr(cls, "_report_names"):
            setattr(cls, "_report_names", {})
        if attrs["report_name"] in cls._report_names:
            raise Exception("Two classes cannot have the same report_name")
        cls._report_names[attrs["report_name"]] = name
        return super().__new__(cls, name, bases, attrs)


class ReportBase(metaclass=ReportMeta):
    """Extend this class to generate reports"""

    report_name = "base"

    @classmethod
    def generate(cls, *args):
        """Override this function to generate reports"""
        raise Exception("Report not defined")
