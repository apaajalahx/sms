from src import db
from sqlalchemy.inspection import inspect
from sqlalchemy.orm import Mapped, mapped_column


class Serialize:

    def serialize(self):
        return { c: getattr(self, c) for c in inspect(self).attrs.keys() }
    
    def serialize_list(l):
        return [m.serialize() for m in l]
    

class Users(db.Model, Serialize):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]

    def is_active():
        return True

    def get_id(self):
        return self.id
    
    def is_authenticated():
        return True


class Contacts(db.Model, Serialize):
    __tablename__ = 'contacts'
    id: Mapped[int] = mapped_column(primary_key=True)
    phonenumber: Mapped[str]
    

class Templates(db.Model, Serialize):
    __tablename__ = 'templates'
    id: Mapped[int] = mapped_column(primary_key=True)
    messages: Mapped[str]


class AwsSetting(db.Model, Serialize):
    __tablename__ = 'aws_setting'
    id: Mapped[int] = mapped_column(primary_key=True)
    aws_access_key: Mapped[str]
    aws_secret_key: Mapped[str]
    aws_region: Mapped[str]
    phonenumber: Mapped[str]


class Twilio(db.Model, Serialize):
    __tablename__ = 'twilio_setting'
    id: Mapped[int] = mapped_column(primary_key=True)
    twilio_account_sid: Mapped[str]
    twilio_auth_token: Mapped[str]
    phonenumber: Mapped[str]


class NexmoVonage(db.Model, Serialize):
    __tablename__ = 'nexmo_vonage'
    id: Mapped[int] = mapped_column(primary_key=True)
    vonage_api_key: Mapped[str]
    vonage_api_secret: Mapped[str]
    phonenumber: Mapped[str]