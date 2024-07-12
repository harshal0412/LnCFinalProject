# #db_opertions.py
# from datetime import datetime, timedelta
# from sentiment import SentimentAnalyzer
# import pyodbc
# from recommendation_engine import RecommendationSystem

# Emp_id = 0

# class DBOperations:
#     def __init__(self, db_config):
#         self.connection = None
#         self.db_config = db_config

#     def connect(self):
#         try:
#             conn_str = ';'.join([f"{key}={value}" for key, value in self.db_config.items()])
#             self.connection = pyodbc.connect(conn_str)
#             print("Database connection successful")
#         except pyodbc.Error as e:
#             print("Failed to connect to the database")
#             print(e)
#             self.connection = None

#     def close(self):
#         if self.connection:
#             self.connection.close()
#             print("Database connection closed")

#     def fetch_all(self, query):
#         cursor = self.connection.cursor()
#         cursor.execute(f"""
#         SELECT DISTINCT f.menu_id, f.rating, f.sentiment_score
#         FROM Feedback f
#         LEFT JOIN Menu m ON f.menu_id = m.ID where m.type = '{query}';""")
#         result = cursor.fetchall()
#         print(result)
#         return result

#     def get_yesterdays_items(self, item_category):
#         cursor = self.connection.cursor()
#         yesterday = str(datetime.now() - timedelta(1))
#         cursor.execute(f"""
#         SELECT DISTINCT c.menu_id
#         FROM Chefmenutable c
#         left join menu m on m.id = c.menu_id
#         where c.sentdate = '{yesterday}' and m.type = '{item_category}';""")
#         data=cursor.fetchall()
#         print(data)
#         return data

#     def signup(self, username, password, role):
#         if self.connection:
#             cursor = self.connection.cursor()
#             cursor.execute("INSERT INTO Users (name, password, role) VALUES (?, ?, ?)", username, password, role)
#             self.connection.commit()
#             return "Signup successful"
#         else:
#             return "Database connection not established"

#     def login(self, username, password):
#         if self.connection:
#             cursor = self.connection.cursor()
#             cursor.execute("SELECT role, Emp_id FROM Users WHERE name = ? AND password = ?", username, password)
#             result = cursor.fetchone()
#             Emp_id=result.Emp_id
#             print(result)
#             if result:
#                 return True, result.role, result.Emp_id
#             else:
#                 return False, None
#         else:
#             return False, None

#     def add_menu_item(self, name, price, availability):
#         if self.connection:
#             cursor = self.connection.cursor()
#             cursor.execute("INSERT INTO Menu (name, price, availability) VALUES (?, ?, ?)", name, price, availability)
#             self.connection.commit()
#             return "Menu item added successfully"
#         else:
#             return "Database connection not established"

#     def update_menu_item(self, item_id, price, availability):
#         if self.connection:
#             cursor = self.connection.cursor()
#             cursor.execute("UPDATE Menu SET price = ?, availability = ? WHERE ID = ?", price, availability, item_id)
#             self.connection.commit()
#             return "Menu item updated successfully"
#         else:
#             return "Database connection not established"

#     def delete_menu_item(self, item_id):
#         if self.connection:
#             cursor = self.connection.cursor()
#             cursor.execute("DELETE FROM Menu WHERE ID = ?", item_id)
#             self.connection.commit()
#             return "Menu item deleted successfully"
#         else:
#             return "Database connection not established"

#     def display_menu(self):
#         if self.connection:
#             cursor = self.connection.cursor()
#             cursor.execute("SELECT * FROM Menu")
#             result = cursor.fetchall()
#             menu_items = [f"ID: {row.ID}, Name: {row.name}, Price: {row.price}, Availability: {row.availability}" for row in result]
#             return "\n".join(menu_items)
#         else:
#             return "Database connection not established"

#     def get_menu_recommendations(self):
#         if not self.connection:
#             return "Database connection not established"
        
#         rec_system = RecommendationSystem(self)
#         recommendations = rec_system.get_recommendations(self, 5)

#         breakfast = "\n".join([f"{item['ID']}: {item['name']}" for item in recommendations['breakfast']])
#         lunch = "\n".join([f"{item['ID']}: {item['name']}" for item in recommendations['lunch']])
#         dinner = "\n".join([f"{item['ID']}: {item['name']}" for item in recommendations['dinner']])  
        
#         # breakfast = "\n".join([f"{item['ID']}: {item['name']} - {item['score']}" for item in recommendations["breakfast"]])
#         # lunch = "\n".join([f"{item['ID']}: {item['name']} - {item['score']}" for item in recommendations["lunch"]])
#         # dinner = "\n".join([f"{item['ID']}: {item['name']} - {item['score']}" for item in recommendations["dinner"]])
        
#         return f"Breakfast:\n{breakfast}\n\nLunch:\n{lunch}\n\nDinner:\n{dinner}"

#     def roll_out_menu(self, breakfast_ids, lunch_ids, dinner_ids):
#         if not self.connection:
#             return "Database connection not established"
        
