import streamlit as st
from utils import *

st.title("Welcome to AceInterview!")

resume = st.file_uploader('Please upload your resume as a PDF', type="pdf")

if resume is not None:
    try:
        resume_image = convert_from_bytes(resume.read())
        if st.button("Preview resume"):
            st.image(resume_image)

    except Exception as e:
        st.error(f"Error reading resume file: {e}")

job_posting = st.text_input('Optional: upload a job posting you are interested in. To bypass this step, please write "None".') 

if resume is not None and job_posting != '':
    try:
        base64_img_data_url = get_base64_pdf_image(resume_image)
        action = st.radio('Select an option and hit "Begin"', ["Practice interview", "Generate sample questions and responses", "Write cover letter"],
                          captions = ["Speak live with an AI voice to simulate a virtual interview", "See what questions may come up based on your experience", "Write and download a personalized letter for this position"])
        
        if st.button("Begin"):
            if action == "Generate sample questions and responses":
                with st.spinner('Generating questions and responses...'):
                    summary =  generate_questions(job_posting, base64_img_data_url)
                    #st.subheader("Example questions and responses:")
                    st.write(summary)
            if action == "Write cover letter":
                with st.spinner('Writing custom cover letter...'):
                    summary = generate_cover_letter(job_posting, base64_img_data_url)
                        #st.subheader("Cover Letter:")
                    st.write(summary)

                    new_file_name = generate_pdf(summary, "cover_letter.pdf")
                    with open(new_file_name, "rb") as f:
                        st.download_button("Download PDF", f, new_file_name)
                    
    
    except Exception as e:
        st.error(f"Please upload a resume: {e}")
