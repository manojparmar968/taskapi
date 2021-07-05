from common_app.models import Account

def is_email_exist(email):
    email_obj = Account.objects.filter(email=email)
    if email_obj:
        user_id = [email_obj.id for email_obj in email_obj]
        return user_id
    else:
        return None