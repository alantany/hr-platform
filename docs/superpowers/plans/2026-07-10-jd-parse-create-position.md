# JD单生成岗位 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 在项目管理页岗位列表，组长/管理员粘贴 JD 文本，经 `POST /api/positions/parse-jd` 解析后预填现有「创建岗位」弹窗，用户补选客户/项目并确认后走现有 `POST /api/positions` 落库。

**Architecture:** 后端新增只读解析接口（不写库），复用 `get_openai_client`，新增 JD 专用 LLM 调用与枚举清洗函数；前端新增 JD 粘贴小弹窗与 `hrApi.parseJd`，解析成功后复用现有 `[data-position-modal]` 预填；客户/项目不预填，锁定上限保持 10。

**Tech Stack:** 静态 HTML + vanilla JS（`app.js` / `frontend-api.js`）、FastAPI、Pydantic、现有 OpenAI 兼容客户端（DeepSeek）、pytest + `unittest.mock.patch`

---

## File Structure

| 文件 | 职责 |
|------|------|
| `backend/app/schemas.py` | 新增 `PositionJdParseRequest` / `PositionJdParseOut` |
| `backend/app/main.py` | 新增 `JD_PARSE_*` 常量、`call_llm_for_jd_parse`、`normalize_jd_parse_result`、`POST /api/positions/parse-jd`（权限与创建岗位一致） |
| `tests/test_position_parse_jd.py` | 解析接口单测（mock LLM；空文本 400；操作员 403；枚举清洗） |
| `frontend-api.js` | 新增 `parseJd({ jd_text })` |
| `src/pages/projects.html` | JD 按钮改 `data-action`；新增 JD 粘贴小弹窗；操作员隐藏选择器同步 |
| `app.js` | 打开/关闭/确认解析；预填创建弹窗；错误 Toast 且不打开创建弹窗 |
| `docs/superpowers/specs/2026-07-10-jd-parse-create-position-design.md` | 实现完成后更新状态 |
| `findings.md` / `progress.md` / `task_plan.md` | 每阶段收尾记录 |

### 枚举以真实创建弹窗为准（已核对 `projects.html`）

| 字段 | DOM `option value`（权威） | Spec 一致？ |
|------|---------------------------|-------------|
| 紧急程度 | `紧急`、`正常` | 是（列表筛选仍用高/中/低，本功能不改） |
| 年龄规则 | `不限`、`20-30岁`、`30-40岁` | 是 |
| 性别规则 | `不限`、`男`、`女` | 是 |
| 学历要求 | `不限`、`本科`、`大专`、`硕士` | 是 |
| 工作经验 | `不限`、`应届生`、`1-3年`、`3-5年`、`5年以上` | 是 |
| 求职状态 | `不限`、`离职`、`在职` | 是 |

### API ↔ DOM 映射（前后端字段名必须一致）

| API / `PositionJdParseOut` | DOM selector |
|----------------------------|--------------|
| `name` | `[data-position-name]` |
| `description`（前端用粘贴原文覆盖） | `[data-position-description]` |
| `urgency` | `[data-position-urgency]` |
| `hiring_count` | `[data-position-count]` |
| `salary_min` | `[data-position-salary-min]` |
| `salary_max` | `[data-position-salary-max]` |
| `location` | `[data-position-location]` |
| `age_requirement` | `[data-position-req-age]` |
| `gender_requirement` | `[data-position-req-gender]` |
| `education_requirement` | `[data-position-req-edu]` |
| `experience_requirement` | `[data-position-req-exp]` |
| `job_status_requirement` | `[data-position-req-status]` |
| （不返回）客户/项目 | `[data-position-company]` / `[data-position-project]` 保持空 |
| （不改）锁定上限 | `[data-position-target-count]` 保持 `10` |

### 实现常量（本计划锁定，不再 TBD）

| 项 | 值 |
|----|-----|
| `jd_text` 去空白后最大长度 | `20000` |
| LLM 失败 HTTP | `502`，detail=`JD 解析失败，请稍后重试` |
| 空文本 HTTP | `400`，detail=`请先粘贴 JD` |
| 超长 HTTP | `400`，detail=`JD 文本过长，请控制在 20000 字以内` |
| 结果完全不可用 | `422`，detail=`未能从 JD 中解析出可用字段`（见 Task 2 判定） |
| 权限 | 与 `add_position` 相同：`is_admin or is_leader`，否则 403 |

---

### Task 1: Schema + parse-jd 路由骨架（mock LLM）+ 权限 + 空文本校验

**Files:**
- Create: `tests/test_position_parse_jd.py`
- Modify: `backend/app/schemas.py`（在 `PositionAssignPayload` 之前插入新 schema）
- Modify: `backend/app/main.py`（在 `@app.post("/api/positions")` 的 `add_position` 函数之后、`@app.patch("/api/positions/{position_id}")` 之前插入路由）

- [ ] **Step 1: Write the failing test**

创建 `tests/test_position_parse_jd.py`：

