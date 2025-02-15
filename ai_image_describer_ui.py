import streamlit as st
import google.generativeai as genai
from PIL import Image
import os
API_KEY = os.getenv("API_KEY")  # for  Secure api keys
# this api key is securely deployed in streamlit community cloud, it will automaticaly inject key to the environment




if not API_KEY:
    st.error("API Key is missing. Please set it in your environment variables.")
else:
    genai.configure(api_key=API_KEY)

sys_prompt = """You are an AI model that answers users' questions about an uploaded image.
Please provide precise, structured, and well-labeled answers with clear details.
But initially you should describe the picture which uploaded and give answer then you have to ask more about any questions that left."""


model = genai.GenerativeModel(model_name="gemini-1.5-flash", system_instruction=sys_prompt)

# Streamlit UI Setup
st.set_page_config(page_title="AI Image Identifier", layout="wide")

st.markdown("<h1 style='text-align: center; color: #0078D7;'>AI Image Identifier</h1>", unsafe_allow_html=True)

# File Upload
uploaded_file = st.file_uploader(" Upload an image", type=["jpg", "png", "jpeg"])

if uploaded_file:
    col1, col2 = st.columns(2)
    
    # Display Image
    with col1:
        st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)

    
    
    image = Image.open(uploaded_file)
    

    # User Input for Question
    with col2:
        st.markdown("### 📝 Ask a Question About the Image:")
        prompt = st.text_area("Type your question below 👇", height=100)

        if st.button("Analyze Image"):
            if prompt:
                with st.spinner("Identifying details... Please wait."):
                    try:
                        response = model.generate_content([image, prompt])
                        
                        # Progress Bar Effect
                        progress = st.progress(0)
                        for percent in range(100):
                            progress.progress(percent + 1)
                        
                        st.success("✅ Analysis Complete!")
                        st.subheader("AI Response:")
                        st.write(response.text)
                    except Exception as e:
                        st.error(f"❌ An error occurred: {e}")
            else:
                st.warning("⚠️ Please enter a question before analyzing.")

# Footer
st.markdown("<br><hr>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Powered by Gemini AI | Built with Streamlit</p>", unsafe_allow_html=True)
