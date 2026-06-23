import os
import sys
import time
from pathlib import Path

# 确保 backend 可以导入
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from fastapi.testclient import TestClient
from pypdf import PdfReader
from reportlab.lib.pagesizes import A4
from backend.app.main import app, ROOT_DIR

def test_pdf_resume_export():
    with TestClient(app) as client:
        # 1. 登录
        login_res = client.post("/api/auth/login", json={"username": "admin", "password": "admin123"})
        assert login_res.status_code == 200
        token = login_res.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # 2. 获取候选人
        candidates = client.get("/api/candidates", headers=headers).json()
        assert len(candidates) > 0
        candidate = candidates[0]

        # 3. 模拟前端参数进行简历导出 (PDF格式)
        payload = {
            "candidate_id": candidate["id"],
            "candidate_name": candidate["name"],
            "company_name": "测试客户公司",
            "project_name": "测试招聘项目",
            "position_name": "测试职位",
            "format": "PDF",
            "watermarked": True,
            "exported_by": "admin"
        }

        response = client.post("/api/export-records", json=payload, headers=headers)
        assert response.status_code == 200
        export_record = response.json()

        # 4. 验证返回数据
        assert export_record["candidate_id"] == candidate["id"]
        assert export_record["format"] == "PDF"
        assert export_record["file_name"].startswith(candidate["name"])
        assert export_record["file_name"].endswith(".pdf")
        assert export_record["file_path"].startswith("/exports/")

        # 5. 验证物理文件确实生成且有效
        physical_path = os.path.join(ROOT_DIR, export_record["file_path"].lstrip("/"))

        assert os.path.exists(physical_path), f"Physical PDF file not found at: {physical_path}"
        
        with open(physical_path, "rb") as f:
            header = f.read(4)
            assert header == b"%PDF", "Generated file is not a valid PDF document"

        reader = PdfReader(physical_path)
        assert len(reader.pages) >= 1
        first_page = reader.pages[0]
        assert round(float(first_page.mediabox.width), 2) == round(float(A4[0]), 2)
        assert round(float(first_page.mediabox.height), 2) == round(float(A4[1]), 2)

        # 6. 清理生成的测试物理文件，防止产生脏文件
        try:
            os.remove(physical_path)
        except OSError:
            pass
