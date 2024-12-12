import streamlit as st
import google.generativeai as genai
from apikey import google_gemini_api_key, openai_api_key
from openai import OpenAI
from streamlit_carousel import carousel
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize clients with API keys from environment variables
client = OpenAI(api_key=openai_api_key)
genai.configure(api_key=google_gemini_api_key)

# Set app to wide mode
st.set_page_config(layout='wide')

# Image Slider for the blog
single_image = dict(
    title="",
    text="",
    interval=None,
    img="",
)

# Create the model
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    generation_config=generation_config,
)

# Set app logo
logo_path = r"C:\Users\Kevin\OneDrive - Cal Poly Pomona\Documents\Personal Projects\AI Blogging Assistant\Draftly Logo.webp"  # Replace with the correct path

# Center the logo using columns
col1, col2, col3 = st.columns([1, 2, 1])  # Adjust column widths as needed
with col1:
    st.write("")  # Empty column for spacing
with col2:
    st.image(logo_path, width=200)  # Center the image
with col3:
    st.write("")  # Empty column for spacing

# Title of the app
st.title("Draftly: Your AI Blogging Assistant")

# Create a subheader
st.subheader("Craft the personal blog for your fans with the help of Draftly")

# Sidebar for user input
with st.sidebar:
    st.title("Input your Details")
    st.subheader("Enter Details for the Blog you want to generate...")

    # Blog Title
    blog_title = st.text_input("Blog Title")
    # Keywords input
    keywords = st.text_area("Keywords (separated by comma)")
    # Number of Words
    num_words = st.slider("Number of words", min_value=250, max_value=1000, step=250)
    # Number of images
    num_images = st.number_input("Number of Images", min_value=1, max_value=5, step=1)
    # Prompt
    prompt_parts = [
        f"Generate a comprehensive, engaging blog post relevant to the given title \"{blog_title}\" and keywords \"{keywords}\". The blog should be approximately {num_words} words in length, suitable for an online audience. Ensure the content is original, informative, and maintains a consistent tone throughout.",
    ]
    
    # Submit_button
    submit_button = st.button("Generate Blog")

if submit_button:
    response = model.generate_content(prompt_parts)

    images_gallery = []
    for i in range(num_images):
        image_response = client.images.generate(
            model="dall-e-3",
            prompt=f"Generate a Blog Post Image on the title: {blog_title}",
            size="1024x1024",
            quality="standard",
            n=1,
        )
        new_image = single_image.copy()
        new_image["title"] = f"Image {i+1}"
        new_image["text"] = f"{blog_title}"
        new_image["img"] = image_response.data[0].url
        images_gallery.append(new_image)

    carousel(items=images_gallery, width=1)

    st.title("YOUR BLOG POST:")
    st.write(response.text)
