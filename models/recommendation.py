import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def generate_recommendations(db):
    cars = list(db["cars"].find({}, {"_id": 0, "name": 1, "type": 1}))
    if not cars:
        return "No car data available for recommendations."
    
    df = pd.DataFrame(cars)

    df["combined_features"] = df["name"] + " " + df["type"]

    count_matrix = CountVectorizer().fit_transform(df["combined_features"])
    similarity_matrix = cosine_similarity(count_matrix)

    car_index = 0
    similar_cars = list(enumerate(similarity_matrix[car_index]))
    sorted_similar_cars = sorted(similar_cars, key=lambda x: x[1], reverse=True)

    recommendations = [
        df.iloc[i[0]]["name"] for i in sorted_similar_cars[1:4]
    ]
    return f"Recommended cars: {', '.join(recommendations)}"
