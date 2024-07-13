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
    folder_name: Mapped[str]
    phonenumber: Mapped[str]

    def groupBy(page: int = 1, per_page: int = 10):
        return Contacts.query.with_entities(Contacts.folder_name) \
                    .group_by(Contacts.folder_name) \
                    .paginate(page=page, per_page=per_page, error_out=False)

    def groupByAll():
        return Contacts.query.with_entities(Contacts.folder_name) \
                    .group_by(Contacts.folder_name) \
                    .all()

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


class ThreadingStatus(db.Model, Serialize):
    __tablename__ = 'threading_status'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    is_active: Mapped[bool] = mapped_column(default=False)
    completed: Mapped[bool] = mapped_column(default=False)
    size: Mapped[int]
    success_count: Mapped[int]
    failed_count: Mapped[int]
    Account_type: Mapped[str]
    Account_id: Mapped[int]

    def getRelationship(id: int):
        thread = ThreadingStatus.query.filter(ThreadingStatus.id == id).first()
        ret = {'thread' : thread, 'aws' : None, 'twilio' : None, 'vonage' : None}
        if thread is not None:
            if thread.Account_type == 'aws':
                ret['aws'] = AwsSetting.query.filter(AwsSetting.id == thread.Account_id).first()
            elif thread.Account_type == 'vonage':
                ret['vonage'] = NexmoVonage.query.filter(NexmoVonage.id == thread.Account_id).first()
            elif thread.Account_type == 'twilio':
                ret['twilio'] = Twilio.query.filter(Twilio.id == thread.Account_id).first()

        return ret