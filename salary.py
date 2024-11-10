import joblib
import pandas as pd

# Load the trained model
model = joblib.load('./salary_model/salary_prediction_model.pkl')

def predict_salary(age, years_code, work_exp):
    
    # Create a DataFrame with the input data
    input_data = {'Age': [age], 'YearsCode': [years_code], 'WorkExp': [work_exp]}
    input_df = pd.DataFrame(input_data)
    
    # Make salary prediction
    salary_prediction = model.predict(input_df)
    
    return salary_prediction[0]
