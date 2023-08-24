import pandas as pd
from sklearn.metrics.pairwise import linear_kernel
from sklearn.feature_extraction.text import TfidfVectorizer

class CollabBasedRecommender:
    def __init__(self, df):
        self.df = df

    def get_recommendation(self,title):
        self.df['combined']=self.df['brand'] + ' ' + self.df['sub_cat']
        vectorizer = TfidfVectorizer()
        matrix = vectorizer.fit_transform(self.df["combined"])
        cosine_similarities = linear_kernel(matrix, matrix)
        idx=self.df[self.df['item_id'] == title].index[0]
        sim_scores = list(enumerate(cosine_similarities[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:5]
        item_indices = [i[0] for i in sim_scores]
        unique_item_indices = []
        seen_item_ids = set()
        for index in item_indices:
            item_id = self.df['item_id'].iloc[index]
            if item_id not in seen_item_ids:
                unique_item_indices.append(index)
                seen_item_ids.add(item_id)

        return self.df['item_id'].iloc[unique_item_indices]

# Create a sample DataFrame
# data = {
#     'item_id': [1, 2, 3, 4, 5],
#     'brand': ['Apple', 'Samsung', 'Sony', 'Apple', 'Sony'],
#     'sub_cat': ['Phone', 'Phone', 'TV', 'Tablet', 'TV']
# }

# df = pd.DataFrame(data)

# Create an instance of ContentBasedRecommender

# Test the content_recommender method
# print("Recommended items:", recommended_items.tolist())
# title_to_recommend = 1  # Change this to the desired item_id
# recommended_items = recommender.content_recommender(title_to_recommend)
