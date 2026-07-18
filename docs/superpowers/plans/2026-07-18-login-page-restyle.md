# 登录页视觉改版 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将登录页改为浅色分栏风格，并用内联 SVG 呈现六边形 XL logo，同时保持登录逻辑不变。

**Architecture:** 仅改 `src/pages/login.html` 的 markup/页内 CSS，以及 `styles.css` 中登录页 `!important` 覆盖规则。Logo 用页内 SVG（蓝六边形 + 白 XL + 外层光晕），不新增静态资源文件。认证脚本、默认账号、错误/踢下线提示原样保留。

**Tech Stack:** 静态 HTML + 页内 CSS + 内联 SVG；现有 `frontend-api.js` 登录接口；pytest 做 markup 契约断言。

## Global Constraints

- Logo 字母必须为 **XL**（内联 SVG，不单独落文件）
- 主色约 `#3b82f6`；背景浅蓝 `#e0f2fe` → 白 `#ffffff`
- 三个 pill：智能招聘 / 权限管理 / 数据分析
- 保留默认账号 `admin` / `admin123` 与 `reason=kicked` 提示
- 不改 `frontend-api.js`、鉴权接口、RBAC、后台其他页面视觉
- 完成后更新 `progress.md` / `findings.md` / `task_plan.md`，再 commit 并 push

---

## File Structure

| 文件 | 职责 |
|------|------|
| `tests/test_login_page_markup.py` | 断言登录页关键 markup（logo / 文案 / 表单钩子） |
| `src/pages/login.html` | 登录页结构、页内样式、SVG logo、登录脚本 |
| `styles.css` | 放宽/改写登录页全局 `!important` 覆盖，避免压扁新布局 |
| `progress.md` / `findings.md` / `task_plan.md` | 任务收尾记录 |

---

### Task 1: 登录页 markup 契约测试

**Files:**
- Create: `tests/test_login_page_markup.py`
- Modify: （无）
- Test: `tests/test_login_page_markup.py`

**Interfaces:**
- Consumes: 仓库内 `src/pages/login.html` 文本内容
- Produces: 失败的契约测试，驱动后续 HTML/CSS 改写

- [ ] **Step 1: 写入失败测试**

```python
from pathlib import Path

LOGIN_HTML = Path(__file__).resolve().parents[1] / "src" / "pages" / "login.html"


def _html() -> str:
    return LOGIN_HTML.read_text(encoding="utf-8")


def test_login_page_has_hexagon_xl_logo():
    html = _html()
    assert 'class="login-logo"' in html
    assert "<svg" in html
    assert ">XL<" in html or ">XL</" in html


def test_login_page_brand_copy_and_pills():
    html = _html()
    assert "AI招聘管理平台" in html
    assert "人力资源管理系统 v3.0" in html
    assert "智能招聘" in html
    assert "权限管理" in html
    assert "数据分析" in html


def test_login_page_keeps_auth_hooks():
    html = _html()
    assert 'data-login-form' in html
    assert 'data-login-username' in html
    assert 'data-login-password' in html
    assert 'data-login-submit' in html
    assert 'data-login-message' in html
    assert 'value="admin"' in html
    assert 'value="admin123"' in html
    assert "reason=kicked" in html or "reason === 'kicked'" in html


def test_login_page_drops_old_blue_panel_mark():
    html = _html()
    assert 'class="login-mark"' not in html
    assert "login-footnote" not in html
```

- [ ] **Step 2: 跑测试确认失败**

Run: `python -m pytest tests/test_login_page_markup.py -v`

Expected: FAIL（当前仍是 `login-mark` / 无 SVG XL / 仍有 footnote）

- [ ] **Step 3: Commit 测试**

```bash
git add tests/test_login_page_markup.py
git commit -m "$(cat <<'EOF'
test: 增加登录页视觉改版 markup 契约

EOF
)"
```

---

### Task 2: 重写 login.html 布局与 SVG logo

**Files:**
- Modify: `src/pages/login.html`（整体替换 `<style>` 与 `<body>` 内结构；保留底部登录 script 逻辑）
- Test: `tests/test_login_page_markup.py`

**Interfaces:**
- Consumes: Task 1 契约（`login-logo`、pill 文案、`data-login-*`）
- Produces: 浅色分栏登录页；内联 SVG XL logo；保留 `hrApi.login` 流程

- [ ] **Step 1: 替换页内样式与 markup（保留 script）**

将 `src/pages/login.html` 的 `<style>` 与 `<main>...</main>` 改为以下结构（script 块保持现有登录逻辑不变）：

