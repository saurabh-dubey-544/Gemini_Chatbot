import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os
from PyPDF2 import PdfReader
from langchain_google_genai import ChatGoogleGenerativeAI,GoogleGenerativeAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
import faiss
from langchain.prompts import PromptTemplate
from langchain.chains.question_answering import load_qa_chain

#### Loading the environment variables---API
load_dotenv()

#### Configure the API Key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# -------------------------------------------------------------------------------------------------------------------------

#### Initializing the Models

# Text related tasks
model1 = genai.GenerativeModel("gemini-pro")
# Image data related tasks
model2 = genai.GenerativeModel("gemini-pro-vision")

# -------------------------------------------------------------------------------------------------------------------------

#### Initialize the Streamlit App
st.set_page_config(page_title="QnA Model" , page_icon=":page_with_curl:")

# -------------------------------------------------------------------------------------------------------------------------

#### Creating the App UI
# Title
st.title("QnA Model")
# Tabs
pro , pro_vision = st.tabs(["pro","vision_pro"])

# -------------------------------------------------------------------------------------------------------------------------

# Function to generate content
def generate_gemini_pro_response(user_input):
    response = model1.generate_content(user_input)
    return response.text

#### pro tab
user_input = pro.text_input("Ask any question" , key="pro_input" , placeholder="Provide the question here!")
submit = pro.button("Generate Response" , key="pro_button")

if submit:
    pro.success(generate_gemini_pro_response(user_input))

# -------------------------------------------------------------------------------------------------------------------------

# Function to handle image
def input_image_details(uploaded_file):
    if uploaded_file is not None:
        # Check if the uploaded file is an image
        if uploaded_file.type.startswith('image'):
            # Read the file into bytes
            bytes_data = uploaded_file.read()
            
            image_parts = [
                {
                    "mime_type": uploaded_file.type,
                    "data": bytes_data
                }
            ]
            return image_parts
        else:
            pro_vision.warning("Please upload a valid image file.")
    else:
        pro_vision.warning("No file uploaded.")

# Function to generate response
def generate_gemini_vision_response(input_text, image):
    response = model2.generate_content([input_text, image[0]])
    return response.text

def input_image_details(uploaded_file):
    if uploaded_file is not None:
        # Check if the uploaded file is an image
        if uploaded_file.type.startswith('image'):
            # Read the file into bytes
            bytes_data = uploaded_file.read()
            
            image_parts = [
                {
                    "mime_type": uploaded_file.type,
                    "data": bytes_data
                }
            ]
            return image_parts
        else:
            pro_vision.warning("Please upload a valid image file.")
    else:
        pro_vision.warning("No file uploaded.")
        
# Function to read the PDF, go through each and every page and extract the text and store it
def get_pdf_text(pdf_docs):       ## pdf_docs -- multiple pdf inputs by user
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
            
    return text

# Divide the text into Chunks
def get_text_chunks(text):
    text_splitter=RecursiveCharacterTextSplitter(chunk_size=10000 , chunk_overlap=1000)
    chunks = text_splitter.split_text(text)
    return chunks

# Converting the chunks into vectors
def get_vector_stores(chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_stores = faiss.FAISS.from_texts(chunks, embedding=embeddings)  ## FAISS will take all chunks and embed acccording to the embeddings specified
    # We can store these vector_stores in local or a database
    vector_stores.save_local("faiss_index")  ## Inside faiss_index folder, it'll store the embeddings
    
def get_conversational_chain():
    prompt_template = """
        Answer the question as detailed as possible from the provided context, make sure to provide all the details, if the answer is not in the provided context just say, "Answer is not available in the context", don't provide the wrong answer\n\n
        Context: \n {context} \n
        Question: \n {question} \n
        
        Answer:
    """
    
    model = ChatGoogleGenerativeAI(model="gemini-pro",temperature=0.3)
    prompt = PromptTemplate(template=prompt_template,input_variables=["context","question"])
    chain = load_qa_chain(model,chain_type="stuff",prompt=prompt)
    return chain

#### pro-vision tab
input_prompt = pro_vision.text_input("Enter Prompt:", key="vision_input")
uploaded_file = pro_vision.file_uploader("Upload any Image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Display image
    pro_vision.subheader("Uploaded Image")
    pro_vision.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
    
    
# Submit Button
submit = pro_vision.button("Generate Result",key="vision_button")

# Submit button is clicked
if submit:
    image_data = input_image_details(uploaded_file)
    if image_data:
        # Perform analysis
        response = generate_gemini_vision_response(input_prompt, image_data)
        
        # Display results
        pro_vision.subheader("Generated Result:")
        pro_vision.info(response)
