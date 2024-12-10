import streamlit as st
from openai import OpenAI
from datetime import datetime
import json
from boostingInfo import boosting_info

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

# Function to get response from OpenAI
def get_openai_response(question):
    if not st.session_state.openai_api_key:
        st.error("Please enter your password")
        return None
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a data science expert. Provide answers in JSON format with 'reasoning' and 'answer' as keys. Keep responses clear and concise."},
                {"role": "user", "content": question}
            ],
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        st.error(f"Error calling OpenAI API: {str(e)}")
        return None

# Add new note section
st.subheader("Add Notes")
with st.form("note_form"):
    question = st.text_area("Ad a new note", height=100)
    submitted = st.form_submit_button("Save Note")
    
    if submitted and question:
        response = get_openai_response(question)
        if response:
            new_note = {
                "title": f"Q: {question[:50]}...",
                "date": datetime.now().strftime("%Y-%m-%d"),
                "category": "Data Science",
                "question": question,
                "reasoning": response["reasoning"],
                "answer": response["answer"]
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