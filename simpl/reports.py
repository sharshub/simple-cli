from utils.reports import ReportBase


class DiscountReport(ReportBase):
    report_name = "discount"

    @classmethod
    def generate(cls, *args):
        return super().generate(*args)


class DuesReport(ReportBase):
    report_name = "dues"

    @classmethod
    def generate(cls, *args):
        return super().generate(*args)


class UsersAtCreditLimitReport(ReportBase):
    report_name = "users-at-credit-limit"

    @classmethod
    def generate(cls, *args):
        return super().generate(*args)


class TotalDuesReport(ReportBase):
    report_name = "total-dues"

    @classmethod
    def generate(cls, *args):
        return super().generate(*args)