```python
from pathlib import Path
import sys
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from fastapi.testclient import TestClient

from backend.app.main import app
from tests.auth_helpers import login_headers


SAMPLE_JD = """
岗位名称：高级 Java 工程师
工作地点：上海
薪资：20-35K
学历：本科
经验：5年以上
紧急招聘 2 人
"""


@patch("backend.app.main.call_llm_for_jd_parse")
def test_parse_jd_success_as_leader(mock_llm):
    mock_llm.return_value = {
        "name": "高级 Java 工程师",
        "urgency": "紧急",
        "hiring_count": 2,
        "salary_min": 20,
        "salary_max": 35,
        "location": "上海",
        "age_requirement": "不限",
        "gender_requirement": "不限",
        "education_requirement": "本科",
        "experience_requirement": "5年以上",
        "job_status_requirement": "不限",
    }
    with TestClient(app) as client:
        headers = login_headers(client, "leader")
        res = client.post(
            "/api/positions/parse-jd",
            json={"jd_text": SAMPLE_JD},
            headers=headers,
        )
        assert res.status_code == 200, res.text
        data = res.json()
        assert data["name"] == "高级 Java 工程师"
        assert data["urgency"] == "紧急"
        assert data["hiring_count"] == 2
        assert data["salary_min"] == 20
        assert data["salary_max"] == 35
        assert data["location"] == "上海"
        assert data["education_requirement"] == "本科"
        assert data["experience_requirement"] == "5年以上"
        assert data["description"] == SAMPLE_JD
        mock_llm.assert_called_once()


def test_parse_jd_empty_text_returns_400():
    with TestClient(app) as client:
        headers = login_headers(client, "admin")
        res = client.post(
            "/api/positions/parse-jd",
            json={"jd_text": "   \n\t  "},
            headers=headers,
        )
        assert res.status_code == 400
        assert "请先粘贴 JD" in res.text


def test_parse_jd_operator_forbidden():
    with TestClient(app) as client:
        headers = login_headers(client, "operator")
        res = client.post(
            "/api/positions/parse-jd",
            json={"jd_text": SAMPLE_JD},
            headers=headers,
        )
        assert res.status_code == 403


@patch("backend.app.main.call_llm_for_jd_parse")
def test_parse_jd_llm_failure_returns_502(mock_llm):
    mock_llm.side_effect = RuntimeError("timeout")
    with TestClient(app) as client:
        headers = login_headers(client, "admin")
        res = client.post(
            "/api/positions/parse-jd",
            json={"jd_text": SAMPLE_JD},
            headers=headers,
        )
        assert res.status_code == 502
        assert "JD 解析失败" in res.text
```

- [ ] **Step 2: Run test to verify it fails**

Run:

```bash
cd /Users/huaiyuan/Desktop/workspace/hr-plateform && python -m pytest tests/test_position_parse_jd.py -v
```

Expected: FAIL（`call_llm_for_jd_parse` 未定义，或路由 404）

- [ ] **Step 3: Add schemas**

在 `backend/app/schemas.py` 的 `PositionUpdate` 之后、`PositionAssignPayload` 之前插入：

```python
class PositionJdParseRequest(BaseModel):
    jd_text: str


class PositionJdParseOut(BaseModel):
    name: str = ""
    description: str = ""
    urgency: str = "正常"
    hiring_count: int | None = 1
    salary_min: int | None = None
    salary_max: int | None = None
    location: str = ""
    age_requirement: str = "不限"
    gender_requirement: str = "不限"
    education_requirement: str = "不限"
    experience_requirement: str = "不限"
    job_status_requirement: str = "不限"
```

确保文件顶部已有 `from pydantic import BaseModel`（已有则不动）。

- [ ] **Step 4: Add stub LLM + route (minimal, no enum sanitize yet)**

在 `backend/app/main.py` 中 `get_openai_client` 附近（或 `call_llm_for_json` 之后）新增 stub（Task 2 会换成真实实现）：

```python
JD_PARSE_MAX_CHARS = 20000

def call_llm_for_jd_parse(jd_text: str) -> dict:
    """Parse JD text into position fields. Task 2 replaces body with real LLM call."""
    raise NotImplementedError("call_llm_for_jd_parse not implemented")
```

在 `add_position` 之后插入路由：

```python
@app.post("/api/positions/parse-jd", response_model=schemas.PositionJdParseOut)
def parse_position_jd(payload: schemas.PositionJdParseRequest, user: User = Depends(require_user)):
    if not security.is_admin(user) and not security.is_leader(user):
        raise HTTPException(status_code=403, detail="仅组长及系统管理员有权解析 JD 生成岗位")
    jd_text = (payload.jd_text or "").strip()
    if not jd_text:
        raise HTTPException(status_code=400, detail="请先粘贴 JD")
    if len(jd_text) > JD_PARSE_MAX_CHARS:
        raise HTTPException(status_code=400, detail=f"JD 文本过长，请控制在 {JD_PARSE_MAX_CHARS} 字以内")
    try:
        raw = call_llm_for_jd_parse(jd_text)
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=502, detail="JD 解析失败，请稍后重试")
    if not isinstance(raw, dict):
        raise HTTPException(status_code=502, detail="JD 解析失败，请稍后重试")
    # Task 1: pass-through + force description = original text
    out = {
        "name": str(raw.get("name") or "").strip(),
        "description": jd_text,
        "urgency": raw.get("urgency") or "正常",
        "hiring_count": raw.get("hiring_count", 1),
        "salary_min": raw.get("salary_min"),
        "salary_max": raw.get("salary_max"),
        "location": str(raw.get("location") or "").strip(),
        "age_requirement": raw.get("age_requirement") or "不限",
        "gender_requirement": raw.get("gender_requirement") or "不限",
        "education_requirement": raw.get("education_requirement") or "不限",
        "experience_requirement": raw.get("experience_requirement") or "不限",
        "job_status_requirement": raw.get("job_status_requirement") or "不限",
    }
    return out
```

