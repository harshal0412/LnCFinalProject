# db_operations.py
from datetime import datetime,timedelta
from sentiment import SentimentAnalyzer
import pyodbc

class DBOperations:
    def __init__(self, db_config):
        self.connection = None
        self.db_config = db_config

    def connect(self):
        try:
            conn_str = ';'.join([f"{key}={value}" for key, value in self.db_config.items()])
            self.connection = pyodbc.connect(conn_str)
            print("Database connection successful")
        except pyodbc.Error as e:
            print("Failed to connect to the database")
            print(e)
            self.connection = None

    def close(self):
        if self.connection:
            self.connection.close()
            print("Database connection closed")

    def fetch_all(self, query):
        cursor = self.connection.cursor()
        cursor.execute(f"""
        SELECT DISTINCT f.menu_id, f.rating, f.sentiment_score
        FROM Feedback f
        LEFT JOIN Menu m ON f.menu_id = m.ID where m.type = '{query}';""")
        result = cursor.fetchall()
        print(result)
        return result

    def get_yesterdays_items(self, item_category):
        cursor = self.connection.cursor()
        yesterday = str(datetime.now() - timedelta(1))
        cursor.execute(f"""
        SELECT DISTINCT c.menu_id
        FROM Chefmenutable c
        left join menu m on m.id = c.menu_id
        where c.sentdate = '{yesterday}' and m.type = '{item_category}';""")
        data=cursor.fetchall()
        print(data)
        return data

    def signup(self, username, password, role):
        if self.connection:
            cursor = self.connection.cursor()
            cursor.execute("INSERT INTO Users (name, password, role) VALUES (?, ?, ?)", username, password, role)
            self.connection.commit()
            return "Signup successful"
        else:
            return "Database connection not established"

    def login(self, username, password):
        if self.connection:
            cursor = self.connection.cursor()
            cursor.execute("SELECT role FROM Users WHERE name = ? AND password = ?", username, password)
            result = cursor.fetchone()
            if result:
                return True, result.role
            else:
                return False, None
        else:
            return False, None

    def add_menu_item(self, name, price, availability):
        if self.connection:
            cursor = self.connection.cursor()
            cursor.execute("INSERT INTO Menu (name, price, availability) VALUES (?, ?, ?)", name, price, availability)
            self.connection.commit()
            return "Menu item added successfully"
        else:
            return "Database connection not established"

    def update_menu_item(self, item_id, price, availability):
        if self.connection:
            cursor = self.connection.cursor()
            cursor.execute("UPDATE Menu SET price = ?, availability = ? WHERE ID = ?", price, availability, item_id)
            self.connection.commit()
            return "Menu item updated successfully"
        else:
            return "Database connection not established"

    def delete_menu_item(self, item_id):
        if self.connection:
            cursor = self.connection.cursor()
            cursor.execute("DELETE FROM Menu WHERE ID = ?", item_id)
            self.connection.commit()
            return "Menu item deleted successfully"
        else:
            return "Database connection not established"

    def display_menu(self):
        if self.connection:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM Menu")
            result = cursor.fetchall()
            menu_items = [f"ID: {row.ID}, Name: {row.name}, Price: {row.price}, Availability: {row.availability}" for row in result]
            return "\n".join(menu_items)
        else:
            return "Database connection not established"

    def get_menu_recommendations(self):
        from recommendation_engine import RecommendationSystem
        
        if not self.connection:
            return "Database connection not established"
        
        rec_system = RecommendationSystem(self.db_config)
        recommendations = rec_system.get_recommendations(5)  
        
        breakfast = "\n".join([f"{item['ID']}: {item['name']}" for item in recommendations['breakfast']])
        lunch = "\n".join([f"{item['ID']}: {item['name']}" for item in recommendations['lunch']])
        dinner = "\n".join([f"{item['ID']}: {item['name']}" for item in recommendations['dinner']])
        
        return f"Breakfast Recommendations:\n{breakfast}\n\nLunch Recommendations:\n{lunch}\n\nDinner Recommendations:\n{dinner}"

    def roll_out_menu(self, breakfast_ids, lunch_ids, dinner_ids):
        if not self.connection:
            return "Database connection not established"
        from recommendation_engine import RecommendationSystem
        
        try:
            cursor = self.connection.cursor()

            # Roll out breakfast menu items
            self._roll_out_meal(cursor, breakfast_ids, 'Breakfast')

            # Roll out lunch menu items
            self._roll_out_meal(cursor, lunch_ids, 'Lunch')

            # Roll out dinner menu items
            self._roll_out_meal(cursor, dinner_ids, 'Dinner')

            self.connection.commit()
            return "Menu rolled out successfully"

        except pyodbc.Error as e:
            print(f"Error in roll_out_menu: {str(e)}")
            return "Error rolling out menu"

        finally:
            cursor.close()

    def _roll_out_meal(self, cursor, menu_ids, meal_type):
        if menu_ids:
            placeholders = ",".join("?" * len(menu_ids))
            cursor.execute(f"SELECT ID, name FROM Menu WHERE ID IN ({placeholders})", *menu_ids)
            result = cursor.fetchall()
            print(result)
            test_date = str(datetime.now().date())
            for row in result:
                cursor.execute(f"""INSERT INTO Chefmenutable (menu_id, sentdate) VALUES ({row[0]}, '{test_date}')""")



    def generate_monthly_report(self):
        # Placeholder for actual report generation logic
        if self.connection:
            return "Monthly report generated successfully"
        else:
            return "Database connection not established"

    def tomorrows_menu(self):
        if self.connection:
            cursor = self.connection.cursor()
            print(str(datetime.now().date()))
            today_date = str(datetime.now().date())
            
            query = """
            SELECT m.ID, m.name, m.price, m.type
            FROM ChefMenuTable cmt
            JOIN Menu m ON cmt.menu_id = m.ID
            WHERE cmt.sentdate = ?
            """
            cursor.execute(query, (today_date,))
            result = cursor.fetchall()
            
            menu_items = [f"ID: {row.ID}, Name: {row.name}, Price: {row.price}, Type: {row.type}" for row in result]
            return "Today's Menu:\n" + "\n".join(menu_items)
        else:
            return "Database connection not established"

    def give_feedback(self, menu_id, emp_id, comment, rating, date):
        if self.connection:
            sentiment_score = SentimentAnalyzer.analyze_sentiment(comment)
            
            cursor = self.connection.cursor()
            cursor.execute("INSERT INTO Feedback (menu_id, Emp_id, comment, rating, date, sentiment_score) VALUES (?, ?, ?, ?, ?, ?)",
                           menu_id, emp_id, comment, rating, date, sentiment_score)
            self.connection.commit()
            return "Feedback submitted successfully"
        else:
            return "Database connection not established"

    def get_item_detail_by_id(self, ids):
        if not self.connection:
            return "Database connection not established"
        
        cursor = self.connection.cursor()
        print(ids)
        cursor.execute(f"""
        SELECT ID, name, price, availability, type
        FROM Menu
        WHERE ID IN ({ids})
        """)
        data = cursor.fetchall()

        item_details = []
        for row in data:
            item_details.append({
                'ID': row.ID,
                'name': row.name,
                'price': row.price,
                'availability': row.availability,
                'type': row.type
            })
        
        return item_details
