WELCOME ON NotIntollerance (!Intollerance)
READ ME BEFORE RUN THIS APPLICATION.

NotIntollerance comes from the idea of looking for every person who is intolerant (in this case gluten)
all the restaurants around him. The user can register and have his own account managed by the sessions
in which he can review each restaurant. Each restaurateur can register his restaurant in the
"Registrati come ristorante" section, enter all the data and finally wait for the admin to accept or reject the proposal.
The admin instead has a personal panel in which there are all the restaurants to be approved and rejected
if he refuses them they will be deleted from the DB, if he approves them they will appear in the restaurants screen.
It can also delete all toxic reviews.
The admin account is as follows:
user: admin@admin.it
password: admin99

FIRST STEP if you have macOS:

Install HOMEBREW

- /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

Install MONGODB Community that is a database NOSQL that uses !INTOLLERANCE

- brew tap mongodb/brew
- brew install mongodb-community@5.0

OPEN TERMINAL AND WRITE IF YOU WANT TO START DB:

- brew services start mongodb-community@5.0

OPEN TERMINAL AND WRITE IF YOU WANT TO STOP DB:

- brew services stop mongodb-community@5.0

After that you can run requirements.txt for installing all the plugins:

- pip3 install -r requirements.txt

After all you can RUN the file app.py, you can go in Browser and write:

- http://127.0.0.1:5000/

ENJOY.

Copyright By russolucaf