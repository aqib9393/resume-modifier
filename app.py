from flask import Flask, render_template, request, send_file
import subprocess
import os
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT
import io
import re
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Get the API key from the environment variable
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)
generation_config = {
        "temperature": 1,
        "top_p": 1,
        "top_k": 1,
    }

model = genai.GenerativeModel(model_name="gemini-1.5-flash",
                                  generation_config=generation_config)

latex_code = r"""
\documentclass[11pt,a4paper,sans]{moderncv}
\moderncvstyle{banking}
\usepackage{graphicx}
\usepackage{hyperref}
\moderncvcolor{black}
\nopagenumbers{}
\usepackage[utf8]{inputenc}
\usepackage{ragged2e}
\usepackage[scale=0.915]{geometry}
\usepackage{enumitem}
% \usepackage{fontawesome5}
\usepackage{hyperref}
\name{Muhammad}{Aqib}
\hypersetup{draft}  % Disable hyperlinks and interactive content

% Custom CV Entry Command
\newcommand*{\customcventry}[7][.13em]{%
\begin{tabular}{@{}l@{}}%
{\bfseries #4} {\itshape #3}%
\end{tabular}%
\hfill%
\begin{tabular}{r@{}}%
{\bfseries #5} {\itshape #2}%
\end{tabular}%
\ifx&#7&%
\else%
\vspace{#1}%
\par\small #7%
\fi%
\par\addvspace{#1}}

\begin{document}
\makecvtitle
\vspace*{-16mm}

\begin{center}
    \Large
  \textbf{AI Engineer} \\
  Berlin, Germany (willing to relocate) \\
  +49 152 25959918 \\ m.aqib9393@gmail.com \\
  \href{https://www.linkedin.com/in/muhammad-aqib-220251212/}{\textcolor{blue}{linkedin.com/in/muhammad-aqib-220251212}}  \\ 
  \href{https://github.com/aqib9393}{\textcolor{blue}{github.com/aqib9393}}
\end{center}

\section{Profile}
\justifying
AI Engineer with experience of building and deploying AI solutions, specializing in LLMs, Python and machine learning. Spearheaded the development of AI-powered chatbots and video generation systems, improving efficiency by up to 30\%. Developed predictive maintenance models that reduced downtime by 10\%. Willing to relocate.

\vspace*{3mm}

\section{Professional Experience}
\customcventry{October 2024 – January 2025}{\href{https://cognitiveitsolutions.ca/}{Cognitive IT Solutions}}{AI Engineer}{Karachi, PK}{}{
\begin{itemize}[leftmargin=0.6cm, label={\textbullet}]
    \item Diagnosed and resolved 10+ critical bugs in the video generation AI system within the first month; subsequently onboarded 3 new engineers and reduced average bug resolution time by 15\%.
    \item Implemented an LLM-driven resume analysis tool to improve candidate-job alignment and enhance ATS compatibility, resulting in a 15\% increase in qualified applicants.
\end{itemize}}

\customcventry{August 2023 – October 2024}{\href{https://www.digisofttrsol.com/}{Digisoft Transformation Solutions}}{AI Engineer}{Karachi, PK}{}{
\begin{itemize}[leftmargin=0.6cm, label={\textbullet}]
  \item Launched a RAG-based chatbot integrated with LLMs, resulting in a 25\% reduction in average support ticket resolution time and a 15-point surge in customer satisfaction scores within six months.
  \item Engineered AI-powered system using computer vision to extract serial numbers from electric meter images and achieved 95\% data capture rate, reducing data entry errors by 15\%.
  \item Engineered an AI-powered chatbot capable of translating user questions into SQL queries, enabling natural language access to database insights for non-technical users, improving data accessibility by 30\%.
\end{itemize}}

\customcventry{July 2022 – July 2023}{\href{http://virtudigital.net/}{Virtua Digital}}{Python Developer}{Remote (Mexico)}{}{
\begin{itemize}[leftmargin=0.6cm, label={\textbullet}]
  \item Automated ETL pipelines to enhance data flow reliability and reduce manual intervention by 35\%.
  \item Created RESTful APIs for internal tools, enabling seamless and consistent service integration and improving collaboration.
  \item Managed CI/CD workflows using GitHub Actions and AWS, improving deployment stability and delivery speed by 20\%.
\end{itemize}}

\customcventry{July 2021 - July 2021}{\href{https://thesparksfoundationsingapore.org/}{The Spark Foundation}}{Data Scientist Intern}{Remote (Singapore)}{}{
\begin{itemize}[leftmargin=0.6cm, label={\textbullet}]
    \item Streamlined data cleaning process using Pandas, resolved 100+ data quality issues, and improved model performance by 10\% in predicting customer churn rates.
\end{itemize}}

\customcventry{August 2020 - September 2020}{\href{https://thelionlead.com/}{The Lion Lead Digital World}}{Web Developer Intern}{Remote (Pakistan)}{}{
\begin{itemize}[leftmargin=0.6cm, label={\textbullet}]
    \item Optimized website performance by reducing load times and enhancing user experience, resulting in increased site engagement.
\end{itemize}}

\section{Education}
\textbf{Karachi Institute of Economics \& Technology (KIET)} \hfill \textbf{Karachi, PK} \\
\textit{Bachelor of Science Computer Science} \hfill \textit{January 2018 -- June 2022} \\

\section{Certifications}
\begin{itemize}[label=\textbullet, leftmargin=0.6cm]
  \item \href{https://saylaniwelfareusa.com/en/services/education/technical-education/saylani-mass-it-training}{AI \& Data Science}, Saylani Mass IT Training Program (2021)
  \item Analyzing and Visualizing Data with Microsoft Power BI, Enterprise DNA (2022)
\end{itemize}

\section{Projects}
\textbf{SafeBuild – AI for Construction Safety}
\begin{itemize}[leftmargin=0.6cm, label={\textbullet}]
  \item Deployed a computer vision model that identified 50+ daily safety gear violations by construction workers and integrated those detection with instant SMS alerts to site supervisors.
  \item Integrated computer vision outputs with alerting mechanisms to enforce site compliance.
\end{itemize}

\section{Skills}
\begin{itemize}[label=\textbullet, leftmargin=0.6cm]
  \item \textbf{Languages:} Python, R, SQL, Bash
  \item \textbf{AI/ML:} LLMs, YOLO, CNN, ANN, LSTMs, GRUs, ARIMA, Transfer Learning, Model Tuning,  Scikit-learn, TensorFlow, PyTorch, XGBoost, LightGBM,  MLOps, Model Versioning,  Predictive Analytics, Supervised/Unsupervised Learning, Generative AI
  \item \textbf{NLP/Frameworks:} LangChain, Hugging Face, OpenAI, SpaCy,  Feature Engineering, Prompt Engineering
  \item \textbf{Cloud Platforms:} AWS SageMaker, Azure ML, GCP Vertex AI, AWS (EC2, S3, Lambda)
  \item \textbf{Databases:} PostgreSQL, MongoDB, SQL Server
  \item \textbf{Data Engineering:} Pandas, NumPy, Airflow, Data Cleaning, Pipeline Automation
  \item \textbf{Tools:} MLflow, VSCode, Jupyter, Git
\end{itemize}

\section{Languages}
\begin{itemize}[label=\textbullet, leftmargin=0.6cm]
  \item \textbf{English (IELTS):} B2
  \item \textbf{German:} A1 (currently learning)
\end{itemize}

% Hidden comma separated tech keywords
\begin{itemize}[label={}, leftmargin=0.6cm]
    \item \textcolor{white}{\fontsize{4pt}{1pt}\selectfont 
    Python, R, pandas, scikit-learn, TensorFlow, PyTorch,  LLMs,  predictive analytics, supervised learning, unsupervised learning, generative AI,  time series analysis, distributional analysis,  AWS SageMaker, Azure ML, GCP Vertex AI, MLOps, model versioning, model monitoring, automated retraining pipelines, MLflow, data preparation, statistical analysis, machine learning model development, data cleaning, data pipelines,  business insights, data-driven decisions, process optimization,  experiment tracking, version control,  SQL, data visualization, business intelligence,  AI, ML,  data science
    }
\end{itemize}

\end{document}
"""

