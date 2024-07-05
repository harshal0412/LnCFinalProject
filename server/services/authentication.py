from database.db_connection import DatabaseConnection
from commons.literals import *

class AuthService:
    def login(self, email):
        user = self.get_user_details_from_email(email)
        if len(user) == 1:
            print(f"Authentication successfull Welcome {user[0][0]}..!")
            return user
        else:
            print("Authentication failed user not present.")
            return user
    
    def get_user_details_from_email(self, email):
        db = DatabaseConnection(DB_CONFIG)
        db.connect()
        query = "select user_name, email, role_name, user_id from users u join role r on u.role = r.role_id where email = %s;"
        values = (email,)
        user_details = db.fetch_all(query, values)
        return user_details
