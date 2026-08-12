from openai import OpenAI
from config import OPENAI_API_KEY


class CoverLetterGenerator:
    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None
        self.template = """Write a professional cover letter for {name} applying for the {job_title} position at {company}.

        Candidate Background:
        - Experience Level: {experience_level}
        - Key Skills: {skills}
        - Additional Recommended Skills: {recommended_skills}

        Job Requirements:
        {job_description}

        The letter should:
        1. Be addressed to the hiring manager
        2. Highlight relevant skills and experience
        3. Show enthusiasm for the role and company
        4. Be concise (under 400 words)
        5. Use professional business letter format
        """

    def _fallback_cover_letter(self, resume_data: dict, job_description: dict) -> str:
        name = resume_data.get("name", "Candidate")
        title = job_description.get("title", "the role")
        company = job_description.get("company", "the company")
        experience_level = resume_data.get("experience_level", "Professional")
        skills = ", ".join(resume_data.get("skills", [])) or "relevant technical and communication skills"
        recommended_skills = ", ".join(resume_data.get("recommended_skills", [])) or "industry-aligned competencies"
        description = job_description.get("description", "")

        return f"""Dear Hiring Manager,

I am writing to express my interest in the {title} position at {company}. I am {name}, and I bring a strong background as a {experience_level} professional with a focus on {skills}. My experience has prepared me to contribute effectively to your team and to support the goals of the organization.

I am particularly motivated by the opportunity to apply my skills in {recommended_skills}. I believe my background, combined with my work ethic and ability to learn quickly, would allow me to make a positive impact in this role. {description[:200] + ('...' if len(description) > 200 else '')}

I would welcome the opportunity to discuss how my experience and skills align with your needs. Thank you for your time and consideration. I look forward to the possibility of speaking with you.

Sincerely,
{name}
"""

    def generate(self, resume_data: dict, job_description: dict) -> str:
        if not self.client:
            return self._fallback_cover_letter(resume_data, job_description)

        prompt = self.template.format(
            name=resume_data.get("name", "the candidate"),
            job_title=job_description.get("title", ""),
            company=job_description.get("company", ""),
            experience_level=resume_data.get("experience_level", ""),
            skills=", ".join(resume_data.get("skills", [])),
            recommended_skills=", ".join(resume_data.get("recommended_skills", [])),
            job_description=job_description.get("description", "")
        )

        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=1000
        )

        return response.choices[0].message.content