app = Flask(__name__)

def resumeModification(latex_code, jobDescription, model):
    try:
        prompt = f"""
            You are an intelligent AI assistant with deep understanding of resume optimization for Applicant Tracking Systems (ATS). Your task is to revise and enhance the provided LaTeX resume code to achieve the following goals:

            1. **Profile Section:** Rewrite the Profile section in no more than 3 concise, targeted sentences. Focus on autonomy, ownership, experience with investment or decision-support systems, and align it with the job description. Use impactful, engaging language optimized for ATS and recruiters.

            2. **Professional Experience Section:**
            - Add one bullet point to the two most recent roles related to the job description.
            - Modify the experience as per the provided job description.
            - Emphasize quantified impact (e.g., performance boosts, efficiency gains, cost/time savings).
            - Avoid redundancy and use synonyms where needed to improve ATS score.

            3. **Skills Section:**
            - Add all relevant skills from the job description.
            - Remove unrelated or non-aligned technologies/tools.
            - Ensure consistent categorization and formatting.

            4. **Projects Section:**
            - Add a new project that directly demonstrates alignment with the job role.
            - Emphasize technologies, outcomes, and relevance to job description responsibilities.

            5. **New Section:** Append a hidden LaTeX section titled `Hidden comma separated tech keywords` at the end. 
            - Include **all** job-relevant technical terms and keywords from the job description in a comma-separated format.
            - Ensure the section remains in the LaTeX code but does **not** appear in the compiled PDF.

            6. **Formatting Fixes:**
            - Ensure that no section overlaps between pages (e.g., content from Certificates or Projects breaking across pages).
            - Escape all percentages using `\\%` to ensure LaTeX compiles properly.

            7. **Important Constraints:**
            - Do **not** modify or remove the **Language Skills** section.
            - Do **not** change the structure, section order, layout, or design of the original LaTeX template.
            - Return only the updated LaTeX code as plain text. **Do not** include any explanation, markdown, or extra content.

            8. **ATS Optimization:**
            - Ensure the final LaTeX resume is **highly ATS optimized** with a target score of **95\\% or more**.
            - Focus on clear, keyword-rich phrasing, consistent formatting, and impactful metrics.
            - Avoid word repetition; use professional synonyms and ensure linguistic diversity.

            Use the following LaTeX resume code and job description to generate the updated LaTeX document.

            LaTeX Resume Code:
            {latex_code}

            Job Description:
            {jobDescription}
            """
        print("Going for generating the latex")
        response = model.generate_content(prompt)
        print("latex code generated ")
        return response.text.replace("`", "").replace("latex", "").strip()
    except Exception as e:
        print("error ", e)