注意：本 Task 的 stub 在未 mock 时会进 `except Exception` → 502；测试全部 patch `call_llm_for_jd_parse`，因此成功路径可过。

- [ ] **Step 5: Run tests to verify they pass**

Run:

```bash
cd /Users/huaiyuan/Desktop/workspace/hr-plateform && python -m pytest tests/test_position_parse_jd.py -v
```

Expected: 4 passed

- [ ] **Step 6: Commit**

```bash
git add tests/test_position_parse_jd.py backend/app/schemas.py backend/app/main.py
git commit -m "$(cat <<'EOF'
feat: add positions/parse-jd API skeleton with auth and empty-text checks

EOF
)"
```

（本仓库收尾习惯：若本步已改代码，可同步在 `progress.md` 顶部记一行；最终 push 可在全部 Task 完成后统一，或按 finish-workflow 每阶段 push。）

---

### Task 2: LLM prompt + 枚举映射/清洗 + 不可用结果

**Files:**
- Modify: `backend/app/main.py`（实现 `call_llm_for_jd_parse`、`normalize_jd_parse_result`，路由改用 normalize）
- Modify: `tests/test_position_parse_jd.py`（追加清洗与不可用用例）

- [ ] **Step 1: Write the failing tests for normalize behavior**

在 `tests/test_position_parse_jd.py` 追加：

```python
from backend.app.main import normalize_jd_parse_result


def test_normalize_jd_parse_result_maps_enums_and_defaults():
    raw = {
        "name": " 产品经理 ",
        "urgency": "高",  # 非创建弹窗枚举 → 正常
        "hiring_count": "3",
        "salary_min": "15.0",
        "salary_max": "none",
        "location": "北京",
        "age_requirement": "30到40",
        "gender_requirement": "男性",
        "education_requirement": "本科及以上",
        "experience_requirement": "五年以上",
        "job_status_requirement": "随便",
    }
    out = normalize_jd_parse_result(raw, "原文JD")
    assert out["name"] == "产品经理"
    assert out["description"] == "原文JD"
    assert out["urgency"] == "正常"
    assert out["hiring_count"] == 3
    assert out["salary_min"] == 15
    assert out["salary_max"] is None
    assert out["location"] == "北京"
    assert out["age_requirement"] == "30-40岁"
    assert out["gender_requirement"] == "男"
    assert out["education_requirement"] == "本科"
    assert out["experience_requirement"] == "5年以上"
    assert out["job_status_requirement"] == "不限"


def test_normalize_jd_parse_result_detects_unusable():
    out = normalize_jd_parse_result(
        {
            "name": "",
            "urgency": "正常",
            "hiring_count": None,
            "salary_min": None,
            "salary_max": None,
            "location": "",
            "age_requirement": "不限",
            "gender_requirement": "不限",
            "education_requirement": "不限",
            "experience_requirement": "不限",
            "job_status_requirement": "不限",
        },
        "只有一段无法抽取的废话",
    )
    assert out.get("_unusable") is True


@patch("backend.app.main.call_llm_for_jd_parse")
def test_parse_jd_unusable_returns_422(mock_llm):
    mock_llm.return_value = {
        "name": "",
        "urgency": "正常",
        "hiring_count": None,
        "salary_min": None,
        "salary_max": None,
        "location": "",
        "age_requirement": "不限",
        "gender_requirement": "不限",
        "education_requirement": "不限",
        "experience_requirement": "不限",
        "job_status_requirement": "不限",
    }
    with TestClient(app) as client:
        headers = login_headers(client, "admin")
        res = client.post(
            "/api/positions/parse-jd",
            json={"jd_text": "无法解析的内容"},
            headers=headers,
        )
        assert res.status_code == 422
        assert "未能从 JD 中解析出可用字段" in res.text


@patch("backend.app.main.call_llm_for_jd_parse")
def test_parse_jd_empty_name_but_other_fields_ok(mock_llm):
    mock_llm.return_value = {
        "name": "",
        "urgency": "紧急",
        "hiring_count": 2,
        "salary_min": 20,
        "salary_max": 30,
        "location": "深圳",
        "age_requirement": "不限",
        "gender_requirement": "不限",
        "education_requirement": "本科",
        "experience_requirement": "3-5年",
        "job_status_requirement": "不限",
    }
    with TestClient(app) as client:
        headers = login_headers(client, "admin")
        res = client.post(
            "/api/positions/parse-jd",
            json={"jd_text": "深圳本科 20-30K 招2人"},
            headers=headers,
        )
        assert res.status_code == 200, res.text
        assert res.json()["name"] == ""
        assert res.json()["location"] == "深圳"
```

- [ ] **Step 2: Run tests to verify new ones fail**

Run:

