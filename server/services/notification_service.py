import datetime
from commons.literals import DB_CONFIG
from database.db_connection import DatabaseConnection


class Notification:
    def __init__(self, message=None, sender=None):
        self.message = message
        self.sender = sender

    def send_notification(self):
        try:
            db = DatabaseConnection(DB_CONFIG)
            db.connect()
            current_date = str(datetime.datetime.today().date())
            query = "insert into notification (message, notification_date, notification_from) values (%s,%s,%s);"
            values = (self.message, current_date, self.sender)
            db.execute_query(query, values)
            db.disconnect()
        except Exception as e:
            print("Error while sending notification")

    def view_notification(self,role):
        try:
            db = DatabaseConnection(DB_CONFIG)
            db.connect()
            if(role == "CHEF"):
                query = """select message from notification where notification_from = 'ADMIN' 
                order by notification_date DESC;"""
                values = None
            elif(role == "EMPLOYEE"):
                query = """select n.message from (select message, notification_date from notification 
                where notification_from != 'CHEF' union 
                select message, notification_date from notification 
                where notification_from = 'CHEF' and notification_date = %s) as n 
                order by n.notification_date DESC;"""
                yesterday_date = str((datetime.datetime.today() - datetime.timedelta(days=1)).date())
                values = (yesterday_date,)
            notification = db.fetch_all(query,values)
            db.disconnect()
        except Exception as e:
            print("Error in fetching notification")
        response = {"action": "VIEW_NOTIFICATION", "data": notification}
        return response