```html
<style>
  :root {
    --login-ink: #0f172a;
    --login-muted: #64748b;
    --login-line: #e2e8f0;
    --login-primary: #3b82f6;
    --login-bg-top: #e0f2fe;
    --login-bg-bottom: #ffffff;
  }

  body {
    margin: 0;
    color: var(--login-ink);
    background: linear-gradient(180deg, var(--login-bg-top) 0%, var(--login-bg-bottom) 72%);
    min-height: 100vh;
    font-family: "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
  }

  .login-stage {
    position: relative;
    min-height: 100vh;
    display: grid;
    place-items: center;
    padding: 48px 32px;
    overflow: hidden;
  }

  .login-stage::before,
  .login-stage::after {
    content: "";
    position: absolute;
    border: 1.5px solid rgba(255, 255, 255, 0.55);
    border-radius: 50%;
    pointer-events: none;
  }

  .login-stage::before {
    width: 520px;
    height: 520px;
    top: -180px;
    right: -120px;
  }

  .login-stage::after {
    width: 360px;
    height: 360px;
    top: -40px;
    right: 40px;
    border-color: rgba(191, 219, 254, 0.7);
  }

  .login-shell {
    position: relative;
    z-index: 1;
    width: min(980px, 100%);
    display: grid;
    grid-template-columns: 1.05fr 0.95fr;
    gap: 48px;
    align-items: center;
  }

  .login-brief {
    padding: 12px 8px;
  }

  .login-logo {
    width: 72px;
    height: 72px;
    display: grid;
    place-items: center;
    filter: drop-shadow(0 10px 24px rgba(59, 130, 246, 0.28));
  }

  .login-logo svg {
    width: 72px;
    height: 72px;
    display: block;
  }

  .login-brief h1 {
    margin: 28px 0 0;
    font-size: clamp(32px, 4vw, 44px);
    line-height: 1.15;
    letter-spacing: -0.03em;
    font-weight: 800;
  }

  .login-brief p {
    margin: 12px 0 0;
    color: var(--login-ink);
    font-size: 16px;
    font-weight: 500;
  }

  .login-pills {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    margin-top: 28px;
  }

  .login-pill {
    padding: 8px 14px;
    border: 1px solid #e5e7eb;
    border-radius: 999px;
    background: #fff;
    color: #6b7280;
    font-size: 13px;
    box-shadow: 0 1px 2px rgba(15, 23, 42, 0.04);
  }

  .login-form {
    padding: 40px 36px;
    border-radius: 20px;
    background: #fff;
    box-shadow: 0 18px 50px rgba(15, 23, 42, 0.1);
  }

  .login-title {
    margin: 0 0 28px;
    font-size: 28px;
    font-weight: 800;
    letter-spacing: -0.03em;
  }

  .login-field {
    display: grid;
    gap: 8px;
    margin-bottom: 18px;
  }

  .login-field label {
    font-size: 13px;
    font-weight: 600;
    color: #64748b;
  }

  .login-field input {
    width: 100%;
    height: 48px;
    border: 1px solid var(--login-line);
    border-radius: 10px;
    padding: 0 14px;
    background: #fff;
    color: var(--login-ink);
    font-size: 15px;
    outline: none;
    box-sizing: border-box;
  }

  .login-field input:focus {
    border-color: var(--login-primary);
    box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.12);
  }

  .login-submit {
    width: 100%;
    height: 48px;
    margin-top: 8px;
    border: 0;
    border-radius: 10px;
    background: var(--login-primary);
    color: #fff;
    font-size: 16px;
    font-weight: 700;
    cursor: pointer;
  }

  .login-submit:hover {
    filter: brightness(1.05);
  }

  .login-message {
    min-height: 22px;
    margin-top: 12px;
    color: #b04435;
    font-size: 13px;
  }

  @media (max-width: 760px) {
    .login-stage { padding: 28px 18px; }
    .login-shell { grid-template-columns: 1fr; gap: 28px; }
    .login-form { padding: 28px 22px; }
  }
</style>
```

```html
<main class="login-stage">
  <section class="login-shell" aria-label="登录到 AI 招聘管理平台">
    <aside class="login-brief">
      <div class="login-logo" aria-label="XL">
        <svg viewBox="0 0 72 72" xmlns="http://www.w3.org/2000/svg" role="img">
          <defs>
            <filter id="login-hex-glow" x="-30%" y="-30%" width="160%" height="160%">
              <feDropShadow dx="0" dy="4" stdDeviation="4" flood-color="#93c5fd" flood-opacity="0.55"/>
            </filter>
          </defs>
          <polygon points="36,4 64,20 64,52 36,68 8,52 8,20" fill="#ffffff" opacity="0.85" filter="url(#login-hex-glow)"/>
          <polygon points="36,10 58,23 58,49 36,62 14,49 14,23" fill="#3b82f6"/>
          <text x="36" y="44" text-anchor="middle" fill="#ffffff" font-size="22" font-weight="800" font-family="Arial Black, Helvetica, sans-serif" letter-spacing="-1">XL</text>
        </svg>
      </div>
      <h1>AI招聘管理平台</h1>
      <p>人力资源管理系统 v3.0</p>
      <div class="login-pills">
        <span class="login-pill">智能招聘</span>
        <span class="login-pill">权限管理</span>
        <span class="login-pill">数据分析</span>
      </div>
    </aside>
    <form class="login-form" data-login-form>
      <h2 class="login-title">登录系统</h2>
      <div class="login-field">
        <label for="login-username">账号</label>
        <input id="login-username" data-login-username value="admin" autocomplete="username" />
      </div>
      <div class="login-field">
        <label for="login-password">密码</label>
        <input id="login-password" type="password" data-login-password value="admin123" autocomplete="current-password" />
      </div>
      <button class="login-submit" type="submit" data-login-submit>登录</button>
      <div class="login-message" data-login-message></div>
    </form>
  </section>
</main>
```

