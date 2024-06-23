from openai import OpenAI
import base64
from pdf2image import convert_from_bytes
from io import BytesIO
from fpdf import FPDF

client = OpenAI(api_key='YOUR_API_KEY')

def get_base64_pdf_image(resume_image):    
    # Assuming we want the first page
    first_page_image = resume_image[0]

    # Save the image to a BytesIO object
    buffered = BytesIO()
    first_page_image.save(buffered, format="JPEG")
    
    # Get the base64 encoded string
    base64_encoded = base64.b64encode(buffered.getvalue()).decode('utf-8')
    
    # Return as data URL
    return f"data:image/jpeg;base64,{base64_encoded}"


def generate_questions(job_posting, base64_img_data_url):
    if job_posting == "None":
        prompt = "You are a job recruiter. You are given a resume and your job is to provide a list of questions that you want to ask based on the resume that you are given, and sample responses the interviewee can provide based on this resume. Please have each sample response under each potential question."
    else:
        prompt = "You are a recruiter who is hiring for a given job based on its description. You are given a resume and your job is to provide a list of questions that you want to ask based on the resume that you are given and sample responses that the interviewee can provide. Please have each sample response under each potential question. Also consider the job description, and your company knowledge which you will understand via a web search. Start off with general questions first, like 'tell me about yourself'. Try to simulate real-life interview questions as much as possible with the context of the job. You need to understand the company and what they do via a web search."
    
    response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": prompt},
                        {"role": "user", "content": [{"type": "text", "text": f"Link: {job_posting}"},
                                                    {"type": "image_url", 
                                                     "image_url": {"url": base64_img_data_url}}]}],
                    max_tokens=1000, temperature=0.8)
    summary = response.choices[0].message.content.strip()
    return summary

def generate_cover_letter(job_posting, base64_img_data_url):
    if job_posting == "None":
        prompt = "Please write a 1 page cover letter for this resume. Be sure to showcase how the skills and experiences highlighted in the resume are able to demonstrate personal skills such as communication, leadership, teamwork, learning, and/or personal growth."
    else:
        prompt = "Please write a 1 page cover letter for this resume. Also consider the job description from the given job posting, and your company knowledge which you will understand via a web search. Focus on how the skills and experiences in the resume as applicable for the company in question, their product and industry, and their missions. Place additional emphasis on the company itself and its industry. Also include how the skills and experiences highlighted in the resume are able to demonstrate personal skills such as communication, leadership, teamwork, learning, and/or personal growth."
    
    response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": prompt},
                        {"role": "user", "content": [{"type": "text", "text": f"Link: {job_posting}"},
                                                    {"type": "image_url", 
                                                     "image_url": {"url": base64_img_data_url}}]}],
                    max_tokens=1000, temperature=0.8)
    summary = response.choices[0].message.content.strip()
    return summary

def generate_pdf(text, file_name):
    """Generate an example pdf file and save it to example.pdf"""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, text)

    if file_name == "None":
        new_file_name = "cover_letter.pdf"
    elif file_name[-4:] == ".pdf":
        new_file_name = file_name
    else:
        new_file_name = file_name + '.pdf'

    pdf.output(new_file_name)
    return new_file_name







