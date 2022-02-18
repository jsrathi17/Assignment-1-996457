import pandas as pd
reader = pd.read_csv("../data/data.csv")
reader = reader.drop(["name", "neighbourhood_group", "last_review", "reviews_per_month",  "number_of_reviews_ltm", "license"], axis=1)
reader.to_csv("../data/data.csv")
print("Done!")