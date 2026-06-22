from backend.app.database import SessionLocal
from backend.app.models import Candidate
from backend.app.schemas import CandidateOut

db = SessionLocal()
c = db.query(Candidate).filter(Candidate.name == '姜曼').first()
if c:
    try:
        out = CandidateOut.model_validate(c)
        print(out.model_dump_json(indent=2))
    except Exception as e:
        print("Error validating:", e)
else:
    print("Not found")
