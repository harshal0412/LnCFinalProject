import datetime
from commons.literals import DB_CONFIG
from database.db_connection import DatabaseConnection
from services.sentiment_analyzer import SentimentAnalyzer

class Feedback:

    def provide_feedback(self, data):
        try:
            db = DatabaseConnection(DB_CONFIG)
            db.connect()
            feedback_date = str(datetime.datetime.today().date())
            sentiment_analyzer = SentimentAnalyzer()
            sentiment_score = sentiment_analyzer.analyze_sentiment(data['comment'])
            query = '''
            insert into feedback (user_id, item_id, comment, rating, sentiment_score, feedback_date) values (%s,%s,%s,%s,%s,%s);
            '''
            values = (data['user_id'], data['item_id'],data['comment'],data['rating'],sentiment_score,feedback_date)
            db.execute_query(query, values)
            db.disconnect()
            status = "Feedback provided successfully"
        except Exception as e:
            status = "Error while providing feedback"
        response = {"action": "PROVIDE_FEEDBACK", "status": status}
        return response
    
    def provide_detailed_feedback(self, data):
        try:
            db = DatabaseConnection(DB_CONFIG)
            db.connect()
            feedback_date = str(datetime.datetime.today().date())
            query = '''
            insert into detailed_feedback (user_id, item_id, liked, disliked, home_recipe, feedback_date) values (%s,%s,%s,%s,%s,%s);
            '''
            values = (data['user_id'], data['item_id'],data['liked'],data['disliked'],data['home_recipe'],feedback_date)
            db.execute_query(query, values)
            db.disconnect()
            status = "Feedback provided successfully"
        except Exception as e:
            status = "Error while providing feedback"
        response = {"action": "PROVIDE_DETAILED_FEEDBACK", "status": status}
        return response
    
    def get_feedback(self, type=None):
        try:
            db = DatabaseConnection(DB_CONFIG)
            db.connect()
            if(type == "detailed"):
                query = "select id, user_id, item_id, liked, disliked, home_recipe from detailed_feedback order by feedback_date DESC;"
                action = "VIEW_DETAILED_FEEDBACK"
            else:
                query = "select id, user_id, item_id, comment, rating, sentiment_score from feedback order by feedback_date DESC;"
                action = "VIEW_FEEDBACK"
            feedback = db.fetch_all(query)
            db.disconnect()
            status = "Feedback fetched successfully"
        except Exception as e:
            status = "Error while fetching feedback"
        response = {"action": action, "status": status, "feedback": feedback}
        return response