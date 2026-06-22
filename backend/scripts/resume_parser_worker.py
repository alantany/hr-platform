import os
import sys
import time
import json
import asyncio
from pathlib import Path

# Add project root to path
BASE_DIR = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(BASE_DIR))

import pdfplumber
import docx
from openai import OpenAI
from dotenv import load_dotenv

from backend.app.database import SessionLocal
from backend.app.models import ResumeParseTask, Candidate
from sqlalchemy import text

load_dotenv(os.path.join(BASE_DIR, '.env'))

OPENROUTER_BASE_URL = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "openai/gpt-4o")

client = OpenAI(
    base_url=OPENROUTER_BASE_URL,
    api_key=OPENROUTER_API_KEY,
)

PROMPT_FILE_PATH = os.path.join(BASE_DIR, "outputs", "resume_parsing_prompt.md")

def get_system_prompt() -> str:
    with open(PROMPT_FILE_PATH, "r", encoding="utf-8") as f:
        return f.read()

def extract_text_from_file(file_path: str) -> str:
    ext = file_path.lower().split('.')[-1]
    text_content = ""
    if ext == 'pdf':
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text_content += page_text + "\n"
    elif ext in ['doc', 'docx']:
        doc = docx.Document(file_path)
        for para in doc.paragraphs:
            text_content += para.text + "\n"
    else:
        raise ValueError(f"Unsupported file format: {ext}")
    return text_content

def call_llm_for_json(resume_text: str) -> dict:
    if not OPENROUTER_API_KEY or OPENROUTER_API_KEY == "your_api_key_here":
         raise ValueError("OpenRouter API Key is not configured. Please check your .env file.")
         
    system_prompt = get_system_prompt()
    
    response = client.chat.completions.create(
        model=OPENROUTER_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"请解析以下简历文本并严格返回要求的 JSON 格式：\n\n{resume_text}"}
        ],
        response_format={"type": "json_object"},
        temperature=0.1
    )
    
    raw_response = response.choices[0].message.content.strip()
    # clean markdown wrapper if present
    if raw_response.startswith("```json"):
        raw_response = raw_response[7:]
    if raw_response.startswith("```"):
         raw_response = raw_response[3:]
    if raw_response.endswith("```"):
         raw_response = raw_response[:-3]
         
    return json.loads(raw_response.strip())

def process_pending_tasks():
    db = SessionLocal()
    try:
        tasks = db.query(ResumeParseTask).filter(ResumeParseTask.status == "PENDING").all()
        if not tasks:
            print("No pending tasks.")
            return

        for task in tasks:
            print(f"Processing task {task.id} for download_id {task.resume_download_id}...")
            task.status = "PROCESSING"
            db.commit()
            
            try:
                # 1. Fetch file_path from recruit.resume_downloads
                sql = text("SELECT candidate_name, file_path FROM recruit.resume_downloads WHERE id = :id")
                result = db.execute(sql, {"id": task.resume_download_id}).mappings().first()
                if not result:
                    raise Exception(f"resume_download_id {task.resume_download_id} not found.")
                
                file_path = result["file_path"]
                # Assuming file_path is like 'data/resumes/test/数据开发工程师'
                # Prepend 'recruit/' if it's a relative path to root
                full_path = os.path.join(BASE_DIR, "recruit", file_path)
                
                # Check if file exists. If it's a directory (no extension), try to find a file
                # Sometimes file_path is a directory or misses extension in DB. 
                if os.path.isdir(full_path):
                     files = os.listdir(full_path)
                     if not files:
                         raise Exception(f"Directory is empty: {full_path}")
                     full_path = os.path.join(full_path, files[0]) # pick first file
                elif not os.path.exists(full_path):
                     # try to glob it if extension is missing
                     import glob
                     matches = glob.glob(f"{full_path}.*")
                     if matches:
                         full_path = matches[0]
                     else:
                         raise Exception(f"File not found: {full_path}")
                
                print(f"Reading file: {full_path}")
                
                # 2. Extract text
                resume_text = extract_text_from_file(full_path)
                
                # 3. Call LLM
                print("Calling LLM...")
                parsed_data = call_llm_for_json(resume_text)
                
                # 4. Save to Candidate
                # If name is empty, fallback to candidate_name from DB
                candidate_name = parsed_data.get("name") or result["candidate_name"] or "未知候选人"
                
                # Create candidate
                candidate = Candidate(
                    name=candidate_name,
                    phone=parsed_data.get("phone") or "",
                    email=parsed_data.get("email") or "",
                    gender=parsed_data.get("gender") or "",
                    birth_date=parsed_data.get("birth_date") or "",
                    age=parsed_data.get("age") or 0,
                    city=parsed_data.get("city") or "",
                    hukou_location=parsed_data.get("hukou_location") or "",
                    family_status=parsed_data.get("family_status") or "",
                    job_status=parsed_data.get("job_status") or "离职",
                    onboard_cycle=parsed_data.get("onboard_cycle") or "",
                    expected_salary=parsed_data.get("expected_salary") or "",
                    job_intention=parsed_data.get("job_intention") or "",
                    education=parsed_data.get("education") or "",
                    experience_years=parsed_data.get("experience_years") or 0,
                    current_title=parsed_data.get("current_title") or "",
                    core_value=parsed_data.get("core_value") or "",
                    certificates=parsed_data.get("certificates") or "",
                    education_detail=parsed_data.get("education_detail") or "",
                    work_history=parsed_data.get("work_history") or "",
                    project_history=parsed_data.get("project_history") or "",
                    source="AI解析",
                    status="未锁定"
                )
                
                db.add(candidate)
                db.flush() # get candidate.id
                
                task.candidate_id = candidate.id
                task.status = "SUCCESS"
                print(f"Task {task.id} success. Candidate ID: {candidate.id}")
                
            except Exception as e:
                task.status = "FAILED"
                task.error_message = str(e)
                print(f"Task {task.id} failed: {e}")
            
            db.commit()

    finally:
        db.close()

if __name__ == "__main__":
    print("Starting Resume Parser Worker...")
    # Just run once for now. Can be placed in a while loop later.
    process_pending_tasks()
    print("Done.")
