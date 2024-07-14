
# SMS Bulking.

Support Provider : AWS, Twilio And Vonage (nexmo)

python version : 3.10.11

postgres version : PostgreSQL 16.1



install 

```
pip install -r requirements.txt
```

rename .env.example into .env

change SECRET_KEY and WTF_CSRF_SECRET_KEY 

for production stage change APP_ENV=development to production


Migrate database

```
flask migrate:fresh
```


Create new user.

```
flask shell
```
then in flask shell

```
from src.models import Users
from src import db
from werkzeug.security import generate_password_hash
password = generate_password_hash("change_this_with_your_password")
user = Users(username="admin", password=password)
db.session.add(user)
db.session.commit()
```


Run application

```
flask run
```
or
```
python app.py
```


for production make sure using other server handler like gunicorn, waitress, etc.