```bash
cd /Users/huaiyuan/Desktop/workspace/hr-plateform && python -m pytest tests/test_position_parse_jd.py::test_normalize_jd_parse_result_maps_enums_and_defaults tests/test_position_parse_jd.py::test_normalize_jd_parse_result_detects_unusable tests/test_position_parse_jd.py::test_parse_jd_unusable_returns_422 -v
```

Expected: FAIL（`normalize_jd_parse_result` 未定义）

- [ ] **Step 3: Implement normalize + real LLM call**

在 `backend/app/main.py` 用以下完整实现替换 Task 1 的 stub `call_llm_for_jd_parse`，并新增 `normalize_jd_parse_result`：

```python
JD_PARSE_MAX_CHARS = 20000

JD_URGENCY_VALUES = {"紧急", "正常"}
JD_AGE_VALUES = {"不限", "20-30岁", "30-40岁"}
JD_GENDER_VALUES = {"不限", "男", "女"}
JD_EDU_VALUES = {"不限", "本科", "大专", "硕士"}
JD_EXP_VALUES = {"不限", "应届生", "1-3年", "3-5年", "5年以上"}
JD_STATUS_VALUES = {"不限", "离职", "在职"}

JD_PARSE_SYSTEM_PROMPT = """你是猎头招聘助手。只从用户粘贴的 JD 文本中抽取岗位字段，严格返回 JSON 对象。
禁止推断或输出公司名、项目名、客户 ID。
字段与取值约束：
- name: 岗位名称字符串，抽不到则 ""
- urgency: 只能是 "紧急" 或 "正常"；不确定则 "正常"
- hiring_count: 正整数；抽不到则 null
- salary_min / salary_max: 月薪 K 的整数（如 20 表示 20K）；抽不到则 null
- location: 工作城市/地点；抽不到则 ""
- age_requirement: 只能是 "不限" | "20-30岁" | "30-40岁"
- gender_requirement: 只能是 "不限" | "男" | "女"
- education_requirement: 只能是 "不限" | "本科" | "大专" | "硕士"
- experience_requirement: 只能是 "不限" | "应届生" | "1-3年" | "3-5年" | "5年以上"
- job_status_requirement: 只能是 "不限" | "离职" | "在职"
枚举对不上时用 "不限"（urgency 对不上用 "正常"）。
不要返回 description，不要改写 JD 原文。"""


def _coerce_optional_int(value):
    if value is None or value == "":
        return None
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return None


def _pick_enum(value: str, allowed: set[str], default: str, aliases: dict[str, str] | None = None) -> str:
    text = str(value or "").strip()
    if text in allowed:
        return text
    aliases = aliases or {}
    if text in aliases and aliases[text] in allowed:
        return aliases[text]
    # fuzzy contains for common Chinese variants
    for key, mapped in aliases.items():
        if key and key in text and mapped in allowed:
            return mapped
    for item in allowed:
        if item != default and item in text:
            return item
    return default


def normalize_jd_parse_result(raw: dict, jd_text: str) -> dict:
    urgency_aliases = {
        "高": "紧急",
        "紧急招聘": "紧急",
        "低": "正常",
        "中": "正常",
        "一般": "正常",
        "常规": "正常",
    }
    age_aliases = {"20-30": "20-30岁", "30-40": "30-40岁", "30到40": "30-40岁", "20到30": "20-30岁"}
    gender_aliases = {"男性": "男", "女性": "女", "男女不限": "不限"}
    edu_aliases = {"本科及以上": "本科", "本科以上": "本科", "大专及以上": "大专", "硕士及以上": "硕士", "研究生": "硕士"}
    exp_aliases = {
        "五年以上": "5年以上",
        "5年及以上": "5年以上",
        "三到五年": "3-5年",
        "1到3年": "1-3年",
        "应届": "应届生",
    }
    status_aliases = {"已离职": "离职", "在职看机会": "在职"}

    name = str(raw.get("name") or "").strip()
    location = str(raw.get("location") or "").strip()
    hiring_count = _coerce_optional_int(raw.get("hiring_count"))
    if hiring_count is not None and hiring_count < 1:
        hiring_count = None
    salary_min = _coerce_optional_int(raw.get("salary_min"))
    salary_max = _coerce_optional_int(raw.get("salary_max"))

    out = {
        "name": name,
        "description": jd_text,
        "urgency": _pick_enum(raw.get("urgency"), JD_URGENCY_VALUES, "正常", urgency_aliases),
        "hiring_count": hiring_count if hiring_count is not None else 1,
        "salary_min": salary_min,
        "salary_max": salary_max,
        "location": location,
        "age_requirement": _pick_enum(raw.get("age_requirement"), JD_AGE_VALUES, "不限", age_aliases),
        "gender_requirement": _pick_enum(raw.get("gender_requirement"), JD_GENDER_VALUES, "不限", gender_aliases),
        "education_requirement": _pick_enum(raw.get("education_requirement"), JD_EDU_VALUES, "不限", edu_aliases),
        "experience_requirement": _pick_enum(raw.get("experience_requirement"), JD_EXP_VALUES, "不限", exp_aliases),
        "job_status_requirement": _pick_enum(raw.get("job_status_requirement"), JD_STATUS_VALUES, "不限", status_aliases),
    }

    has_signal = bool(name or location or salary_min is not None or salary_max is not None)
    if hiring_count is not None and hiring_count != 1:
        has_signal = True
    if out["urgency"] == "紧急":
        has_signal = True
    if out["age_requirement"] != "不限":
        has_signal = True
    if out["gender_requirement"] != "不限":
        has_signal = True
    if out["education_requirement"] != "不限":
        has_signal = True
    if out["experience_requirement"] != "不限":
        has_signal = True
    if out["job_status_requirement"] != "不限":
        has_signal = True
    if not has_signal:
        out["_unusable"] = True
    return out


def call_llm_for_jd_parse(jd_text: str) -> dict:
    if not DEEPSEEK_API_KEY or DEEPSEEK_API_KEY in ("your_api_key_here", "replace_with_your_openrouter_key"):
        raise ValueError("DeepSeek API Key is not configured. Please check your .env file.")
    client = get_openai_client()
    response = client.chat.completions.create(
        model=DEEPSEEK_MODEL,
        messages=[
            {"role": "system", "content": JD_PARSE_SYSTEM_PROMPT},
            {"role": "user", "content": f"请解析以下 JD 并严格返回 JSON：\n\n{jd_text}"},
        ],
        response_format={"type": "json_object"},
        temperature=0.1,
    )
    raw_response = response.choices[0].message.content or ""
    parsed = json.loads(_strip_json_fence(raw_response))
    if not isinstance(parsed, dict):
        raise ValueError("LLM did not return a JSON object")
    return parsed
```

