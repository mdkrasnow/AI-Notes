import streamlit as st
from openai import OpenAI
from datetime import datetime
import json
import base64
from boostingInfo import boosting_info
from typing import Optional, Any, Dict

# Set page configuration
st.set_page_config(
    page_title="Data Science Notes App",
    page_icon="📝",
    layout="wide"
)

# Initialize OpenAI client
# Check if API key exists in session state
if 'openai_api_key' not in st.session_state:
    st.session_state.openai_api_key = None

# API key input in sidebar
with st.sidebar:
    api_key = st.text_input("Password:", type="password")
    if api_key:
        st.session_state.openai_api_key = api_key
        client = OpenAI(api_key=api_key)

# Add a title
st.title("📝 AC 209 Notes")

st.markdown("""
    <style>
    /* Make the text input field blend with background but invisible text */
    .stTextArea textarea {
        background-color: rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(0, 0, 0, 0.2);
        border-radius: 4px;
        color: transparent !important; /* Make text invisible */
        caret-color: transparent !important; /* Hide caret */
        font-size: 14px;
    }
    
    /* Subtle hover effect */
    .stTextArea textarea:hover {
        border-color: rgba(0, 0, 0, 0.4);
        background-color: rgba(240, 242, 246, 0.2);
    }
    
    /* Focus state */
    .stTextArea textarea:focus {
        border-color: rgba(49, 51, 63, 0.6);
        box-shadow: none;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state for notes if it doesn't exist
if 'notes' not in st.session_state:
    st.session_state.notes = [
        {
            "title": "Sample Data Science Note",
            "date": "2024-12-10",
            "category": "Data Science",
            "question": "What is the difference between bias and variance?",
            "reasoning": "This is a fundamental concept in machine learning that helps understand model performance.",
            "answer": "Bias is the error due to oversimplified assumptions in the learning algorithm. Variance is the error due to too much complexity in the learning algorithm."
        }
    ]
def get_openai_response(question: str, image_data: bytes = None) -> Dict[str, Any]:
    """
    Get a response from OpenAI's API, handling both text and image inputs.
    
    Args:
        question (str): The question or prompt to send to the API
        image_data (bytes, optional): Raw image data to be processed
        
    Returns:
        Dict[str, Any]: Parsed JSON response with 'reasoning' and 'answer' keys
        None: If there's an error or no API key is set
    """
    if not st.session_state.openai_api_key:
        st.error("Please enter your password")
        return None

    try:
        # Prepare messages list
        messages = [
            {
                "role": "system",
                "content": "You are a data science expert. Provide answers in JSON format with 'reasoning' and 'answer' as keys. Keep responses clear and concise."
            }
        ]

        # Prepare user message content
        user_content = [{"type": "text", "text": question}]

        # If image is provided, encode and add it to the message
        if image_data:
            base64_image = base64.b64encode(image_data).decode('utf-8')
            user_content.append({
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_image}"
                }
            })

        # Add user message to messages list
        messages.append({
            "role": "user",
            "content": user_content
        })

        # Make API call
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            response_format={"type": "json_object"}
        )

        # Parse and return response
        return json.loads(response.choices[0].message.content)

    except Exception as e:
        st.error(f"Error calling OpenAI API: {str(e)}")
        return None

# Helper function to safely handle image uploads
def process_uploaded_image(uploaded_file) -> Optional[bytes]:
    """
    Process an uploaded image file and return its bytes.
    
    Args:
        uploaded_file: Streamlit uploaded file object
        
    Returns:
        bytes: Raw image data if successful
        None: If processing fails
    """
    try:
        if uploaded_file is None:
            return None
            
        return uploaded_file.read()
    except Exception as e:
        st.error(f"Error processing uploaded image: {str(e)}")
        return None
    
# Add new note section
st.subheader("Add Notes")
with st.form("note_form"):
    question = st.text_area("Search in notes:", height=68)
    uploaded_image = st.file_uploader("Paste or upload an image:", type=["png", "jpg", "jpeg"])
    submitted = st.form_submit_button("Save Note")
    
    if submitted and (question or uploaded_image):
        image_data = None
        if uploaded_image is not None:
            image_data = process_uploaded_image(uploaded_image)
        
        response = get_openai_response(question, image_data=image_data)
        if response:
            display_title = f"Q: {question[:50]}..." if question else "Q: [Image Attached]"
            new_note = {
                "title": display_title,
                "date": datetime.now().strftime("%Y-%m-%d"),
                "category": "Data Science",
                "question": question if question else "[No question, image only]",
                "reasoning": response.get("reasoning", "No reasoning provided."),
                "answer": response.get("answer", "No answer provided.")
            }
            st.session_state.notes.insert(0, new_note)  # Add to beginning of list
            st.success("Note added successfully!")

# Sidebar for filtering
st.sidebar.header("Filters")

# Date filter
dates = list(set(note["date"] for note in st.session_state.notes))
selected_date = st.sidebar.selectbox(
    "Select Date",
    ["All"] + sorted(dates, reverse=True)
)

# Filter notes based on selection
filtered_notes = st.session_state.notes
if selected_date != "All":
    filtered_notes = [note for note in filtered_notes if note["date"] == selected_date]

# Display notes
st.subheader("Your Notes")
for note in filtered_notes:
    with st.expander(f"📝 {note['title']} - {note['date']}"):
        # Cornell Notes Section
        st.markdown("### Cornell Notes")
        st.write(note["question"])
        st.markdown("**Additional Context:**")
        st.markdown(boosting_info["cornell_notes"])
        
        # Background Information Section
        st.markdown("### Background Information")
        st.write(note["reasoning"])
        st.markdown("**Extended Background on Boosting:**")
        st.markdown(boosting_info["background"])
        
        # Conclusion Section
        st.markdown("### Conclusion")
        st.write(note["answer"])
        st.markdown("**Boosting Insights:**")
        st.markdown(boosting_info["conclusion"])
        
        st.divider()

# Add some statistics
st.sidebar.divider()
st.sidebar.subheader("Statistics")
st.sidebar.write(f"Total Notes: {len(st.session_state.notes)}")
st.sidebar.write(f"Filtered Notes: {len(filtered_notes)}")
