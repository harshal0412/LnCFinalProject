from datetime import datetime, timedelta
from recommendation.recommendation_engine import RecommendationSystem

class ChefDBOperations:
    def __init__(self, connection):
        self.connection = connection

    def get_menu_recommendations(self):
        if not self.connection:
            return "Database connection not established"
        
        rec_system = RecommendationSystem(self)
        recommendations = rec_system.get_recommendations(self, 5)

        breakfast = "\n".join([f"{item['ID']}: {item['name']}" for item in recommendations['breakfast']])
        lunch = "\n".join([f"{item['ID']}: {item['name']}" for item in recommendations['lunch']])
        dinner = "\n".join([f"{item['ID']}: {item['name']}" for item in recommendations['dinner']])  
        
        return f"Breakfast:\n{breakfast}\n\nLunch:\n{lunch}\n\nDinner:\n{dinner}"

    def roll_out_menu(self, breakfast_ids, lunch_ids, dinner_ids):
        if not self.connection:
            return "Database connection not established"
        
        cursor = self.connection.cursor()
        today = datetime.now().strftime("%Y-%m-%d")
        
        try:
            for item_id in breakfast_ids + lunch_ids + dinner_ids:
                cursor.execute("INSERT INTO Chefmenutable (menu_id, sentdate) VALUES (?, ?)", item_id, today)
            self.connection.commit()
            return "Menu rolled out successfully"
        except Exception as e:
            return str(e)

    def generate_monthly_report(self):
        if self.connection:
            cursor = self.connection.cursor()
            query = """
            SELECT 
                DATEPART(month, date) AS Month, 
                m.name AS MenuItem, 
                COUNT(mr.menu_id) AS TotalOrders
            FROM 
                MenuRollout mr
                JOIN Menu m ON mr.menu_id = m.ID
            WHERE 
                DATEPART(year, date) = DATEPART(year, GETDATE())
            GROUP BY 
                DATEPART(month, date), m.name
            ORDER BY 
                Month, TotalOrders DESC
            """
            cursor.execute(query)
            result = cursor.fetchall()
            report = ["Month: {row.Month}, MenuItem: {row.MenuItem}, TotalOrders: {row.TotalOrders}" for row in result]
            return "\n".join(report)
        else:
            return "Database connection not established"

    def tomorrows_menu(self):
        if self.connection:
            cursor = self.connection.cursor()
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

    def discard_menu_list(self):
        if self.connection:
            cursor = self.connection.cursor()
            cursor.execute("SELECT average rating FROM Feedback group by menu_id where average rating < 2")
            result = cursor.fetchall()
            menu_items = [f"ID: {row.ID}, Name: {row.name}, Price: {row.price}, Availability: {row.availability}" for row in result]
            return "\n".join(menu_items)
        else:
            return "Database connection not established"

    def get_yesterdays_items(self, item_category):
        cursor = self.connection.cursor()
        yesterday = str(datetime.now() - timedelta(1))
        cursor.execute(f"""
        SELECT DISTINCT c.menu_id
        FROM Chefmenutable c
        left join menu m on m.id = c.menu_id
        where c.sentdate = '{yesterday}' and m.type = '{item_category}';""")
        data = cursor.fetchall()
        return data
