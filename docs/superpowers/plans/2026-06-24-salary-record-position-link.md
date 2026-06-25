# Salary Record Position Link Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将候选人详情里的“薪资/福利/入职条件记录”改成从岗位管理选择岗位，并自动带出客户公司，消除手工填写岗位名和公司名的入口。

**Architecture:** 薪资记录继续保留冗余显示字段 `position_name/company_name`，但新增真实关联字段 `position_id` 作为单一选择源。前端弹窗只负责选择岗位和展示公司，后端负责根据 `position_id` 回填岗位名与公司名，保证历史记录和详情展示都沿用现有字符串字段。

**Tech Stack:** Vue-free static HTML + vanilla JS, FastAPI, SQLAlchemy 2.0, Pydantic, pytest

---

### Task 1: Add `position_id` to salary records and backfill display fields server-side

**Files:**
- Modify: `backend/app/models.py`
- Modify: `backend/app/schemas.py`
- Modify: `backend/app/main.py`
- Modify: `backend/app/crud.py`
- Test: `tests/test_salary_tracking.py`

- [ ] **Step 1: Write the failing test**

```python
def test_create_salary_record_links_position_and_derives_company(client, db_session):
    position = create_position_with_project_and_company(db_session, company_name="测试公司", position_name="测试岗位")
    candidate = create_candidate(db_session)

    payload = {
        "candidate_id": candidate.id,
        "position_id": position.id,
        "interview_round": "第1轮",
        "agreed_salary": "25K-30K",
        "candidate_accepted": "接受",
    }
    res = client.post("/api/salary-records", json=payload)
    assert res.status_code == 200

    data = res.json()
    assert data["position_id"] == position.id
    assert data["position_name"] == "测试岗位"
    assert data["company_name"] == "测试公司"
```

- [ ] **Step 2: Run the test to verify it fails**

Run: `pytest tests/test_salary_tracking.py -q`
Expected: fail because `position_id` is not part of the salary record schema/model yet.

- [ ] **Step 3: Write the minimal implementation**

```python
class SalaryRecord(Base, TimestampMixin):
    position_id: Mapped[int | None] = mapped_column(ForeignKey("positions.id"), nullable=True)


class SalaryRecordCreate(BaseModel):
    position_id: int | None = None
```

```python
def create_salary_record(db: Session, payload):
    data = payload.model_dump()
    position_id = data.get("position_id")
    if position_id:
        position = db.get(Position, position_id)
        if not position:
            raise HTTPException(status_code=404, detail="岗位不存在")
        project = db.get(Project, position.project_id)
        data["position_name"] = position.name
        data["company_name"] = project.company_name if project else ""
    obj = SalaryRecord(**data)
    db.add(obj)
    return obj
```

```python
def update_salary_record(db: Session, record: SalaryRecord, payload):
    data = payload.model_dump(exclude_unset=True)
    if "position_id" in data and data["position_id"]:
        position = db.get(Position, data["position_id"])
        if not position:
            raise HTTPException(status_code=404, detail="岗位不存在")
        project = db.get(Project, position.project_id)
        record.position_id = position.id
        record.position_name = position.name
        record.company_name = project.company_name if project else ""
    for key, value in data.items():
        if key not in {"candidate_id", "position_id"}:
            setattr(record, key, value)
    return record
```

```python
position_columns = {
    "position_id": "ALTER TABLE salary_records ADD COLUMN position_id INTEGER",
}
```

- [ ] **Step 4: Run the test to verify it passes**

Run: `pytest tests/test_salary_tracking.py -q`
Expected: pass with the new `position_id` field persisted and display fields populated.

- [ ] **Step 5: Commit**

```bash
git add backend/app/models.py backend/app/schemas.py backend/app/main.py backend/app/crud.py tests/test_salary_tracking.py
git commit -m "feat: link salary records to positions"
```

### Task 2: Replace manual job/company inputs with a position dropdown in the salary modal

**Files:**
- Modify: `src/pages/candidates.html`
- Modify: `app.js`

- [ ] **Step 1: Write the failing test**

```javascript
// In a browser smoke test, open the salary modal and assert:
// 1. There is a select for positions populated from window.hrApi.positions()
// 2. There is no editable company text input
// 3. Changing the position updates the company display automatically
```

- [ ] **Step 2: Run the test to verify it fails**

Run: `node --check app.js`
Expected: pass for syntax, but browser smoke should fail because the modal still renders manual inputs.

- [ ] **Step 3: Write the minimal implementation**

```html
<select class="input" id="salary-position-id"></select>
<div id="salary-company-name-display" class="item-meta">所属公司：请选择岗位后自动显示</div>
```

```javascript
const positions = await window.hrApi.positions();
positionSelect.innerHTML = '<option value="">请选择岗位</option>' + positions.map(p => `<option value="${p.id}">${p.name}</option>`).join('');
positionSelect.addEventListener('change', () => {
  const selected = positions.find(p => String(p.id) === positionSelect.value);
  companyDisplay.textContent = selected ? `所属公司：${projectMap.get(selected.project_id)?.company_name || '未知公司'}` : '所属公司：请选择岗位后自动显示';
});
```

```javascript
const payload = {
  position_id: Number(positionSelect.value || 0) || null,
  agreed_salary: agreedEl?.value?.trim() || "",
  welfare_desc: welfareEl?.value?.trim() || "",
  onboard_cond: onboardEl?.value?.trim() || "",
};
```

- [ ] **Step 4: Run the test to verify it passes**

Run: `node --check app.js`
Run: `python3 -m pytest tests/test_salary_tracking.py -q`
Expected: salary modal renders a position dropdown, company is read-only display, and submission sends `position_id`.

- [ ] **Step 5: Commit**

```bash
git add src/pages/candidates.html app.js
git commit -m "feat: select salary position from position management"
```

### Task 3: Reconcile history rendering and update work logs

**Files:**
- Modify: `app.js`
- Modify: `findings.md`
- Modify: `progress.md`

- [ ] **Step 1: Write the failing test**

```python
def test_salary_record_history_keeps_position_name_and_company_name(client, db_session):
    # create record with position_id and confirm the detail page history still renders the derived strings
    ...
```

- [ ] **Step 2: Run the test to verify it fails**

Run: `pytest tests/test_salary_tracking.py -q`
Expected: fail until the detail table reads the derived fields for both create and edit flows.

- [ ] **Step 3: Write the minimal implementation**

```javascript
const positionLabel = rec.position_name || '-';
const companyLabel = rec.company_name || '-';
```

```md
- 薪资记录现在以 `position_id` 作为真实关联源，岗位名和公司名由岗位管理数据回填。
```

```md
- 已完成薪资记录岗位联动改造，弹窗从手输岗位/公司改为选岗位自动带出公司。
```

- [ ] **Step 4: Run the test to verify it passes**

Run: `pytest tests/test_salary_tracking.py -q`
Run: `node --check app.js`
Expected: pass, with history rows still showing岗位名和公司名。

- [ ] **Step 5: Commit**

```bash
git add app.js findings.md progress.md
git commit -m "chore: close salary position linkage rollout"
```