将 `parse_position_jd` 路由体改为：

```python
@app.post("/api/positions/parse-jd", response_model=schemas.PositionJdParseOut)
def parse_position_jd(payload: schemas.PositionJdParseRequest, user: User = Depends(require_user)):
    if not security.is_admin(user) and not security.is_leader(user):
        raise HTTPException(status_code=403, detail="仅组长及系统管理员有权解析 JD 生成岗位")
    jd_text = (payload.jd_text or "").strip()
    if not jd_text:
        raise HTTPException(status_code=400, detail="请先粘贴 JD")
    if len(jd_text) > JD_PARSE_MAX_CHARS:
        raise HTTPException(status_code=400, detail=f"JD 文本过长，请控制在 {JD_PARSE_MAX_CHARS} 字以内")
    try:
        raw = call_llm_for_jd_parse(jd_text)
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=502, detail="JD 解析失败，请稍后重试")
    if not isinstance(raw, dict):
        raise HTTPException(status_code=502, detail="JD 解析失败，请稍后重试")
    out = normalize_jd_parse_result(raw, jd_text)
    if out.pop("_unusable", False):
        raise HTTPException(status_code=422, detail="未能从 JD 中解析出可用字段")
    return out
```

- [ ] **Step 4: Run all parse-jd tests**

Run:

```bash
cd /Users/huaiyuan/Desktop/workspace/hr-plateform && python -m pytest tests/test_position_parse_jd.py -v
```

Expected: 全部 PASS（含 Task 1 原有用例；`description` 仍为请求原文）

- [ ] **Step 5: Commit**

```bash
git add backend/app/main.py tests/test_position_parse_jd.py
git commit -m "$(cat <<'EOF'
feat: add JD parse LLM prompt and enum normalization

EOF
)"
```

---

### Task 3: 前端 `parseJd` + JD 粘贴小弹窗（打开 / loading / 错误）

**Files:**
- Modify: `frontend-api.js`
- Modify: `src/pages/projects.html`
- Modify: `app.js`

本 Task **只做到**：打开小窗、取消、空文本 Toast、调用 API、失败 Toast 且不打开创建弹窗。预填放到 Task 4。

- [ ] **Step 1: Add `parseJd` to API client**

在 `frontend-api.js` 的 `createPosition` 方法后插入：

```javascript
  parseJd(payload) {
    return this.request("/positions/parse-jd", { method: "POST", body: JSON.stringify(payload) });
  },
```

- [ ] **Step 2: Change JD button + add modal HTML**

在 `src/pages/projects.html`：

1) 将岗位列表按钮从：

```html
<button class="btn primary" style="background-color: #15803D; border-color: #15803D;" data-action="noop" data-title="JD单生成岗位">📎 JD单生成岗位</button>
```

改为：

```html
<button class="btn primary" style="background-color: #15803D; border-color: #15803D;" data-action="open-jd-parse-modal" data-title="JD单生成岗位">📎 JD单生成岗位</button>
```

2) 同步操作员隐藏选择器（约 508 行）从：

```javascript
const jdBtn = document.querySelector('[data-action="noop"][data-title="JD单生成岗位"]');
```

改为：

```javascript
const jdBtn = document.querySelector('[data-action="open-jd-parse-modal"][data-title="JD单生成岗位"]');
```

3) 在 `[data-position-modal]` **之前**插入 JD 小弹窗（风格对齐 `candidates.html` 的 AI 检索弹窗）：

