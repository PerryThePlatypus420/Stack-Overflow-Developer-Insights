import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# load the cleaned dataset
df = pd.read_csv('./cleaned_dataset/cleaned_survey_dataset-2.csv')

# print(df.dtypes)


# function for getting recommendations
def recommend_items(user_characteristics, desired_recommendation, df=df,  num_recommend_rows=20):
    # Define column names based on desired recommendation
    if desired_recommendation == 'language':
        columns_to_use = ['LanguageHaveWorkedWith', 'LanguageWantToWorkWith']
    elif desired_recommendation == 'database':
        columns_to_use = ['DatabaseHaveWorkedWith', 'DatabaseWantToWorkWith']
    elif desired_recommendation == 'platform':
        columns_to_use = ['PlatformHaveWorkedWith', 'PlatformWantToWorkWith']
    elif desired_recommendation == 'webframe':
        columns_to_use = ['WebframeHaveWorkedWith', 'WebframeWantToWorkWith']
    elif desired_recommendation == 'os':
        columns_to_use = ['OpSysProfessional use']
    else:
        print("Invalid recommendation type. Please choose from 'language', 'database', 'platform', 'webframe', or 'os'.")
        return
    
    print("2.", user_characteristics)
    
    # Preprocess data and extract relevant features
    df[columns_to_use] = df[columns_to_use].fillna('')
    df['UserFeatures'] = df.apply(lambda row: ' '.join([str(row[col]) for col in user_characteristics]), axis=1)

    # Check if UserFeatures are properly constructed
    # print("UserFeatures:", df['UserFeatures'])

    # TF-IDF Vectorization
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform(df['UserFeatures'])

    # Calculate cosine similarity between user features and desired recommendation
    user_vector = tfidf_vectorizer.transform([str(user_characteristics)])
    cosine_sim = cosine_similarity(user_vector, tfidf_matrix)

    # Get indices of top recommendations
    top_indices = cosine_sim.argsort()[0][-num_recommend_rows:][::-1]

    # Get recommended items
    recommended_items = []
    for _, row in df.iloc[top_indices].iterrows():
        for column in columns_to_use:
            recommended_items.extend(row[column].split(';'))

    
    # removing duplicates and empty string ''
    unique_list = []
    for item in recommended_items:
        if item not in unique_list and item != '':
            unique_list.append(item)
     
            
    # print(unique_list)
        
    return unique_list


