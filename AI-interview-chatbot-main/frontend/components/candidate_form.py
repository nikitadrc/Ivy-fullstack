# frontend/components/candidate_form.py

import streamlit as st
import re
from datetime import datetime
import pandas as pd

def validate_email(email):
    """Basic email validation using regex"""
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(pattern, email) is not None

def validate_form(name, email, experience, skills):
    """Validate form inputs and return error messages"""
    errors = []
    if not name.strip():
        errors.append("Name is required")
    if not validate_email(email):
        errors.append("Valid email is required")
    if not experience.strip():
        errors.append("Experience summary is required")
    if not skills.strip():
        errors.append("At least one skill is required")
    return errors

def candidate_form():
    """Render candidate information collection form with validation"""
    st.header("Candidate Information")
    
    with st.form("candidate_info"):
        # Personal Information
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Full Name*", placeholder="John Doe")
        with col2:
            email = st.text_input("Email*", placeholder="john.doe@example.com")
        
        # Professional Information
        experience = st.text_area(
            "Professional Experience*",
            placeholder="Briefly describe your professional background...",
            height=100
        )
        
        skills = st.text_input(
            "Technical Skills*",
            placeholder="Comma-separated list (e.g., Python, SQL, Project Management)"
        )
        
        # Optional Resume Upload (Bonus Feature)
        resume = st.file_uploader(
            "Upload Resume (Optional)",
            type=["pdf", "docx", "txt"],
            help="Supported formats: PDF, DOCX, TXT"
        )
        
        # Form Submission
        submitted = st.form_submit_button("Start Interview")
        
        if submitted:
            errors = validate_form(name, email, experience, skills)
            
            if errors:
                for error in errors:
                    st.error(error)
            else:
                # Process successful submission
                candidate_data = {
                    "name": name.strip(),
                    "email": email.lower().strip(),
                    "experience": experience.strip(),
                    "skills": [s.strip() for s in skills.split(",")],
                    "resume": resume,
                    "timestamp": datetime.now().isoformat()
                }
                
                # Save to session state
                st.session_state['candidate_data'] = candidate_data
                
                # Optional: Save to CSV/database
                save_candidate_data(candidate_data)
                
                # Show success and progress to next step
                st.success("Information submitted successfully!")
                st.session_state['form_complete'] = True
                st.experimental_rerun()
    
    # Show current progress
    if 'form_complete' in st.session_state and st.session_state.form_complete:
        st.write("")  # Empty space for layout

def save_candidate_data(data):
    """Save candidate data to CSV (example implementation)"""
    try:
        # Remove resume file object before saving to CSV
        save_data = data.copy()
        del save_data['resume']
        
        df = pd.DataFrame([save_data])
        df.to_csv('data/candidates.csv', mode='a', header=False, index=False)
    except Exception as e:
        st.error(f"Error saving candidate data: {str(e)}")

# Example usage (for testing)
if __name__ == "__main__":
    st.set_page_config(page_title="Candidate Form Demo")
    candidate_form()
    if 'candidate_data' in st.session_state:
        st.write("Collected Data:")
        st.json(st.session_state.candidate_data)
