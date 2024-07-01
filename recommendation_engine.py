# recommendation_engine.py

from datetime import datetime, timedelta
from db_operations import DBOperations
from menu_operations import MenuOperations

class RecommendationSystem:
    def __init__(self, db_config):
        self.db_config = db_config

    def fetch_feedback_data(self, item_category):
        db = DBOperations(self.db_config)
        db.connect()
        data = db.fetch_all(item_category)
        db.close()
        return data

    def get_yesterdays_items(self, item_category):
        db = DBOperations(self.db_config)
        db.connect()
        data = db.get_yesterdays_items(item_category)
        db.close()
        return data

    def recommend_items(self, item_category, num_items):
        feedback_data = self.fetch_feedback_data(item_category)
        exclude_items = self.get_yesterdays_items(item_category)
        items = {}
        exclude_items = [item[0] for item in exclude_items]
        for item in feedback_data:
            if item[0] not in exclude_items:
                if item[0] not in items:
                    items[item[0]] = {
                        'total_score': 0,
                        'count': 0,
                    }
                # Combine rating and sentiment_score for scoring items
                score = item[1] + item[2]
                items[item[0]]['total_score'] += score
                items[item[0]]['count'] += 1

        recommendations = sorted(
            items.items(),
            key=lambda x: x[1]['total_score'] / x[1]['count'],
            reverse=True
        )
        recommended_ids = [item[0] for item in recommendations[:num_items]]
        recommended_ids = ','.join(map(str,recommended_ids))
        return recommended_ids

    def get_recommendations(self, num_items):
        db = DBOperations(self.db_config)
        db.connect()
        menu_ops = MenuOperations(db)
        breakfast_recommendations = menu_ops.get_item_detail_by_id(self.recommend_items('breakfast', num_items))
        lunch_recommendations = menu_ops.get_item_detail_by_id(self.recommend_items('lunch', num_items))
        dinner_recommendations = menu_ops.get_item_detail_by_id(self.recommend_items('dinner', num_items))
        db.close()

        return {
            'breakfast': breakfast_recommendations,
            'lunch': lunch_recommendations,
            'dinner': dinner_recommendations,
        }
