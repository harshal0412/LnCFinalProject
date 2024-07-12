from sentiment.sentiment import SentimentAnalyzer
from datetime import datetime

Emp_id=0

class EmployeeDBOperations:
    def __init__(self, connection):
        self.connection = connection

    def employee_voting(self, item_ids):
        if self.connection:
            try:
                for item_id in item_ids:
                    item_id = int(item_id)
                    cursor = self.connection.cursor()
                    today_date = str(datetime.now().date())
                    cursor.execute("UPDATE Chefmenutable SET votes = votes + 1 WHERE menu_id = ? AND sentdate = ?", (item_id, today_date))
                    self.connection.commit()
                return "Vote added successfully"
            except Exception as e:
                return f"Error incrementing votes: {e}"
        else:
            return "Database connection not established"

    def give_feedback(self, menu_id, feedback, rating):
        if self.connection:
            sentiment_score = SentimentAnalyzer.analyze_sentiment(feedback)
            cursor = self.connection.cursor()
            today_date = str(datetime.now().date())
            cursor.execute("INSERT INTO Feedback (menu_id, Emp_id, comment, rating, date, sentiment_score) VALUES (?, ?, ?, ?, ?, ?)", menu_id, Emp_id, feedback, rating, today_date, sentiment_score)
            self.connection.commit()
            return "Feedback submitted successfully"
        else:
            return "Database connection not established"

    def increment_votes(self, menu_ids):
        if self.connection:
            cursor = self.connection.cursor()
            try:
                for item_id in menu_ids:
                    cursor.execute("UPDATE Menu SET votes = votes + 1 WHERE ID = ?", item_id)
                self.connection.commit()
                return "Votes incremented successfully"
            except Exception as e:
                return f"Error incrementing votes: {e}"
        else:
            return "Database connection not established"

    def get_item_detail_by_id(self, ids):
        if self.connection:
            cursor = self.connection.cursor()
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
        else:
            return "Database connection not established"