def generateCoverLetter(leatexCode, jobDescription, model):
    prompt = f"""
        You are an AI assistant tasked with writing a professional, formal, and concise cover letter for a job application.

        ### Rules:
        - Begin the letter with "Dear Hiring Manager,"
        - Do NOT include any placeholder text like "[Platform where you saw the advertisement]" or any text inside square brackets.
        - Do NOT include any contact details such as phone number, email, LinkedIn, or GitHub in the letter.
        - Do NOT repeat contact details at the end — assume they are already included in the resume or email.
        - ONLY use information explicitly present in the resume and job description.
        - If company name or HR manager is not mentioned in the job description, omit them.
        - Use a confident and enthusiastic tone.
        - Make the letter personalized and relevant to the job.
        - Write the complete cover letter below.

        ### Resume Latex code:
        {leatexCode}

        ### Job Description:
        {jobDescription}

        ### Output:
        Write the full cover letter here with no placeholder or dummy content.
        """
    response = model.generate_content(prompt)
    return response.text.strip()

@app.route("/", methods=["GET", "POST"])
def index():
    cover_letter = ""
    pdf_path = "AqibAIEngineer.pdf"

    if request.method == "POST":
        job_desc = request.form.get("jobDescription", "")

        if not job_desc.strip():
            return render_template("index.html", error="Job description is required.", pdf_exists=False)

        try:
            modified_latex = resumeModification(latex_code, job_desc, model)

            with open("AqibAIEngineer.tex", "w", encoding="utf-8") as f:
                f.write(modified_latex)

            subprocess.run(["pdflatex", "-interaction=nonstopmode", "AqibAIEngineer.tex"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            cover_letter_text = generateCoverLetter(modified_latex, job_desc, model)

            buffer = io.BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=40, leftMargin=40, topMargin=60, bottomMargin=40)

            styles = getSampleStyleSheet()
            header_style = ParagraphStyle('Header', parent=styles['Normal'], fontName='Times-Roman', fontSize=12, leading=14, alignment=TA_LEFT)
            justified_style = ParagraphStyle('Justify', parent=styles['Normal'], fontName='Times-Roman', fontSize=12, leading=16, alignment=TA_JUSTIFY)

            flowables = []
            header_lines = [
                "Muhammad Aqib",
                "Berlin, Germany (willing to relocate)",
                "+49 152 25959918",
                "m.aqib9393@gmail.com",
                '<a href="https://linkedin.com/in/muhammad-aqib-220251212">linkedin.com/in/muhammad-aqib-220251212</a>',
                '<a href="https://github.com/aqib9393">github.com/aqib9393</a>'
            ]
            for line in header_lines:
                flowables.append(Paragraph(line, header_style))
            flowables.append(Spacer(1, 24))

            for para in cover_letter_text.strip().split('\n'):
                if para.strip():
                    flowables.append(Paragraph(para.strip(), justified_style))
                    flowables.append(Spacer(1, 12))

            doc.build(flowables)

            with open('cover_letter.pdf', 'wb') as f:
                f.write(buffer.getvalue())

            header_lines = [re.sub(r'<a[^>]*>(.*?)</a>', r'\1', line) for line in header_lines]
            cover_letter =  "\n".join(header_lines) + "\n\n" + cover_letter_text

        except Exception as e:
            return render_template("index.html", error=f"An error occurred: {str(e)}", pdf_exists=False)

    return render_template("index.html", cover_letter=cover_letter, pdf_exists=os.path.exists(pdf_path))

@app.route("/download_resume")
def download_resume():
    return send_file("AqibAIEngineer.pdf", as_attachment=True)

@app.route("/download_cover_letter")
def download_cover_letter():
    return send_file("cover_letter.pdf", as_attachment=True)

if __name__ == "__main__":
    app.run()
