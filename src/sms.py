from .models import AwsSetting, Twilio, NexmoVonage


class TwilioSMS:

    errors: dict = {
        'error' : False,
        'reason' : None
    }

    def __init__(self, account_id: int) -> None:
        from twilio.rest import Client
        self.getAccount = Twilio.query.filter(Twilio.id == account_id).first()
        if self.getAccount is None:
            self.errors = {
                'error' : True,
                'reason' : 'Cannot Search Twilio Account.'
            }
        self.twilio = Client(self.getAccount.twilio_account_sid, self.getAccount.twilio_auth_token)

    def send(self, number: str, body: str) -> bool:
        from twilio.base.exceptions import TwilioRestException
        try:
            response = self.twilio.messages.create(
                to=number,
                from_=self.getAccount.phonenumber,
                body=body
            ).fetch()
            if response.status == "sent":
                return True
            elif response.status == "queued":
                return True
            elif response.status == "sending":
                return True
            return False
        except TwilioRestException:
            return False


class AWSSMS:

    errors: dict = {
        'error' : False,
        'reason' : None
    }

    def __init__(self, account_id: int) -> None:
        import boto3
        self.getAccount = AwsSetting.query.filter(AwsSetting.id == account_id).first()
        if self.getAccount is None:
            self.errors = {
                'error' : True,
                'reason' : 'Cannot Search AWS Account.'
            }
        self.aws = boto3.client(service='sns',  
                                aws_access_key_id=self.getAccount.aws_access_key, 
                                aws_secret_access_key=self.getAccount.aws_secret_key, 
                                region_name=self.getAccount.aws_region)

    def send(self, number: str, body: str) -> bool:
        from botocore.exceptions import ClientError
        try:
            self.aws.publish(
                PhoneNumber=number,
                Message=body
            )
            return True
        except ClientError:
            return False


class VonageSMS:

    errors: dict = {
        'error' : False,
        'reason' : None
    }

    def __init__(self, account_id: int) -> None:
        import vonage
        self.getAccount = NexmoVonage.query.filter(NexmoVonage.id == account_id).first()
        if self.getAccount is None:
            self.errors = {
                'error' : True,
                'reason' : 'Cannot Search Vonage/Nexmo Account.'
            }
        self.nexmo = vonage.Client(key=self.getAccount.vonage_api_key, secret=self.getAccount.vonage_api_secret)

    def send(self, number: str, body: str) -> bool:
        try:
            response = self.nexmo.sms.send_message({
                "from" : self.getAccount.phonenumber,
                "to" : number,
                "body" : body
            })
            if response["messages"][0]["status"] == "0":
                return True
            return False
        except:
            return False


class SMS:

    errors: dict = {
        'error' : False,
        'reason' : None
    }

    def __init__(self, account_id: int, type: str) -> None:
        
        if type == 'aws':
            self.client = AWSSMS(account_id=account_id)
        elif type == 'twilio':
            self.client = TwilioSMS(account_id=account_id)
        elif type == 'vonage':
            self.client = VonageSMS(account_id=account_id)
        else:
            self.errors['error'] = True
            self.errors['reason'] = 'Provider {} Not Found'.format(type)
        
        if self.client.errors['error']:
            self.errors = self.client.errors
        