#         cursor = self.connection.cursor()
#         today = datetime.now().strftime("%Y-%m-%d")
        
#         try:
#             for item_id in breakfast_ids + lunch_ids + dinner_ids:
#                 cursor.execute("INSERT INTO Chefmenutable (menu_id, sentdate) VALUES (?, ?)", item_id, today)
#             self.connection.commit()
#             return "Menu rolled out successfully"
#         except Exception as e:
#             return str(e)

#     def handle_discard_menu_list(self):
#         if self.connection:
#             cursor = self.connection.cursor()
#             cursor.execute("SELECT average rating FROM Feedback group by menu_id where average rating < 2")
#             result = cursor.fetchall()
#             menu_items = [f"ID: {row.ID}, Name: {row.name}, Price: {row.price}, Availability: {row.availability}" for row in result]
#             return "\n".join(menu_items)
#         else:
#             return "Database connection not established"        
#         return

#     def generate_monthly_report(self):
#         if self.connection:
#             cursor = self.connection.cursor()
#             query = """
#             SELECT 
#                 DATEPART(month, date) AS Month, 
#                 m.name AS MenuItem, 
#                 COUNT(mr.menu_id) AS TotalOrders
#             FROM 
#                 MenuRollout mr
#                 JOIN Menu m ON mr.menu_id = m.ID
#             WHERE 
#                 DATEPART(year, date) = DATEPART(year, GETDATE())
#             GROUP BY 
#                 DATEPART(month, date), m.name
#             ORDER BY 
#                 Month, TotalOrders DESC
#             """
#             cursor.execute(query)
#             result = cursor.fetchall()
#             report = ["Month: {row.Month}, MenuItem: {row.MenuItem}, TotalOrders: {row.TotalOrders}" for row in result]
#             return "\n".join(report)
#         else:
#             return "Database connection not established"

#     def tomorrows_menu(self):
#         if self.connection:
#             cursor = self.connection.cursor()
#             print(str(datetime.now().date()))
#             today_date = str(datetime.now().date())
            
#             query = """
#             SELECT m.ID, m.name, m.price, m.type
#             FROM ChefMenuTable cmt
#             JOIN Menu m ON cmt.menu_id = m.ID
#             WHERE cmt.sentdate = ?
#             """
#             cursor.execute(query, (today_date,))
#             result = cursor.fetchall()
            
#             menu_items = [f"ID: {row.ID}, Name: {row.name}, Price: {row.price}, Type: {row.type}" for row in result]
#             return "Today's Menu:\n" + "\n".join(menu_items)
#         else:
#             return "Database connection not established"

#     def employee_voting(self, item_ids):
#         if self.connection:
#             try:
#                 print("hi")            
                
#                 for item_id in item_ids:
#                     item_id=int(item_id)
#                     cursor = self.connection.cursor()
#                     today_date = str(datetime.now().date())
#                     print("item_id==",item_id, today_date)                
#                     cursor.execute("UPDATE Chefmenutable SET votes = votes + 1 WHERE menu_id = ? AND sentdate = ?", (item_id, today_date))
#                     self.connection.commit()
#                 return "Vote added successfully"
#             except Exception as e:
#                 return f"Error incrementing votes: {e}"
#         else:
#             return "Database connection not established"


#     def give_feedback(self, menu_id, feedback, rating):
#         if self.connection:
#             sentiment_score=SentimentAnalyzer.analyze_sentiment(feedback)
#             print(sentiment_score)
#             cursor = self.connection.cursor()
#             today_date = str(datetime.now().date())
#             cursor.execute("INSERT INTO Feedback (menu_id, Emp_id, comment, rating, date, sentiment_score) VALUES (?, ?, ?, ?, ?, ?)", menu_id, Emp_id, feedback, rating, today_date, sentiment_score)
#             self.connection.commit()
#             return "Feedback submitted successfully"
#         else:
#             return "Database connection not established"

#     def increment_votes(self, menu_ids):
#         if self.connection:
#             cursor = self.connection.cursor()
#             try:
#                 for item_id in menu_ids:
#                     cursor.execute("UPDATE Menu SET votes = votes + 1 WHERE ID = ?", item_id)
#                 self.connection.commit()
#                 return "Votes incremented successfully"
#             except Exception as e:
#                 return f"Error incrementing votes: {e}"
#         else:
#             return "Database connection not established"
        
#     def get_item_detail_by_id(self, ids):
#         if not self.connection:
#             cursor = self.connection.cursor()
#             print(ids)
#             cursor.execute(f"""
#             SELECT ID, name, price, availability, type
#             FROM Menu
#             WHERE ID IN ({ids})
#             """)
#             data = cursor.fetchall()

#             item_details = []
#             for row in data:
#                 item_details.append({
#                     'ID': row.ID,
#                     'name': row.name,
#                     'price': row.price,
#                     'availability': row.availability,
#                     'type': row.type
#                 })
#             return item_details
#         else:
#             return "Database connection not established"