```html
  <div class="modal" data-jd-parse-modal style="display:none; position:fixed; inset:0; background:rgba(14,22,34,.45); z-index:2500; padding:24px;">
    <div class="panel" style="max-width:760px; margin:8vh auto 0; background:#fff;">
      <div class="section-head">
        <div>
          <h3>JD单生成岗位</h3>
          <div class="section-sub">粘贴完整 JD 文本，系统解析后预填创建岗位表单；客户与项目需人工选择。</div>
        </div>
        <div class="hero-actions" style="margin-top:0">
          <button class="btn" data-action="close-jd-parse-modal">取消</button>
          <button class="btn primary" data-action="confirm-jd-parse">开始解析</button>
        </div>
      </div>
      <div class="list">
        <div class="list-item">
          <div class="item-top">
            <div>
              <div class="item-title">JD 原文</div>
              <div class="item-meta">支持直接粘贴完整岗位描述；解析成功后将打开创建岗位弹窗并预填</div>
            </div>
          </div>
          <textarea class="input" rows="12" data-jd-parse-textarea placeholder="请粘贴完整 JD 文本…" style="width:100%; border:1px solid #e2e8f0; border-radius:8px; padding:12px; font-size:13px; outline:none; resize:vertical;"></textarea>
        </div>
      </div>
    </div>
  </div>
```

- [ ] **Step 3: Wire open/close/confirm handlers in `app.js`**

在 `handleGlobalButton` 内、`open-position-modal` 分支**之前**插入：

```javascript
  if (button.dataset.action === "open-jd-parse-modal") {
    const modal = document.querySelector("[data-jd-parse-modal]");
    const textarea = modal?.querySelector("[data-jd-parse-textarea]");
    if (textarea) textarea.value = "";
    if (modal) modal.style.display = "block";
    return;
  }
  if (button.dataset.action === "close-jd-parse-modal") {
    const modal = document.querySelector("[data-jd-parse-modal]");
    if (modal) modal.style.display = "none";
    return;
  }
  if (button.dataset.action === "confirm-jd-parse") {
    const modal = document.querySelector("[data-jd-parse-modal]");
    const textarea = modal?.querySelector("[data-jd-parse-textarea]");
    const jdText = textarea?.value?.trim() || "";
    if (!jdText) throw new Error("请先粘贴 JD");
    const hideLoading = showLoadingToast("JD 解析中...");
    try {
      await new Promise((resolve) => requestAnimationFrame(() => resolve()));
      const parsed = await window.hrApi.parseJd({ jd_text: jdText });
      // Task 4 will apply prefills; for now stash and close modal only if parse succeeded
      window.__jdParseDraft = { jdText, parsed };
      if (modal) modal.style.display = "none";
      showToast("JD 解析成功，请在创建弹窗中核对并选择客户/项目");
      // Task 4: open create modal + prefill — call helper if already present
      if (typeof window.applyJdParseToPositionModal === "function") {
        await window.applyJdParseToPositionModal(jdText, parsed);
      }
    } finally {
      hideLoading();
    }
    return;
  }
```

说明：`withButtonBusy` 已包裹全局按钮点击，开始解析时按钮会进入 loading；另加 `showLoadingToast` 与 AI 检索一致。失败时 `throw` 由外层 catch 成 Toast，小窗不关（因成功才 `display=none`），且不会调用预填。

- [ ] **Step 4: Manual smoke (no LLM needed if backend down — at least UI)**

在浏览器打开 `src/pages/projects.html`（需已登录组长/管理员）：

1. 切到岗位列表 Tab → 点击「📎 JD单生成岗位」→ 小窗出现  
2. 不填内容点「开始解析」→ Toast「请先粘贴 JD」  
3. 点「取消」→ 小窗关闭  

Expected: 上述交互正常；操作员账号下按钮仍隐藏。

- [ ] **Step 5: Commit**

```bash
git add frontend-api.js src/pages/projects.html app.js
git commit -m "$(cat <<'EOF'
feat: add JD paste modal and parseJd client for position create

EOF
)"
```

---

### Task 4: 解析成功后打开创建弹窗并预填

**Files:**
- Modify: `app.js`

- [ ] **Step 1: Extract / add `applyJdParseToPositionModal` helper**

在 `app.js` 中靠近 `handleGlobalButton` 之前（或文件内合适位置）新增：

