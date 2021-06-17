from pyfcm import FCMNotification
from teacherpal.settings import firebase_server_key


proxy_dict = {
          "http"  : "http://127.0.0.1",
          "https" : "http://127.0.0.1",
        }


# for simple notification (message notification) we can also send data notification
def send_notification(fcm_token_qs,message_title,message_body):
    push_service = FCMNotification(api_key=firebase_server_key)

    registration_ids =[]

    for fcm_token in fcm_token_qs:
        if fcm_token.fcm_token !="":
            registration_ids.append(fcm_token.fcm_token)

    valid_registration_ids = push_service.clean_registration_ids(registration_ids)

    result = push_service.notify_multiple_devices(registration_ids=valid_registration_ids, 
                                                    message_title=message_title, message_body=message_body)
    
    print(result)