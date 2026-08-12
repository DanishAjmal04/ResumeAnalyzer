# AI Resume Analyzer Pro

<div align="center">
  <img src="Logo/Logo Ai.png" alt="AI Resume Analyzer Pro Logo" width="180" />
</div>

AI Resume Analyzer Pro is a Streamlit web application that analyzes uploaded resumes, predicts a suitable career field, estimates experience level, scores the resume, recommends skills and courses, and generates tailored cover letters.

## 📋 Overview

This project is designed to help job seekers understand how strong their resume is and what they can improve. Users can upload a PDF resume and get instant AI-assisted insights such as:

- Resume parsing and preview
- Skill extraction
- Career field prediction
- Experience level estimation
- Resume scoring
- Skill and course recommendations
- Cover letter generation
- Admin analytics and candidate screening

## 📸 Screenshots

<div align="center">
  <img src="assets/screenshot1.png" alt="Home Page" width="800" />
  <p><em>Home Page</em></p>

  <img src="assets/screenshot2.png" alt="Resume Analysis" width="800" />
  <p><em>Resume Analysis</em></p>

  <img src="assets/screenshot3.png" alt="Admin Dashboard" width="800" />
  <p><em>Admin Dashboard</em></p>
</div>

## 🚀 Features

- Upload resumes in PDF format
- Extract name, email, contact number, skills, and page count
- Predict the most suitable career field from extracted skills
- Estimate experience level using a trained model with fallback rules
- Score resumes with a trained scoring model
- Recommend skills for career growth
- Suggest learning resources and courses
- Generate a personalized cover letter using OpenAI when an API key is available
- View candidate analytics in the admin dashboard
- Screen candidates against a job description using semantic similarity
- Store resume data in MySQL, with automatic fallback to SQLite if MySQL is unavailable

## 🛠️ Tech Stack

- **Backend and UI:** Streamlit
- **Language:** Python
- **PDF Parsing:** pdfminer3, pyresparser fallback
- **Machine Learning:** scikit-learn, joblib
- **Data Handling:** pandas, numpy
- **Database:** MySQL or SQLite fallback
- **NLP and Embeddings:** sentence-transformers
- **AI Cover Letters:** OpenAI API

## ⚙️ How It Works

1. The user uploads a PDF resume.
2. The app extracts text and structured data from the file.
3. The resume is analyzed to predict a career field and experience level.
4. The resume score is calculated.
5. The app recommends skills and courses based on the predicted field.
6. The user can generate a tailored cover letter.
7. The admin dashboard can review stored candidates and run AI-based screening.



## 📬 Contact & Support

For questions, suggestions, or collaboration, feel free to reach out:

- GitHub: [DanishAjmal04](https://github.com/DanishAjmal04)
- Email: danishajmal56da@gmail.com
