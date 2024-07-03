# recommendation_engine.py
from menu_operations import MenuOperations

class RecommendationSystem:
    def __init__(self, menu_operations):
        self.menu_operations = menu_operations

    def fetch_feedback_data(self, item_category):
        data = self.menu_operations.fetch_all(item_category)
        return data

    def get_yesterdays_items(self, item_category):
        data = self.menu_operations.get_yesterdays_items(item_category)
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
        recommended_ids = ','.join(map(str, recommended_ids))
        return recommended_ids

    def get_recommendations(self, db_operations, num_items):
        menu_ops = MenuOperations(db_operations)
        breakfast_recommendations = menu_ops.get_item_detail_by_id(self.recommend_items('breakfast', num_items))
        lunch_recommendations = menu_ops.get_item_detail_by_id(self.recommend_items('lunch', num_items))
        dinner_recommendations = menu_ops.get_item_detail_by_id(self.recommend_items('dinner', num_items))

        return {
            'breakfast': breakfast_recommendations,
            'lunch': lunch_recommendations,
            'dinner': dinner_recommendations,
        }
