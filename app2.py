import streamlit as st
from PIL import Image
from datetime import datetime
import pytz
from prediction import load_model_and_labels, predict_flower
import webbrowser

#Page
st.set_page_config(
    page_title="Flower Power App",
    page_icon="🌼",
    layout="centered",
    initial_sidebar_state="expanded"
)

#Eastern time
def get_current_eastern_time():
    eastern = pytz.timezone("US/Eastern")
    return datetime.now(eastern).strftime("%Y-%m-%d %H:%M:%S")


if st.button("Go to Main Page"):
    webbrowser.open_new_tab("https://flowerpowerweb-y5xthaukjkfnapp8zymvysg.streamlit.app")
    
#two modes 
if "theme" not in st.session_state:
    st.session_state.theme = "light"

if st.button("Toggle Night Mode" if st.session_state.theme == "light" else "Toggle Light Mode"):
    st.session_state.theme = "dark" if st.session_state.theme == "light" else "light"

if st.session_state.theme == 'light':
    background_gradient = 'linear-gradient(to bottom right, #e0f7fa, #f0f8ff)'
    text_color = '#4CAF50'
    background_color = '#ffffffcc'
else:
    background_gradient = 'linear-gradient(to bottom right, #000000, #434343)'
    text_color = '#ffffff'
    background_color = '#000000cc'



#themes
background_gradient = (
    "linear-gradient(to bottom right, #e0f7fa, #f0f8ff)"
    if st.session_state.theme == "light"
    else "linear-gradient(to bottom right, #000000, #434343)"
)
text_color = "#4CAF50" if st.session_state.theme == "light" else "#ffffff"

st.markdown(
    f"""
    <style>
    .main {{ background: {background_gradient}; padding: 20px; border-radius: 15px; }}
    .stButton>button {{ background-color: {text_color}; color: white; border-radius: 8px; font-size: 16px; }}
    img.uploaded-image {{ border: 5px solid {text_color}; border-radius: 15px; }}
    </style>
    """,
    unsafe_allow_html=True,
)

# app title
st.markdown(
    f"""
    <div style="text-align: center; background: #ffffffcc; padding: 20px; border-radius: 15px;">
        <h1 style="color: {text_color}; font-size: 3em;">Flower Power App 🌼</h1>
        <p style="color: #555;">Upload a flower image</p>
        <p style="color: #777;">Current Eastern Time: {get_current_eastern_time()}</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Developer Info"])

if page == "Home":
    #upload images
    uploaded_file = st.file_uploader("Choose an image file", type=["jpg", "jpeg", "png"])

    if uploaded_file:
        try:
            image = Image.open(uploaded_file)
            
            st.image(image, caption="Uploaded Image", use_container_width=True)

           
            with st.spinner("Loading model......🌼  "):
                model, class_labels = load_model_and_labels()

            
            with st.spinner("Identifying the flower...🌼"):
                predicted_label, confidence = predict_flower(image, model, class_labels)

            # Displayresults
            if predicted_label:
                st.success(f"Predicted Flower: {predicted_label} with {confidence:.2f}% confidence.")
            else:
                st.warning("The flower cannot be confidently recognized. Please try another image.")
        except Exception as e:
            st.error(f"An unexpected error occurred: {str(e)}")
    else:
        st.info("Please upload an image to get started.")
elif page == "Developer Info":
    st.markdown(
        f"""
        <div style="background: #ffffffcc; padding: 20px; border-radius: 15px;">
            <h2 style="color: {text_color};">Developer Team</h2>
            <ul style="list-style-type: none;">
                <li>Imrul</li>
                <li>Mansur</li>
                <li>Zahava</li>
                <li>Jessica/li>
            </ul>
        </div>

         <div style="margin-top: 20px;">
                <p style="font-size: 1em; color: #999;">Model: Our Own model.</p>
                <p style="font-size: 1em; color: #999;">Website designed by the team. Check out other work: <a href="https://flowerpowerweb-y5xthaukjkfnapp8zymvysg.streamlit.app" style="color: #999; text-decoration: underline;">here</a></p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