```javascript
async function openPositionCreateModalBlank() {
  const modal = document.querySelector("[data-position-modal]");
  if (!modal) throw new Error("未找到创建岗位弹窗");
  const reset = (selector, val) => {
    const el = document.querySelector(selector);
    if (el) el.value = val;
  };
  reset("[data-position-company]", "");
  reset("[data-position-project]", "");
  reset("[data-position-name]", "");
  reset("[data-position-description]", "");
  reset("[data-position-urgency]", "正常");
  reset("[data-position-count]", "1");
  reset("[data-position-salary-min]", "");
  reset("[data-position-salary-max]", "");
  reset("[data-position-location]", "");
  reset("[data-position-req-age]", "不限");
  reset("[data-position-req-gender]", "不限");
  reset("[data-position-req-edu]", "不限");
  reset("[data-position-req-exp]", "不限");
  reset("[data-position-req-status]", "不限");
  reset("[data-position-target-count]", "10");

  const createPosCompany = modal.querySelector("[data-position-company]");
  const createPosProject = modal.querySelector("[data-position-project]");
  if (createPosCompany && createPosProject) {
    createPosCompany.innerHTML = '<option value="">加载中...</option>';
    createPosProject.innerHTML = '<option value="">请先选择客户</option>';
    createPosProject.disabled = true;
    try {
      const [companies, projects] = await Promise.all([
        window.hrApi.companies(),
        window.hrApi.projects(),
      ]);
      createPosCompany.innerHTML =
        '<option value="">请选择客户</option>' +
        companies
          .map((c) => `<option value="${c.id}">${escapeHtml(c.name)}</option>`)
          .join("");
      const fillProjects = () => {
        const companyId = Number(createPosCompany.value || 0);
        const filtered = companyId ? projects.filter((p) => p.company_id === companyId) : [];
        createPosProject.disabled = !companyId;
        createPosProject.innerHTML = companyId
          ? '<option value="">请选择项目</option>' +
            filtered.map((p) => `<option value="${p.id}">${escapeHtml(p.name)}</option>`).join("")
          : '<option value="">请先选择客户</option>';
      };
      createPosCompany.onchange = fillProjects;
      fillProjects();
    } catch (err) {
      console.warn("Failed to populate company/project selects in position modal:", err);
      createPosCompany.innerHTML = '<option value="">获取客户失败</option>';
      createPosProject.innerHTML = '<option value="">获取项目失败</option>';
    }
  }

  modal.style.display = "block";
  if (!window.__positionCityInitialized) {
    initCitySelector("[data-position-modal]");
    window.__positionCityInitialized = true;
  }
  return modal;
}

async function applyJdParseToPositionModal(jdText, parsed) {
  await openPositionCreateModalBlank();
  const setVal = (selector, val) => {
    const el = document.querySelector(selector);
    if (el && val !== undefined && val !== null) el.value = String(val);
  };
  // 客户/项目故意不填
  setVal("[data-position-name]", parsed.name || "");
  setVal("[data-position-description]", jdText || parsed.description || "");
  setVal("[data-position-urgency]", parsed.urgency || "正常");
  setVal(
    "[data-position-count]",
    parsed.hiring_count === null || parsed.hiring_count === undefined ? "1" : parsed.hiring_count
  );
  setVal(
    "[data-position-salary-min]",
    parsed.salary_min === null || parsed.salary_min === undefined ? "" : parsed.salary_min
  );
  setVal(
    "[data-position-salary-max]",
    parsed.salary_max === null || parsed.salary_max === undefined ? "" : parsed.salary_max
  );
  setVal("[data-position-location]", parsed.location || "");
  setVal("[data-position-req-age]", parsed.age_requirement || "不限");
  setVal("[data-position-req-gender]", parsed.gender_requirement || "不限");
  setVal("[data-position-req-edu]", parsed.education_requirement || "不限");
  setVal("[data-position-req-exp]", parsed.experience_requirement || "不限");
  setVal("[data-position-req-status]", parsed.job_status_requirement || "不限");
  // 锁定上限保持 10，不覆盖为其它值
  setVal("[data-position-target-count]", "10");
}
window.applyJdParseToPositionModal = applyJdParseToPositionModal;
```

- [ ] **Step 2: Refactor `open-position-modal` to reuse helper**

将原 `if (button.dataset.action === "open-position-modal") { ... }` 整块替换为：

```javascript
  if (button.dataset.action === "open-position-modal") {
    await openPositionCreateModalBlank();
    return;
  }
```

- [ ] **Step 3: Confirm `confirm-jd-parse` already calls apply helper**

确认 Task 3 中的成功分支包含：

```javascript
      if (typeof window.applyJdParseToPositionModal === "function") {
        await window.applyJdParseToPositionModal(jdText, parsed);
      }
```

若 Toast 文案重复，将成功 Toast 改为更短一句，例如 `showToast("已预填创建岗位表单，请选择客户与项目")`。

- [ ] **Step 4: Manual verification checklist**

用 mock 或真实环境验证：

1. 解析成功 → JD 小窗关闭 → 创建岗位弹窗打开  
2. `[data-position-description]` === 粘贴原文（非 LLM 改写）  
3. 名称/紧急/人数/薪资/地点/五类要求按映射写入  
4. 客户、项目为空；`[data-position-target-count]` 仍为 `10`  
5. 解析失败（可临时让后端返回 502）→ Toast，创建弹窗不出现，JD 小窗仍开着  

- [ ] **Step 5: Commit**

```bash
git add app.js
git commit -m "$(cat <<'EOF'
feat: prefill create-position modal from JD parse result

EOF
)"
```

---

### Task 5: 权限一致性 + 冒烟测试 + 文档收尾

**Files:**
- Modify: `tests/test_position_parse_jd.py`（补 admin 成功路径若尚未覆盖）
- Modify: `docs/superpowers/specs/2026-07-10-jd-parse-create-position-design.md`（状态）
- Modify: `findings.md` / `progress.md` / `task_plan.md`

- [ ] **Step 1: Add admin success + oversize text tests**

追加到 `tests/test_position_parse_jd.py`：

```python
@patch("backend.app.main.call_llm_for_jd_parse")
def test_parse_jd_success_as_admin(mock_llm):
    mock_llm.return_value = {
        "name": "测试岗",
        "urgency": "正常",
        "hiring_count": 1,
        "salary_min": None,
        "salary_max": None,
        "location": "杭州",
        "age_requirement": "不限",
        "gender_requirement": "不限",
        "education_requirement": "不限",
        "experience_requirement": "不限",
        "job_status_requirement": "不限",
    }
    with TestClient(app) as client:
        headers = login_headers(client, "admin")
        res = client.post(
            "/api/positions/parse-jd",
            json={"jd_text": "岗位：测试岗\n地点：杭州"},
            headers=headers,
        )
        assert res.status_code == 200
        assert res.json()["location"] == "杭州"


def test_parse_jd_too_long_returns_400():
    with TestClient(app) as client:
        headers = login_headers(client, "admin")
        res = client.post(
            "/api/positions/parse-jd",
            json={"jd_text": "A" * 20001},
            headers=headers,
        )
        assert res.status_code == 400
        assert "20000" in res.text
```

