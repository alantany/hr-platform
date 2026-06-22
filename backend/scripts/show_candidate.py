import sys
import json
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(BASE_DIR))
from backend.app.database import SessionLocal
from backend.app.models import Candidate

db = SessionLocal()
c = db.query(Candidate).filter(Candidate.id == 10021).first()
if c:
    data = {
        "name": c.name,
        "phone": c.phone,
        "email": c.email,
        "gender": c.gender,
        "age": c.age,
        "birth_date": c.birth_date,
        "education": c.education,
        "experience_years": c.experience_years,
        "city": c.city,
        "hukou_location": c.hukou_location,
        "expected_salary": c.expected_salary,
        "job_status": c.job_status,
        "onboard_cycle": c.onboard_cycle,
        "current_title": c.current_title,
        "core_value": c.core_value,
        "certificates": c.certificates,
        "education_detail": c.education_detail,
        "work_history": c.work_history,
        "project_history": c.project_history
    }
    print(json.dumps(data, indent=2, ensure_ascii=False))
else:
    print("Not found")
db.close()
