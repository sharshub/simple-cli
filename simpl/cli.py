import config
import cmd
from simpl.models import db, User, Merchant, Transaction
from simpl.controllers import create


class SimplCLI(cmd.Cmd):
    intro = "Welcome to Simpl CLI tool. Enter '?' for commands, 'exit' to exit."
    prompt = "> "

    def do_new(self, arg):
        """Create a new object"""
        attr, obj = create(arg)
        globals[attr] = obj

    def do_exit(self, arg):
        """Exit"""
        print("Goodbye!")
        return True


if __name__ == "__main__":
    db.connect()
    db.create_tables([User, Merchant, Transaction])
    SimplCLI().cmdloop()
