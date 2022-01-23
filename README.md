# simpl-cli

## Installation
Create a virtual environment and activate
```python
python3 -m venv env
source env/bin/activate
```
Install requirements
```python
pip install -r requirements.txt
```
Installation is complete. You can enter the CLI by typing
```python
python simpl/cli.py
```
When you enter the CLI for the first time, an SQLite DB is automatically created.

## Navigating
### Creating entries
Creating a user as
```
new user <name> <email> <credit_limit>
```
e.g.
```
new user user1 user1@mail.com 1000
```

Create a merchant by
```
new merchant <name> <discount>
```
e.g.
```
new merchant merchant1 10%
```
Create a transaction for user as
```
new txn <<user> <merchant> <amount>
```
e.g.
```
new txn user1 merchant1 900
```

### Updating entries
Update data for user as
```
update user <name> <email> <credit_limit>
```
e.g.
```
update user user1 user1new@mail.com 2000
```
Update data for merchant as
```
update merchant <name> <discount>
```
e.g.
```
update merchant merchant1 5%
```

### Payback
Make payments against dues for a user as
```
payback <user> <amount>
```
e.g.
```
payback user1 800
```

### Reports
Four different reports are defined

1. Get total discount offered by a merchant
```
report discount <merchant>
```
e.g.
```
report discount merchant1
```
2. Get remaining dues of a user
```
report dues <user>
```
e.g.
```
report dues user1
```
3. Get all the users who have reached credit limit
```
report users-at-credit-limit
```
4. Get all the dues owed by users
```
report total-dues
```