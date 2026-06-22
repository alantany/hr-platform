from backend.app.database import SessionLocal
from backend.app.models import Candidate

db = SessionLocal()
c = db.query(Candidate).filter(Candidate.name == '姜曼').first()
if c:
    print(f"Name: {c.name}")
    print(f"Birth Date: {c.birth_date}")
    print(f"Hukou: {c.hukou_location}")
    print(f"Family: {c.family_status}")
    print(f"Edu Detail: {c.education_detail}")
    print(f"Core Value: {c.core_value}")
else:
    print("Not found")
