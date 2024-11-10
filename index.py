import streamlit as st
import pandas as pd
import recommendations
import salary


# Read the CSV file
df = pd.read_csv('./cleaned_dataset/cleaned_survey_dataset-2.csv')


print("\nSession state object:", st.session_state)

# Define user_characteristics globally
if "user_characteristics" not in st.session_state:
    st.session_state['user_characteristics'] = {}

print("Session state object:", st.session_state)


# Function to display recommendations in Streamlit GUI
def display_recommendations(recommended_items, desired_recommendation, num_recommendations=6):
    # Ensure that the number of recommended items to display does not exceed the actual number of recommended items
    num_recommendations = min(num_recommendations, len(recommended_items))

    # Display recommended items in Streamlit GUI
    st.write(f"Recommended {desired_recommendation}s:")
    for i, item in enumerate(recommended_items[:num_recommendations], start=1):
        st.write(f"{i}. {item}")


# Sidebar form for entering user characteristics
def show_recommendations_form():
    
    with st.sidebar.form(key='recommendations_form'):
        # text input fields for user characteristics
        age = st.selectbox(label='Enter your age', options=['Under 18 years old',
                                                            '18-24 years old', '25-34 years old',
                                                            '35-44 years old', '45-54 years old', '55-64 years old',
                                                            '65 years or older', 'Prefer not to say'])

        employment = st.multiselect(label='Select your employment status',
                                    options=['Employed, full-time', 'Employed, part-time',
                                             'Independent contractor, freelancer or self-employed',
                                             'Student, full-time', 'Student, part-time',
                                             'Not employed, but looking for work', 'Not employed, and not looking for work',
                                             'Retired'])

        education = st.selectbox(label='Select your education level',
                                 options=["Bachelor's degree (BA, BS, B.Eng., etc.)",
                                          "Master's degree (M.A., M.S., M.Eng., MBA, etc.)",
                                          "Some college/university study without earning a degree",
                                          "secondary school (e.g. American high school, German Realschule or Gymnasium, etc.)",
                                          "Associate degree (A.A., A.S., etc.)", "Other doctoral degree (Ph.D., Ed.D., etc.)"])

        remote = st.selectbox(label='Select your remote work status', options=['Remote',
                                                                              'Hybrid (some remote, some in-person)',
                                                                              'In-person'])

        yrs_code = st.number_input("Enter your work experience (in years):", step=1)
        # Convert the integer to a string because it is string in dataset and we want to compare them
        yrs_code = str(int(yrs_code))

        # submit button
        submit_recom = st.form_submit_button(label='Submit')

    # Process the form submission
    if submit_recom:
        st.session_state['user_characteristics'] = {
            'Age': age,
            'Employment': employment,
            'EdLevel': education,
            'RemoteWork': remote,
            'YearsCode': yrs_code
        }

        # Convert lists to comma-separated strings
        for key, value in st.session_state["user_characteristics"].items():
            if isinstance(value, list):
                st.session_state["user_characteristics"][key] = ";".join(value)

        print("\n1.", st.session_state["user_characteristics"])

        st.write("#### Choose a recommendation type ^")


# Sidebar form for entering values for salary prediction
def show_salary_prediction_form():
    
    
    with st.sidebar.form(key='salary_prediction_form'):
        age = st.number_input("Enter your age", step=1)
        years_code = st.number_input("Enter your years of coding experience", step=1)
        work_exp = st.number_input("Enter your work experience", step=1)

        submit_salary = st.form_submit_button(label='Predict')

    if submit_salary:
        
        predicted_salary = salary.predict_salary(age, years_code, work_exp)
        
        st.write("### Predicted Yearly Salary")
        st.markdown(f"<h1 style='text-align: center;'>${predicted_salary:.2f}</h1>", unsafe_allow_html=True)

       
# Create a horizontal layout
col1, col2, col3, col4, col5 = st.columns(5)


with col1:
    if st.button("Languages"):
        languages = recommendations.recommend_items(df=df,
                                                     user_characteristics=st.session_state["user_characteristics"],
                                                     desired_recommendation='language')
        display_recommendations(languages, 'language')

with col2:
    if st.button("Databases"):
        databases = recommendations.recommend_items(df=df,
                                                     user_characteristics=st.session_state["user_characteristics"],
                                                     desired_recommendation='database')
        display_recommendations(databases, 'database')

with col3:
    if st.button("Platforms"):
        platforms = recommendations.recommend_items(df=df,
                                                     user_characteristics=st.session_state["user_characteristics"],
                                                     desired_recommendation='platform')
        display_recommendations(platforms, 'platform')

with col4:
    if st.button("Webframes"):
        webframes = recommendations.recommend_items(df=df,
                                                     user_characteristics=st.session_state["user_characteristics"],
                                                     desired_recommendation='webframe')
        display_recommendations(webframes, 'webframe')

with col5:
    if st.button("Operating Systems"):
        op_sys = recommendations.recommend_items(df=df,
                                                  user_characteristics=st.session_state["user_characteristics"],
                                                  desired_recommendation='os')
        display_recommendations(op_sys, 'Operating System')



# Sidebar buttons for selecting functionality
selected_option = st.sidebar.radio("Select Functionality", ("Recommendations", "Salary Prediction"))

st.sidebar.write('### Enter user characteristics')

if selected_option == "Recommendations":
    show_recommendations_form()
elif selected_option == "Salary Prediction":
    show_salary_prediction_form()

