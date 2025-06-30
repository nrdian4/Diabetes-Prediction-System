import pickle
import streamlit as st
from streamlit_option_menu import option_menu
import base64
import os
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# Get Base64 Background Image
def get_base64_of_background_image(image_path):
    try:
        if os.path.exists(image_path):
            with open(image_path, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode()
            return f"data:image/png;base64,{encoded_string}"
    except Exception as e:
        st.warning(f"Background image not found: {image_path}")
    return None

# Set Page Configuration
def set_page_config():
    st.set_page_config(page_title="diaScan - Your Health Partner", layout="wide")

# CSS sytles
def set_custom_css(background_image_path, show_background=True):
    css = """
        <style>
        /*--Form--*/
        /* Customize selectbox dropdown */
        div[data-baseweb="select"] > div {
            background-color: white !important;
       }
       
        /* Customize number input fields */
        input[type="number"] {
            background-color: white !important;
        }
        
        /*--Home Page--*/
        .main-container {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100px;
        }
        
        .content-box {
            display: flex;
            justify-content: center;
            margin-top: 60px;
        }
        
        /*Prediction Page*/  
        .stButton {
            display: flex;
            justify-content: center;
        }
        
        .stButton > button {
            background-color: #4da6ff;
            color: white;
            padding: 0.5rem 3rem;
            font-size: 1.2rem;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .stButton > button:hover {
            background-color: #4da6ff;
            opacity: 0.8;
            color: #000000;
        }
        
        div[data-testid="column"] {
            display: flex;
            justify-content: center;
        }
        
        /*Text Styling*/
        .stMarkdown p {
            font-size: 1.1rem;
            line-height: 1.6;
            margin-bottom: 1rem;
        }
        
        .stMarkdown ul {
            font-size: 1.1rem;
            line-height: 1.6;
        }
        
        .stMarkdown ul ul {
            font-size: 1.1rem;
        }
        
        .stMarkdown li {
            margin-bottom: 0.5rem;
        }
        
        .stMarkdown strong {
            font-weight: 600;
        }
        
        /*--Educational Support Page--*/
        
        /*Styles for Global statistics*/
        .stats-column-container{
            display: flex;
            justify-content: space-around;
            flex-wrap: wrap;
            margin-bottom: 100px;
            
        }
        .stat-circle {
            background-color: #C94F7C;
            border-radius: 50%;
            width: 200px;
            height: 200PX;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
            padding: 20px;
            color: white;
            margin: 15px 0;
        }
        .stat-circle.blue {
            background-color: #008B9C;
        }
        .stat-circle.purple {
            background-color: #9C4F7F;
        }
        .big-number {
            font-size: 2.7rem;
            font-weight: bold;
            margin: 0;
        }
        .stat-text {
            font-size: 0.9rem;
            margin: 5px 0;
            line-height: 1.2;
            padding: 0 10px;
        }
        
        /* Educational page text styling */
        .main-title {
            font-size: 2.3rem;
            font-weight: bold;
            color: #262730;
            margin-bottom: 1rem;
        }
        .stat-description {
            font-size: 1.1rem;
            color: #333;
            text-align: justify;
            margin: 10px 0;
            max-width: 600px;
        }
        .stat-list{
            text-align: justify;
            margin-bottom: 70px;
        }
        
        /*Styles for Malaysia statistics*/
        .stApp {
            background-color: #EEF3F7;
        }
        .custom-box {
            background-color: white;
            padding: 15px;
            border-radius: 15px;
            box-shadow: rgba(0, 0, 0, 0.1) 0px 4px 12px;
            height: 100%;
            margin-bottom: 5px;
        }
        
        """
    
    if show_background:
            with open(background_image_path, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode()
                
            css += f"""
            [data-testid="stAppViewContainer"] {{
                background-image: url("data:image/png;base64,{encoded_string}");
                background-size: cover;
                background-position: center;
            }}
            """
    
    css += "</style>"
    st.markdown(css, unsafe_allow_html=True)
    

# Home page
def home_page():
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("<div style='margin-bottom: 400px;'></div>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("Predict Now", key="predict_button"):
                st.session_state.page = 'predict'
                st.rerun()
            

# Prediction Page
def predict_diabetes():
    st.title("Predict Diabetes Risk")
    
    # Set a two colums for form
    with st.form("risk_assessment_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            gender = st.selectbox('Gender', ["Female", "Male"], index=None, placeholder="Select gender")
            age = st.number_input('Age', min_value=0, max_value=200, step=1)
            hypertension = st.radio('Do you have hypertension?', ["No", "Yes"], index=0)
            heart_disease = st.radio('Do you have heart disease?', ["No", "Yes"], index=0)
        
        with col2:
            smoking_history = st.selectbox('Smoking History', 
                ["Never", "Not Current", "Former", "Current"],
                index=None, placeholder="Select smoking history")
            bmi = st.number_input('Body Mass Index (BMI)', min_value=0.0, max_value=100.0, step=0.1)
            hba1c_level = st.number_input('HbA1c Level (%)', min_value=0.0, max_value=20.0, step=0.1)
            blood_glucose = st.number_input('Blood Glucose Level (mg/dL)', min_value=0, max_value=1000, step=1)
        
        submitted = st.form_submit_button("Get Prediction")
        
        if submitted:
            if not all([gender, smoking_history]) or not all(x > 0 for x in [age, bmi, hba1c_level, blood_glucose]):
                st.error("Please fill in all fields before submitting.")
            else:
                    # Convert inputs to match model (Convert categorical columns to numerical values)
                    gender_map = {"Female": 0, "Male": 1, "Other": 2}
                    smoking_map = {"Never": 0, "Current": 2, "Former": 3, "Not Current": 5}
                    
                    input_data = [
                        gender_map[gender],
                        age,
                        1 if hypertension == "Yes" else 0,
                        1 if heart_disease == "Yes" else 0,
                        smoking_map[smoking_history],
                        bmi,
                        hba1c_level,
                        blood_glucose
                    ]
                    
                    # Load the model and StandardScaler
                    model_path = r"C:\Users\nordi\OneDrive - Universiti Teknologi MARA\Documents\DEGREE SEM 6\CSP650\FRONT END\XGBoost-sav\diabetes_prediction_model.sav"
                    scaler_path = r"C:\Users\nordi\OneDrive - Universiti Teknologi MARA\Documents\DEGREE SEM 6\CSP650\FRONT END\XGBoost-sav\diabetes_prediction_scaler.sav"
                    
                    diabetes_model = pickle.load(open(model_path, "rb"))
                    scaler = pickle.load(open(scaler_path, "rb"))
                    
                    # Standardize the input data
                    input_data_standardized = scaler.transform([input_data])
                    
                    # Make prediction
                    diabetes_prediction = diabetes_model.predict(input_data_standardized)
                    
                    # Display results
                    if diabetes_prediction[0] == 1:
                        st.markdown("""
                            <div style="background-color: #ffebee; padding: 20px; border-radius: 10px; margin-top: 20px;">
                                <h2 style="color: #c62828;">Higher Risk Detected</h2>
                                <p style="color: #c0392b;">Disclaimer: This result is an estimate of your diabetes risk. Please consult a doctor for medical advice and regular check-ups.</p>
                                <p>Based on the provided information, you may have an elevated risk of developing diabetes.</p>
                                <h3>Recommended Next Steps:</h3>
                                <ol>
                                    <li>Consult a Healthcare Professional
                                        <ul>
                                            <li>Schedule an appointment with a doctor for further testing.</li>
                                        </ul>
                                    </li>
                                    <li>Implement Lifestyle Changes
                                        <ul>
                                            <li><strong>Lose Extra Weight:</strong> Aim to lose 7% to 10% of body weight if overweight. Set realistic goals for gradual weight loss (1-2 pounds per week).</li>
                                            <li><strong>Increase Physical Activity:</strong> Engage in at least 150 minutes of moderate aerobic exercise weekly such as brisk walk, swimming, biking or running, and incorporate strength training exercises at least 2-3 times a week.</li>
                                        </ul>
                                    </li>
                                    <li>Adopt a Healthy Diet
                                        <ul>
                                            <li>Focus on a diet rich in fruits, vegetables, whole grains, and lean proteins.</li>
                                            <li>Avoid processed foods, sugary beverages, and unhealthy fats</li>
                                        </ul>
                                    </li>
                                </ol>
                            </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown("""
                           <div style="background-color: #e8f5e9; padding: 20px; border-radius: 10px; margin-top: 20px; width: 100%;">
                                <h2 style="color: #2e7d32;">Lower Risk Detected</h2>
                                <p>Based on the provided information, your risk of developing diabetes appears to be lower.</p>
                                <h3>Recommended Next Steps:</h3>
                                <ol>
                                    <li>Stay Physically Active
                                        <ul>
                                            <li>Maintain a routine of regular exercise, aiming for at least 150 minutes of moderate aerobic activity weekly, and include strength training.</li>
                                        </ul>
                                    </li>
                                    <li>Regular Health Check-ups
                                        <ul>
                                            <li>Schedule regular check-ups with your doctor to keep track of your health status.</li>
                                        </ul>
                                    </li>
                                    <li>Eat a Balanced Diet
                                        <ul>
                                            <li>Keep a diet rich in whole, unprocessed foods, with a focus on fiber-rich fruits, vegetables, and healthy fats.</li>
                                            <li>Limit sugar and refined carbohydrates.</li>
                                        </ul>
                                    </li>
                                </ol>
                            </div>

                        """, unsafe_allow_html=True)

# Malaysia Statistic Dashboard
def create_malaysia_dashboard():
        
    # Create four columns for all elements
    col_total, col_type1, col_type2, col_others = st.columns([1, 1, 1, 1])
    
    # Total patients box
    with col_total:
        st.markdown("""
            <div class="custom-box">
                <h1 style="text-align: center; margin: 0; font-size: 2.5rem;">1,956,151</h1>
                <p style="text-align: center; margin: 0; color: #666;">total diabetes patients in Malaysia</p>
            </div>
        """, unsafe_allow_html=True)
    
    # Diabetes Types data
    diabetes_types = [
        ("Type 1 Diabetes\nMellitus", 0.47),
        ("Type 2 Diabetes\nMellitus", 99.48),
        ("Others", 0.05)
    ]
    
    # Create donut charts for each type
    for col, (diabetes_type, percentage) in zip([col_type1, col_type2, col_others], diabetes_types):
        with col:
            st.markdown(f"""
                <div class="custom-box">
                    <p style="text-align: center; margin-bottom: 10px; font-size: 0.9rem;">{diabetes_type}</p>
                </div>
            """, unsafe_allow_html=True)
            
            fig = go.Figure(data=[go.Pie(
                labels=['', diabetes_type],
                values=[100-percentage, percentage],
                hole=.7,
                marker_colors=['#E8E8E8', '#1f77b4'] if 'Type 2' in diabetes_type else ['#E8E8E8', '#89CFF0']
            )])
            
            fig.update_layout(
                annotations=[dict(text=f'{percentage}%', x=0.5, y=0.5, font_size=20, showarrow=False)],
                showlegend=False,
                height=200,
                margin=dict(l=0, r=0, t=30, b=30),
                paper_bgcolor='white'
            )
            
            st.plotly_chart(fig, use_container_width=True)

    # Add some vertical spacing before the next row
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Gender and Ethnic distribution in the second row
    col1, col2 = st.columns(2)
    
    # Gender Distribution
    with col1:
        st.markdown(f"""
            <div class="custom-box">
                <p style="text-align: center; margin-bottom: 10px; font-size: 1rem;">Gender Distribution</p>
            </div>
        """, unsafe_allow_html=True)
        gender_data = pd.DataFrame({
            'Gender': ['Men', 'Women'],
            'Percentage': [42.92, 57.08]
        })
        
        fig_gender = px.pie(
            gender_data,
            values='Percentage',
            names='Gender',
            color_discrete_sequence=['#86eae9', '#3b6696']
        )
        fig_gender.update_traces(textposition='inside', textinfo='percent+label')
        fig_gender.update_layout(
            paper_bgcolor='white',
            margin=dict(l=0, r=0, t=30, b=30),
            height=300
        )
        st.plotly_chart(fig_gender, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Ethnic Distribution
    with col2:
        st.markdown(f"""
            <div class="custom-box">
                <p style="text-align: center; margin-bottom: 10px; font-size: 1rem;">Ethnicity Distribution</p>
            </div>
        """, unsafe_allow_html=True)
        ethnic_data = pd.DataFrame({
            'Ethnicity': ['Malay', 'Chinese', 'Indian', 'Others'],
            'Percentage': [60.13, 19.27, 12.58, 8.02]
        })
        
        fig_ethnic = px.bar(
        ethnic_data,
        x='Ethnicity',
        y='Percentage',
        color='Ethnicity', 
        color_discrete_sequence=['#00589c', '#19aade', '#1ac9e6', '#6dfdd2']
        )
        fig_ethnic.update_layout(
            xaxis_title="Ethnicity",
            yaxis_title="Percentage (%)",
            showlegend=False,
            paper_bgcolor='white',
            plot_bgcolor='white',
            margin=dict(l=10, r=10, t=30, b=30),
            height=300
        )
        st.plotly_chart(fig_ethnic, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        


# Educational page
def educational_page():
    st.markdown("""
        <link href='https://cdn.jsdelivr.net/npm/boxicons@2.1.1/css/boxicons.min.css' rel='stylesheet'>
    """, unsafe_allow_html=True)
    
    # Main Title for Diabetes Overview
    st.markdown("<h1 class='main-title'>What is Diabetes?</h1>", unsafe_allow_html=True)
    
    st.write("""
             Diabetes is a chronic, metabolic disease characterized by elevated levels of blood glucose (or blood sugar), 
                which leads over time to serious damage to the heart, blood vessels, eyes, kidneys, and nerves.
            
    """)

    # Types of Diabetes
    st.markdown("<h1 class='main-title' style='margin-top: 40px'>Types of Diabetes</h1>", unsafe_allow_html=True)
    
    # Type 1 Diabetes
    st.markdown("<h3 class='category-title'>Type 1 Diabetes</h3>", unsafe_allow_html=True)
    st.markdown("""
                <ul>
                  <li>Type 1 diabetes was previously called juvenile diabetes.</li>
                  <li>It occurs when the immune system targets and destroys insulin-producing beta cells in the pancreas.</li>
                  <li>This leads to an insulin deficiency, a hormone critical for:
                    <ul>
                      <li>Allowing glucose to enter cells.</li>
                      <li>Providing cells with energy.</li>
                    </ul>
                  </li>
                  <li>Currently, type 1 diabetes:
                    <ul>
                      <li>Cannot be prevented.</li>
                      <li>Has no cure.</li>
                      <li>Requires daily insulin prescriptions.</li>
                    </ul>
                  </li>
                  <li>Risk factors for type 1 diabetes include:
                    <ul>
                      <li>Family history of diabetes.</li>
                      <li>Certain genetic factors.</li>
                    </ul>
                  </li>
                  <li>Anyone can be diagnosed with type 1 diabetes, regardless of lifestyle, fitness level, or body weight.</li>
                </ul>
                """, unsafe_allow_html=True)

    # Type 2 Diabetes
    st.markdown("<h3 class='category-title'>Type 2 Diabetes</h3>", unsafe_allow_html=True)
    st.markdown("""
                <ul>
                  <li>Type 2 diabetes typically develops in adulthood.</li>
                  <li>Unlike type 1 diabetes, where the body doesn't produce enough insulin:
                    <ul>
                      <li>Type 2 diabetes occurs when the body continues to make insulin but is unable to use it effectively, a condition called <strong>insulin resistance</strong>.</li>
                      <li>Over time, the demand for insulin overwhelms the pancreas’ ability to produce it, leading to an <strong>insulin deficiency</strong>.</li>
                    </ul>
                  </li>
                  <li>It is a persistent medical condition that results in:
                    <ul>
                      <li>Excessive blood sugar levels.</li>
                      <li>Potential complications affecting the heart, nerves, and immune system.</li>
                    </ul>
                  </li>
                  <li>Risk factors for developing type 2 diabetes include:
                    <ul>
                      <li>Family history of diabetes.</li>
                      <li>Obesity.</li>
                      <li>A sedentary lifestyle.</li>
                      <li>A poor diet.</li>
                      <li>Certain ethnicities.</li>
                    </ul>
                  </li>
                </ul>
                """, unsafe_allow_html=True)      

    # Gestational Diabetes
    st.markdown("<h3 class='category-title'>Gestational Diabetes</h3>", unsafe_allow_html=True)
    st.markdown("""
                <ul>
                  <li>Gestational diabetes is a temporary form of diabetes that develops during pregnancy.</li>
                  <li>Similar to other diabetes types, it alters the body's glucose metabolism.</li>
                  <li>Excessive blood sugar levels can harm both maternal and fetal health.</li>
                  <li>Gestational diabetes typically resolves after childbirth but:
                    <ul>
                      <li>It significantly increases the risk of developing type 2 diabetes later in life.</li>
                    </ul>
                  </li>
                </ul>
                """, unsafe_allow_html=True)
    
    # Symptoms
    st.markdown("<h1 class='main-title' style='margin-top: 40px'>Symptoms</h1>", unsafe_allow_html=True)
    st.markdown("""
            <p>Diabetes symptoms vary depending on how high your blood sugar is. 
            Some patients, particularly those with prediabetes, gestational diabetes, or type 2 diabetes, may not have symptoms. 
            Type 1 diabetes symptoms appear fast and are more severe.</p>
        
            <p>Some of the symptoms of type 1 diabetes and type 2 diabetes are:</p>
            
            <ul>
                <li>Feeling thirstier than usual.</li>
                <li>Urinating frequently.</li>
                <li>Losing weight unintentionally.</li>
                <li>Feeling tired and weak.</li>
                <li>Feeling irritable or experiencing other mood changes.</li>
                <li>Having blurry vision.</li>
                <li>Having slow-healing sores.</li>
                <li>Getting a lot of infections, such as gum, skin and vaginal infections.</li>
            </ul>
        """, unsafe_allow_html=True)



    # Global Diabetes Statistics
    st.markdown("<h1 class='main-title' style='margin-top: 50px;'>Global Diabetes Statistics</h1>", unsafe_allow_html=True)
    st.markdown("""
        <div class='stats-column-container'>
            <div class='stat-circle' style="background-color: #C94F7C;">
                <div class='big-number'>537m</div>
                <div class='stat-text'>adults with diabetes globally</div>
            </div>
            <div class='stat-circle blue' >
                <div class='big-number'>3 in 4</div>
                <div class='stat-text'>adults with diabetes live in low- and middle-income countries.</div>
            </div>
            <div class='stat-circle purple'>
                <div class='big-number'>6.7m</div>
                <div class='stat-text'>deaths due to diabetes in 2021</div>
            </div>
        </div>
        
        <div class="stat-list">
            <p><i class='bx bx-world'></i> <strong> 537 million</strong> adults (20-79 years) are living with diabetes. This number is predicted to increase to <strong> 643 million </strong> by 2030 and <strong> 783 million </strong> by 2045.</p>
            <p><i class='bx bxs-building-house'></i> <strong>Over 3 in 4</strong> adults with diabetes live in low- and middle-income countries.</p>
            <p><i class='bx bxs-heart'></i> Diabetes caused <strong>6.7 million</strong> deaths in 2021.</p>
            <p><i class='bx bx-money-withdraw'></i> Diabetes caused at least <strong>USD 966 billion</strong> dollars in health expenditure – a 316% increase over the last 15 years.</p>
        </div>
    """, unsafe_allow_html=True)

    # Malaysian Statistics
    st.markdown("<h1 class='main-title'>Malaysian Diabetes Statistics in 2023</h1>", unsafe_allow_html=True)
    create_malaysia_dashboard()

    
def main():
    
    # Background image for home page
    background_image_path = r"C:\Users\nordi\OneDrive - Universiti Teknologi MARA\Documents\DEGREE SEM 6\CSP650\USER INTERFACE\1.3.png"
    risk_assessment_background_path = r"C:\Users\nordi\OneDrive - Universiti Teknologi MARA\Documents\DEGREE SEM 6\CSP650\USER INTERFACE\risk_assessment(3).png"

    set_page_config()
    
    if 'page' not in st.session_state:
        st.session_state.page = 'home'
    
    if st.session_state.page == 'home':
        set_custom_css(background_image_path, show_background=True)
        home_page()
    else:
        set_custom_css(risk_assessment_background_path, show_background=True)
        
        # Navigation Bar
        with st.sidebar:
            selected = option_menu(
                'Welcome to diaScan - Your Health Partner',
                ['Predict Diabetes Risk', 'Educational Support', 'Back to Home'],
                icons=['clipboard-data', 'house'],
                menu_icon="list",
                default_index=0,
                styles={
                    "container": {"background-color": "#cce7f7"},
                    "nav-link": {
                        "font-size": "16px", 
                        "--hover-color": "#4da6ff",
                        "background-color": "#another_color"
                    },
                    "nav-link-selected": {"background-color": "#4da6ff"},
                }
            )
        
        if selected == 'Predict Diabetes Risk':
            predict_diabetes()
        elif selected == 'Educational Support':
            educational_page()
        elif selected == 'Back to Home':
            st.session_state.page = 'home'
            st.rerun()


if __name__ == "__main__":
    main()