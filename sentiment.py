import numpy as np
from textblob import TextBlob  # For sentiment analysis

class RecommendationSystem:
    def __init__(self, db):
        self.db = db

    def fetch_feedback_data(self):
        cursor = self.db.connection.cursor()
        cursor.execute("SELECT item_id, rating, comment FROM Feedback")
        return cursor.fetchall()

    def analyze_sentiment(self, comment):
        blob = TextBlob(comment)
        sentiment_score = blob.sentiment.polarity  # Returns a value between -1 and 1
        return sentiment_score

    def aggregate_feedback(self, feedback_data):
        feedback_summary = {}

        for feedback in feedback_data:
            item_id, rating, comment = feedback
            sentiment_score = self.analyze_sentiment(comment)

            if item_id not in feedback_summary:
                feedback_summary[item_id] = {'ratings': [], 'sentiments': []}

            feedback_summary[item_id]['ratings'].append(rating)
            feedback_summary[item_id]['sentiments'].append(sentiment_score)

        return feedback_summary

    def compute_item_scores(self, feedback_summary):
        item_scores = {}

        for item_id, feedback in feedback_summary.items():
            avg_rating = np.mean(feedback['ratings'])
            avg_sentiment = np.mean(feedback['sentiments'])

            # Example score calculation: combine average rating and average sentiment
            overall_score = (avg_rating + (avg_sentiment * 5)) / 2
            item_scores[item_id] = overall_score

        return item_scores

    def recommend_menu_items(self):
        feedback_data = self.fetch_feedback_data()
        feedback_summary = self.aggregate_feedback(feedback_data)
        item_scores = self.compute_item_scores(feedback_summary)

        # Sort items by score in descending order
        recommended_items = sorted(item_scores.items(), key=lambda x: x[1], reverse=True)
        
        return recommended_items

# Example usage
if __name__ == "__main__":
    db_operations = DBOperations()  # Assume this is already configured and connected
    recommender = RecommendationSystem(db_operations)
    recommendations = recommender.recommend_menu_items()
    
    for item_id, score in recommendations:
        print(f"Item ID: {item_id}, Score: {score}")
