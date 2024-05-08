from dotenv import load_dotenv

load_dotenv() ## load all the environment variables
import traceback
import streamlit as st
import os
import google.generativeai as genai
from PIL import Image
from Assessmentgenerator.utils import read_file,get_table_data
import pandas as pd

os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

## Function to load Google Gemini Pro Vision API And get response

def get_gemini_repsonse(prompt,cohort,test_type,text,number,subject, tone):
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content([prompt,text,test_type,number,cohort,subject,tone])
    return response.text


##initialize our streamlit app

st.set_page_config(page_title="Assessment Generator")

st.header("Assessment Generator")
uploaded_file=st.file_uploader("Uplaod a PDF or txt file")

#Subject
subject=st.text_input("Insert Subject",max_chars=20)

student_class=st.text_input("Class",max_chars=20)

Test_type=st.text_input(" Type of test ",key="input")

# Quiz Tone
tone=st.text_input("Complexity Level Of Questions", max_chars=20, placeholder="Simple")

number=st.number_input("no of question", min_value=3, max_value=50)

submit=st.button("Generate Assessment")

input_prompt="""
Text:{text}
You are an expert in the field of Measurement and evaulation, and also an expert examiner. You are good at setting test material like\

1. Achievement Tests: These tests are designed to measure a person's knowledge or skills in a particular subject or area. They typically assess how well a person has learned the material presented in a specific course or educational program. Achievement tests often have predetermined criteria or standards against which a person's performance is compared. Examples include standardized tests like the SAT (Scholastic Assessment Test) or ACT (American College Testing) which measure academic achievement in various subjects.

2. Objective Tests: Objective tests are assessments where responses are scored using predetermined criteria, typically with clear right or wrong answers. These tests are designed to measure specific knowledge or skills and are often administered in a multiple-choice format. Objective tests aim to provide an unbiased and standardized way of evaluating a person's understanding of a subject. Examples include standardized assessments like the GRE (Graduate Record Examination) or MCAT (Medical College Admission Test).

3. Essay Tests: Essay tests require students to generate their own responses to questions or prompts. These responses are typically longer and more open-ended, allowing for greater depth of understanding and expression of ideas. Essay tests assess a person's ability to critically analyze information, formulate arguments, and communicate effectively in written form. They are commonly used in subjects where subjective evaluation is necessary, such as literature, history, and philosophy.

4. Aptitude Tests: Aptitude tests are designed to measure a person's innate abilities or potential to perform well in certain areas. These tests assess cognitive abilities, skills, and talents that are not necessarily related to specific knowledge acquired through education or training. Aptitude tests aim to predict how well an individual is likely to perform in future tasks or roles. Examples include the SAT Subject Tests, which measure aptitude in specific academic subjects, or the ASVAB (Armed Services Vocational Aptitude Battery), which assesses aptitude for military occupations.

5. Intelligence Tests: Intelligence tests, also known as IQ (Intelligence Quotient) tests, are assessments designed to measure a person's cognitive abilities, including reasoning, problem-solving, memory, and linguistic skills. These tests aim to quantify a person's intellectual abilities relative to others in a population. Intelligence tests provide scores that are often used for educational placement, career assessment, and identifying intellectual disabilities or giftedness. Examples include the Stanford-Binet Intelligence Scales and the Wechsler Adult Intelligence Scale (WAIS).
Given the above text,it is your job to \
create an student assessment based on the {test_type} for a given {subject} for students in {class} and also set the difficulty level base on {tone}. 
Make sure the questions are not repeated and check all the questions to be conforming the text as well.
Make sure to format your response to the right assessment type \
Ensure to make use of the specified {number} of questions and also provide the correct answers for each question.
Follow the format below for each test

Certainly! Here's a basic format for each type of test:

1. Achievement Test Format:
   - Test Title: [Title of the Achievement Test]
   - Subject: [Subject Area Being Assessed]
   - Instructions: [Clear Instructions for Test Takers]
   - Sections: 
     - Section 1: [Description of Section 1 Content]
     - Section 2: [Description of Section 2 Content]
     - ...
   - Question Types: [Types of Questions, e.g., Multiple Choice, Short Answer, Essay]
   - Scoring: [Explanation of How the Test Will Be Scored]

2. Objective Test Format:
   - Test Title: [Title of the Objective Test]
   - Subject: [Subject Area Being Assessed]
   - Instructions: [Clear Instructions for Test Takers]
   - Question Format: 
     - Question 1: [Question Text]
       - Option A: [Option A Text]
       - Option B: [Option B Text]
       - ...
     - Question 2: [Question Text]
       - Option A: [Option A Text]
       - Option B: [Option B Text]
       - ...
   - Scoring: [Explanation of How the Test Will Be Scored]

3. Essay Test Format:
   - Test Title: [Title of the Essay Test]
   - Subject: [Subject Area Being Assessed]
   - Instructions: [Clear Instructions for Test Takers]
   - Essay Prompts: 
     - Prompt 1: [Essay Prompt]
     - Prompt 2: [Essay Prompt]
     - ...
   - Scoring Rubric: [Criteria for Grading Essays]

4. Aptitude Test Format:
   - Test Title: [Title of the Aptitude Test]
   - Subject: [Subject Area Being Assessed]
   - Instructions: [Clear Instructions for Test Takers]
   - Sections:
     - Section 1: [Description of Section 1 Content]
     - Section 2: [Description of Section 2 Content]
     - ...
   - Question Types: [Types of Questions, e.g., Verbal Reasoning, Numerical Reasoning]
   - Scoring: [Explanation of How the Test Will Be Scored]

5. Intelligence Test Format:
   - Test Title: [Title of the Intelligence Test]
   - Subject: [Subject Area Being Assessed (e.g., Cognitive Abilities)]
   - Instructions: [Clear Instructions for Test Takers]
   - Sections:
     - Section 1: [Description of Section 1 Content]
     - Section 2: [Description of Section 2 Content]
     - ...
   - Question Types: [Types of Questions, e.g., Verbal, Performance]
   - Scoring: [Explanation of How the Test Will Be Scored]

These formats provide a structured framework for designing and administering each type of test, ensuring clarity and consistency for both test creators and test takers.

"""

## If submit button is clicked

if submit and uploaded_file is not None and Test_type and subject and tone and number:
        with st.spinner("loading..."):
            try:
                text=read_file(uploaded_file)
                response=get_gemini_repsonse(input_prompt,student_class,Test_type,text,str(number),subject,tone)
                st.subheader("The Response is")
                st.write(response)
            except Exception as e:
                traceback.print_exception(type(e), e, e.__traceback__)
                st.error("Error")
