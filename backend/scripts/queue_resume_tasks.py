import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(BASE_DIR))

from backend.app.database import SessionLocal
from backend.app.models import ResumeParseTask
from sqlalchemy import text

def queue_all():
    db = SessionLocal()
    try:
        # Get all resume_downloads that are not queued yet
        sql = text("""
            SELECT id FROM recruit.resume_downloads 
            WHERE id NOT IN (SELECT resume_download_id FROM resume_parse_tasks)
        """)
        results = db.execute(sql).fetchall()
        
        queued = 0
        for row in results:
            download_id = row[0]
            task = ResumeParseTask(
                resume_download_id=download_id,
                status="PENDING"
            )
            db.add(task)
            queued += 1
            
        db.commit()
        print(f"Successfully queued {queued} new resume parse tasks.")
        
    finally:
        db.close()

if __name__ == "__main__":
    queue_all()