底部 `<script>` 保持现有实现（`hrApi.login`、token、`next` 跳转、`reason=kicked`）。

- [ ] **Step 2: 跑 markup 测试**

Run: `python -m pytest tests/test_login_page_markup.py -v`

Expected: PASS（若 Task 3 的 CSS 尚未改，markup 测试仍应 PASS）

- [ ] **Step 3: Commit**

```bash
git add src/pages/login.html
git commit -m "$(cat <<'EOF'
style: 登录页改为浅色分栏并加入 XL 六边形 logo

EOF
)"
```

---

### Task 3: 调整 styles.css 登录覆盖规则

**Files:**
- Modify: `styles.css`（约 3258–3268 行登录相关 `!important` 块）
- Test: `tests/test_login_page_markup.py`（回归）

**Interfaces:**
- Consumes: Task 2 的 class 名（`login-stage` / `login-shell` / `login-brief` / `login-form` / `login-submit` / `login-logo`）
- Produces: 全局样式不再把新登录页压成旧蓝栏卡片

- [ ] **Step 1: 替换登录覆盖块**

将 `styles.css` 中：

```css
/* Login follows the same restrained visual system. */
body:has(.login-stage) { color: var(--foreground) !important; background: var(--background) !important; }
.login-stage { padding: 32px 20px !important; background: var(--background) !important; }
.login-stage::before { display: none !important; }
.login-shell { border: 1px solid var(--border) !important; border-radius: 12px !important; background: #fff !important; box-shadow: var(--shadow-sm) !important; backdrop-filter: none !important; }
.login-brief { background: var(--primary) !important; }
.login-brief::before, .login-brief::after { display: none !important; }
.login-mark { border-radius: 12px !important; background: #fff !important; color: var(--primary) !important; box-shadow: none !important; }
.login-form-panel { background: #fff !important; }
.login-form-panel h2 { color: var(--foreground) !important; font-weight: 600 !important; }
.login-submit { border-radius: 8px !important; background: var(--primary) !important; box-shadow: none !important; }
```

替换为：

```css
/* Login page owns its visual system in login.html; do not flatten it here. */
body:has(.login-stage) {
  color: #0f172a !important;
  background: linear-gradient(180deg, #e0f2fe 0%, #ffffff 72%) !important;
}
.login-stage {
  padding: 48px 32px !important;
  background: transparent !important;
}
.login-shell {
  border: 0 !important;
  border-radius: 0 !important;
  background: transparent !important;
  box-shadow: none !important;
  backdrop-filter: none !important;
}
.login-brief {
  background: transparent !important;
  color: #0f172a !important;
}
.login-brief::before,
.login-brief::after {
  display: none !important;
}
.login-form {
  background: #fff !important;
  border-radius: 20px !important;
  box-shadow: 0 18px 50px rgba(15, 23, 42, 0.1) !important;
}
.login-submit {
  border-radius: 10px !important;
  background: #3b82f6 !important;
  box-shadow: none !important;
}
```

- [ ] **Step 2: 回归测试**

Run: `python -m pytest tests/test_login_page_markup.py -v`

Expected: PASS

- [ ] **Step 3: 浏览器目视验收**

1. 打开 `src/pages/login.html`（需后端可用时可实际登录）
2. 确认：浅色背景、六边形 XL、三 pill、右侧白卡
3. 确认：错误密码有失败提示；`?reason=kicked` 提示仍在
4. 窄屏宽度下品牌在上、表单在下

- [ ] **Step 4: 更新三份 MD 并最终提交推送**

在 `progress.md` / `findings.md` / `task_plan.md` 顶部追加本次完成记录；`task_plan.md` 的 Current Phase 改为登录页改版已完成。

```bash
git add styles.css progress.md findings.md task_plan.md
git commit -m "$(cat <<'EOF'
style: 放开登录页全局样式覆盖以适配浅色分栏

EOF
)"
git push -u origin HEAD
```

---

## Spec Coverage Check

| Spec 要求 | Task |
|-----------|------|
| 浅蓝→白渐变背景 + 右上弧线 | Task 2 |
| 左右分栏 / 窄屏堆叠 | Task 2 |
| 六边形 XL SVG logo | Task 2 |
| 标题 / 副标题 / 三 pill | Task 2 |
| 右侧白卡登录表单 | Task 2 |
| 保留 auth hooks / kicked | Task 1 + Task 2 |
| 去掉旧脚注 / login-mark | Task 1 + Task 2 |
| 调整 styles.css !important | Task 3 |
| 不改登录 API | 全局约束（未改 frontend-api） |

## Placeholder Scan

无 TBD / TODO / “类似 Task N” 占位。
