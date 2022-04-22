import config
import cmd
from simple.models import db, User, Merchant, Transaction, Payment
from simple.controllers import create, payback, update, report


class SimpleCLI(cmd.Cmd):
    intro = "Welcome to Simple CLI tool. Enter '?' for commands, 'exit' to exit."
    prompt = "> "

    def do_new(self, arg):
        """Create a new object"""
        try:
            obj = create(arg)
            print(obj)
        except Exception as e:
            print("ERROR:", e)

    def do_update(self, arg):
        """Update an existing object"""
        try:
            obj = update(arg)
            print(obj)
        except Exception as e:
            print("ERROR:", e)

    def do_payback(self, arg):
        """Payback amount for user"""
        try:
            payment = payback(arg)
            print(
                "{name} (dues:{dues})".format(
                    name=payment.user.name, dues=payment.user.dues
                )
            )
        except Exception as e:
            print("ERROR:", e)

    def do_report(self, arg):
        """Generate reports"""
        try:
            print(report(arg))
        except Exception as e:
            print("ERROR:", e)

    def do_exit(self, arg):
        """Exit"""
        print("Goodbye!")
        return True


if __name__ == "__main__":
    db.connect()
    db.create_tables([User, Merchant, Transaction, Payment])
    SimpleCLI().cmdloop()
