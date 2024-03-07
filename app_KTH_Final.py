from pathlib import Path
import weaviate
import weaviate.classes as wvc
import streamlit as st
import requests
import base64
from add_data_in_batch import COLLECTION_NAME

client = weaviate.connect_to_local()

# Streamlit App
st.set_page_config(page_title="Multi-Modal RAG(MM-RAG) using Vector DB and GPT4 Vision", layout="wide", page_icon=":owl:")

GPT4_VISION_API_URL = "https://api.openai.com/v1/chat/completions"

logo_path = Path("assets/OWL.png")
title_cols = st.columns([0.25, 0.75])
with title_cols[0]:
    st.write("")
    st.image(logo_path.read_bytes(), width=150)
with title_cols[1]:
    st.title("Multi-Modal RAG(MM-RAG) using Vector DB and GPT4 Vision")

st.subheader("Instructions")
st.write(
    """
    Search the dataset by uploading an image or entering free text.
    The model is multi-lingual as well - try searching in different languages!
    This model used the following 50+ languages to align the vector spaces: 
    ar, bg, ca, cs, da, de, el, es, et, fa, fi, fr, fr-ca, gl, gu, he, hi, 
    hr, hu, hy, id, it, ja, ka, ko, ku, lt, lv, mk, mn, mr, ms, my, nb, nl, 
    pl, pt, pt, pt-br, ro, ru, sk, sl, sq, sr, sv, th, tr, uk, ur, vi, zh-cn, zh-tw.

    (Note: If you enter both, only the image will be used.)
    """
)

st.subheader("Search the dataset")

srch_cols = st.columns(2)
with srch_cols[0]:
    search_text = st.text_area(label="Search by text")
with srch_cols[1]:
    img = st.file_uploader(label="Search by image", type=["jpg", "jpeg", "png"])

# Your OpenAI API key
api_key = st.text_input("Enter your OpenAI API Key", type="password")
prompt= st.text_area(label="Prompt to ask GPT V4 Vision Model")
def generate_description_from_image_gpt4(prompt, image64):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image64}"  # base64 encoded image
                        }
                    }
                ]
            }
        ],
        "max_tokens": 300
    }

    response_oai = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

    if response_oai.status_code == 200:
        response_json = response_oai.json()
        if 'choices' in response_json and len(response_json['choices']) > 0:
            result = response_json['choices'][0]['message']['content']
            print(f"Generated description: {result}")
            return result
        else:
            print("No 'choices' key in the response or 'choices' list is empty.")
            return "No description available."
    else:
        print(f"Error in API response. Status code: {response_oai.status_code}")
        if response_oai.text:
            print(f"Error message: {response_oai.text}")
        return "Failed to get description from the API."

if search_text != "" or img is not None:
    mm_coll = client.collections.get(COLLECTION_NAME)

    if img is not None and api_key:
        st.image(img, caption="Uploaded Image", use_column_width="auto")
        imgb64 = base64.b64encode(img.getvalue()).decode()

        response = mm_coll.query.near_image(
            near_image=imgb64,
            return_properties=[
                "filename",
            ],
            return_metadata=wvc.query.MetadataQuery(distance=True),
            limit=6,
        )

    else:
        response = mm_coll.query.near_text(
            query=search_text,
            return_properties=[
                "filename",
            ],
            return_metadata=wvc.query.MetadataQuery(distance=True),
            limit=6,
        )

    st.subheader("Results found:")
    for i, r in enumerate(response.objects):
        if i % 3 == 0:
            with st.container():
                columns = st.columns(3)
                st.divider()
        with columns[i % 3]:
            st.write(r.properties["filename"])

            imgpath = Path("data/images") / r.properties["filename"]
            img = imgpath.read_bytes()
            st.image(img)

            st.write(f"Distance: {r.metadata.distance:.3f}")

            if api_key:
                imgb64 = base64.b64encode(img).decode()
                if prompt:
                    description = generate_description_from_image_gpt4(prompt, imgb64)
                    st.write(f"Description: {description}")
                    pass
                else:
                    st.warning("Please enter a prompt to ask the GPT V4 Vision Model.")
                

st.markdown("""
    <style>
        .reportview-container {
            margin-top: -2em;
        }
        #MainMenu {visibility: hidden;}
        .stDeployButton {display:none;}
        footer {visibility: hidden;}
        #stDecoration {display:none;}
    </style>
""", unsafe_allow_html=True)