- [ ] **Step 2: Run full parse-jd suite**

Run:

```bash
cd /Users/huaiyuan/Desktop/workspace/hr-plateform && python -m pytest tests/test_position_parse_jd.py -v
```

Expected: 全部 PASS。`tests/conftest.py` 会在每测后清理库；本接口不写库，无需额外 finally。

- [ ] **Step 3: Frontend permission smoke**

1. 操作员登录 → `projects.html` 岗位 Tab →「JD单生成岗位」与「新建岗位」均不可见  
2. 组长登录 → 两按钮可见；直接 `POST /api/positions/parse-jd`（可用 curl + operator token）应 403  

Operator curl 示例：

```bash
TOKEN=$(curl -s -X POST http://127.0.0.1:8000/api/auth/login \
  -H 'Content-Type: application/json' \
  -d '{"username":"operator","password":"operator123"}' | python -c 'import sys,json; print(json.load(sys.stdin)["access_token"])')
curl -s -o /tmp/parse_jd_out.txt -w "%{http_code}" -X POST http://127.0.0.1:8000/api/positions/parse-jd \
  -H "Authorization: Bearer $TOKEN" -H 'Content-Type: application/json' \
  -d '{"jd_text":"测试"}'
cat /tmp/parse_jd_out.txt
```

Expected: HTTP `403`

- [ ] **Step 4: Update design spec status**

将 `docs/superpowers/specs/2026-07-10-jd-parse-create-position-design.md` 顶部状态改为：

```markdown
- **状态**：已确认，实现计划已就绪（实现见 `docs/superpowers/plans/2026-07-10-jd-parse-create-position.md`）
```

实现全部完成后，再改为「已实现」。

- [ ] **Step 5: Update task MD files**

`task_plan.md` Current Phase：

```markdown
## Current Phase

JD生成岗位实现计划已就绪，待用户选择执行方式（subagent-driven / inline）。维护流程：**改代码 → 更新三份 MD → commit → push**。
```

Phase 28：

```markdown
### Phase 28 - JD单生成岗位（实现计划已就绪）

- [x] 确认方案 A：粘贴 JD → 解析预填 → 人确认后走现有创建岗位
- [x] 写入设计文档 `docs/superpowers/specs/2026-07-10-jd-parse-create-position-design.md`
- [x] 用户审阅 spec
- [x] 编写实现计划 `docs/superpowers/plans/2026-07-10-jd-parse-create-position.md`
- [ ] 前后端实现与验证
- **Status:** plan ready, awaiting execution choice
```

- [ ] **Step 6: Final commit for this task’s code/docs**

```bash
git add tests/test_position_parse_jd.py docs/superpowers/specs/2026-07-10-jd-parse-create-position-design.md findings.md progress.md task_plan.md
git commit -m "$(cat <<'EOF'
test: harden parse-jd coverage and mark plan ready in docs

EOF
)"
```

---

## Self-Review

### 1. Spec coverage

| Spec 需求 | Task |
|-----------|------|
| 入口按钮从 noop → 打开 JD 小窗 | Task 3 |
| 小窗：多行、开始解析/取消、loading、空文本 Toast | Task 3 |
| `POST /api/positions/parse-jd` 不写库 | Task 1 |
| 鉴权组长/管理员；操作员 403 | Task 1、5 |
| 空文本 400；LLM 失败 502 | Task 1 |
| 枚举映射；不确定→不限/正常 | Task 2 |
| description=原文；不推断客户项目 | Task 2、4 |
| 成功后关小窗、开创建弹窗预填 | Task 4 |
| 锁定上限 10 不动 | Task 4 |
| 失败不打开创建弹窗 | Task 3 |
| 保存仍走现有 `POST /api/positions` | 不改保存路径（Task 4 仅预填） |
| 前端隐藏与后端 403 一致 | Task 3（选择器）、Task 5 |
| 岗位名为空仍可打开预填 | Task 2 `test_parse_jd_empty_name_but_other_fields_ok` + Task 4 |
| 不做 Word/PDF、不自动落库、不改锁定 | Non-Goals，计划未引入 |

### 2. Placeholder scan

无 TBD/TODO/「类似 Task N」/「补充错误处理」占位；长度上限与错误码已锁定。

### 3. Type / field consistency

- Request: `jd_text`
- Response: `name`, `description`, `urgency`, `hiring_count`, `salary_min`, `salary_max`, `location`, `age_requirement`, `gender_requirement`, `education_requirement`, `experience_requirement`, `job_status_requirement`
- 前端 `parseJd({ jd_text })` → `applyJdParseToPositionModal(jdText, parsed)` 使用同一字段名
- DOM 映射表见 File Structure；紧急程度以创建弹窗 `紧急`/`正常` 为准（非列表 `高`/`中`/`低`）
