from backend.app.database import SessionLocal
from sqlalchemy import text
db = SessionLocal()
res = db.execute(text("SELECT last_value FROM candidates_id_seq;")).fetchone()
print("Sequence candidates_id_seq last_value:", res)
