import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

class ItemItemRecommender:
    def __init__(self, df):
        self.df = df
        self.category_similar_matrix = self._get_similarity_matrix(self.df['sub_cat'])
        self.brand_similar_matrix = self._get_similarity_matrix(self.df['brand'])

    def _get_similarity_matrix(self, attribute_data):
        # Create a DataFrame with item_id and attribute_data
        df_attribute = pd.DataFrame({'item_id': self.df['item_id'], 'attribute_data': attribute_data})

        # Drop duplicate entries based on item_id, keeping only the first occurrence
        df_attribute_unique = df_attribute.drop_duplicates(subset='item_id', keep='first')

        tfidf_vectorizer = TfidfVectorizer(stop_words='english')
        doc_term = tfidf_vectorizer.fit_transform(df_attribute_unique['attribute_data'])
        dt_matrix = pd.DataFrame(doc_term.toarray().round(3), index=[i for i in df_attribute_unique['item_id']],
                                 columns=tfidf_vectorizer.get_feature_names_out())
        cos_similar_matrix = pd.DataFrame(cosine_similarity(dt_matrix.values), columns=df_attribute_unique['item_id'],
                                          index=df_attribute_unique['item_id'])
        return cos_similar_matrix

    # ... (add_new_data and _update_similarity_matrix methods)

    # ... (other methods and initialization)

    def get_recommendations(self, user_id, top_n=20):
        self.df['visited_count']=pd.to_numeric(self.df['visited_count'])
        # Create an empty list to store recommendations
        top_n_recommendations = []

        # Get the user's item interactions from the dataset
        user_items = self.df[self.df['user_id'] == user_id]['item_id']

        # Combine category and brand similarity (e.g., by taking the average)
        combined_similar_matrix = (self.category_similar_matrix + self.brand_similar_matrix) / 2

        # Iterate through the user's interactions
        for item_id in user_items:
            # Get similar items based on the combined similarity matrix for the current item
            similar_items = combined_similar_matrix.loc[item_id]
            similar_items = similar_items.sort_values(ascending=False)

            # Exclude items that the user has already interacted with
            similar_items = similar_items[~similar_items.index.isin(user_items)]

            # Get top-N recommended items for the user from the current item's similarity
            top_n_items = similar_items.head(top_n).index.tolist()
            top_n_recommendations.extend(top_n_items)

        # Calculate the average view count of recommended items that are present in the original DataFrame
        avg_view_count = self.df[self.df['item_id'].isin(top_n_recommendations)]['visited_count'].mean()

        # Sort the recommended items by a combination of content similarity and view count
        sorted_recommendations = sorted(top_n_recommendations, key=lambda item: (
            combined_similar_matrix[item].mean(),
            self.df[self.df['item_id'] == item]['visited_count'].values[0] / avg_view_count),
                                        reverse=True)

        # Return the list of top-N recommendations for the user (excluding their own interactions)
        return list(set(sorted_recommendations) - set(user_items))

# Dummy data with items and interactions
data = {
    'user_id': ['user1', 'user1', 'user2', 'user2', 'user3', 'user3', 'user4', 'user4'],
    'item_id': ['item1', 'item2', 'item2', 'item3', 'item3', 'item4', 'item4', 'item10'],
    'sub_cat': ['electronics', 'ghewar', 'clothing', 'electronics', 'electronics', 'clothing', 'clothing', 'electronics'],
    'brand': ['brandA', 'brandalana', 'brandB', 'brandC', 'brandC', 'brandA', 'brandA', 'brandB'],
    'visited_count': [5, 3, 2, 4, 1, 5, 3, 2]
}

df = pd.DataFrame(data)

# Create an instance of ContentBasedRecommender
content_recommender =ItemItemRecommender(df)

# Specify the target user for recommendations
target_user = 'user1'

# Get recommendations for the target user
recommendations = content_recommender.get_recommendations(target_user)

print("Recommended items sorted by view count:")
for item in recommendations:
    print(item)
