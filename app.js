const nav = [
  ["dashboard.html", "首页", "概览"],
  ["candidates.html", "求职者数据池", "资源"],
  ["import.html", "简历导入", "导入"],
  ["customers.html", "客户管理", "客户"],
  ["projects.html", "项目管理", "项目"],
  ["positions.html", "岗位管理", "岗位"],
  ["evaluations.html", "评价体系", "评价"],
  ["warranty.html", "质保期管理", "质保"],
  ["notifications.html", "通知提醒", "通知"],
  ["statistics.html", "统计管理", "报表"],
  ["users.html", "用户管理", "账号"],
  ["roles.html", "角色管理", "角色"],
  ["permissions.html", "权限管理", "权限"],
  ["data-permissions.html", "数据权限", "范围"],
  ["dictionary.html", "标签字典", "标签"],
  ["ai-center.html", "AI能力中心", "AI"],
  ["system-config.html", "系统配置", "系统"],
  ["logs.html", "操作日志", "日志"],
  ["db-explorer.html", "数据探针", "探针"],
];

const parseId = (val) => {
  if (val === undefined || val === null || val === '') return 0;
  const num = Number(val);
  return isNaN(num) ? String(val) : num;
};

const pages = {
  dashboard: {
    crumbs: "首页 / 数据看板",
    title: "招聘交付驾驶舱",
    desc: "围绕客户项目、岗位推进与候选人流转的一体化管理视图。重点呈现交付漏斗、团队效率与待办风险。",
  },
  candidates: {
    crumbs: "求职者 / 数据池",
    title: "求职者数据池",
    desc: "高密度候选人检索工作台，支持搜索、筛选、锁定、释放和导出，围绕岗位匹配高效筛人。",
  },
  import: {
    crumbs: "求职者 / 简历导入",
    title: "简历导入",
    desc: "接收外部程序下载好的简历池数据，完成批量导入、解析结果查看和失败重试。",
  },
  customers: {
    crumbs: "客户管理 / 客户列表",
    title: "客户管理",
    desc: "管理甲方公司及其下属招聘项目，查看客户交付进度与推进概况。",
  },
  projects: {
    crumbs: "客户管理 / 项目管理",
    title: "项目管理",
    desc: "以招聘包为单位管理多个岗位，跟踪项目状态、等级、人数与进度。",
  },
  positions: {
    crumbs: "项目管理 / 岗位管理",
    title: "岗位管理",
    desc: "统一管理项目下的岗位、紧急程度、薪资范围与状态流转。",
  },
  evaluations: {
    crumbs: "评价 / 评价管理",
    title: "评价体系",
    desc: "记录候选人在面试和推进过程中的轮次评价，保留评分、内容、评价人和时间。",
  },
  warranty: {
    crumbs: "系统设置 / 质保期管理",
    title: "质保期管理",
    desc: "统一配置质保期并监控候选人到期状态，支持到期提醒与重新激活。",
  },
  notifications: {
    crumbs: "通知提醒 / 通知列表",
    title: "通知提醒",
    desc: "承接导入、候选人、评价、质保和系统事件的站内消息，支持查看、已读与跳转。",
  },
  statistics: {
    crumbs: "统计 / 数据大屏",
    title: "统计管理",
    desc: "展示简历导入、推荐、面试、录用、留存和团队绩效等经营指标。",
  },
  users: { crumbs: "系统设置 / 用户管理", title: "用户管理", desc: "管理系统内部账号及其组织归属。" },
  roles: { crumbs: "系统设置 / 角色管理", title: "角色管理", desc: "定义管理员、组长、组员等角色及权限模板。" },
  permissions: { crumbs: "系统设置 / 权限管理", title: "权限管理", desc: "配置功能权限与操作权限。" },
  "data-permissions": { crumbs: "系统设置 / 数据权限", title: "数据权限", desc: "配置不同组织范围可见的客户、项目与候选人数据。" },
  dictionary: { crumbs: "系统设置 / 标签字典", title: "标签字典", desc: "统一候选人、岗位与项目标签口径。" },
  "ai-center": { crumbs: "AI中心 / 能力总览", title: "AI能力中心", desc: "提供简历解析、JD 生成和智能推荐任务入口，并记录任务结果。" },
  "system-config": { crumbs: "系统设置 / 系统配置", title: "系统配置", desc: "管理系统名称、邮件配置、水印和响应式规则。" },
  logs: { crumbs: "系统设置 / 操作日志", title: "操作日志", desc: "查看导入、推荐、权限变更等关键操作记录。" },
  "db-explorer": {
    crumbs: "系统设置 / 数据探针",
    title: "数据库资源探针",
    desc: "直接读取与呈现系统底层的数据库实体物理表数据，适配 SQLite / PostgreSQL，用于开发辅助及状态查验。"
  },
};

const icons = {
  home: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 11.5 12 4l9 7.5"/><path d="M5 10.5V20h14v-9.5"/><path d="M9 20v-6h6v6"/></svg>`,
  users: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M17 21v-2a4 4 0 0 0-4-4H7a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>`,
  file: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M14 2H7a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6"/></svg>`,
  building: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 21h18"/><path d="M5 21V7l7-3v17"/><path d="M19 21V10l-7-3"/><path d="M9 9h1"/><path d="M9 13h1"/><path d="M9 17h1"/><path d="M15 13h1"/><path d="M15 17h1"/></svg>`,
  star: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m12 3 2.8 5.7 6.3.9-4.5 4.4 1 6.3L12 17.8 6.4 20.3l1-6.3-4.5-4.4 6.3-.9z"/></svg>`,
  chart: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 19V5"/><path d="M4 19h16"/><path d="M8 16v-5"/><path d="M12 16V9"/><path d="M16 16v-3"/></svg>`,
  settings: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 2v2"/><path d="M12 20v2"/><path d="M4.93 4.93l1.41 1.41"/><path d="M17.66 17.66l1.41 1.41"/><path d="M2 12h2"/><path d="M20 12h2"/><path d="M4.93 19.07l1.41-1.41"/><path d="M17.66 6.34l1.41-1.41"/><circle cx="12" cy="12" r="3.5"/></svg>`,
  inbox: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 12h-6l-2 3h-4l-2-3H2"/><path d="M5 4h14a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2h-3l-2 3H8l-2-3H3a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2Z"/></svg>`,
  log: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 7h16"/><path d="M4 12h16"/><path d="M4 17h10"/></svg>`,
  bell: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M15 17H5a2 2 0 0 0 2-2v-4a5 5 0 1 1 10 0v4a2 2 0 0 0 2 2z"/><path d="M13.73 21a2 2 0 0 1-3.46 0"/></svg>`,
  dot: `<svg viewBox="0 0 8 8" fill="currentColor" aria-hidden="true"><circle cx="4" cy="4" r="4"/></svg>`,
};

function getNavVisibility(role) {
  const normalized = String(role || "").toLowerCase();
  if (String(role || "").includes("超级") || normalized.includes("admin")) {
    return new Set(nav.map(([href]) => href));
  }
  if (String(role || "").includes("组长") || String(role || "").includes("主管") || normalized.includes("leader")) {
    return new Set([
      "dashboard.html",
      "candidates.html",
      "import.html",
      "customers.html",
      "positions.html",
      "projects.html",
      "evaluations.html",
      "warranty.html",
      "notifications.html",
      "statistics.html",
      "permissions.html",
      "data-permissions.html",
      "ai-center.html",
      "system-config.html",
      "logs.html",
      "db-explorer.html",
    ]);
  }
  return new Set([
    "dashboard.html",
      "candidates.html",
      "import.html",
      "customers.html",
      "positions.html",
      "projects.html",
      "evaluations.html",
      "notifications.html",
    "ai-center.html",
    "db-explorer.html",
  ]);
}

function shell(pageKey, body, currentUser = null) {
  const active = (p) => p === `${pageKey}.html` || (pageKey === "index" && p === "dashboard.html");
  const visible = getNavVisibility(currentUser?.role || currentUser?.role_name || "超级管理员");
  const navHtml = nav.filter(([href]) => visible.has(href)).map(([href, label, badge]) => `
    <a class="nav-item ${active(href) ? "active" : ""}" href="./${href}">
      <span class="nav-icon">${badge === "概览" ? icons.home : badge === "资源" ? icons.users : badge === "导入" ? icons.file : badge === "客户" ? icons.building : badge === "项目" ? icons.inbox : badge === "评价" ? icons.star : badge === "质保" ? icons.settings : badge === "报表" ? icons.chart : badge === "账号" ? icons.users : badge === "角色" ? icons.settings : badge === "权限" ? icons.settings : badge === "范围" ? icons.settings : badge === "标签" ? icons.settings : badge === "探针" ? icons.settings : icons.log}</span>
      <span>${label}</span>
      <span class="nav-badge">${badge}</span>
    </a>`).join("");
  return `
  <div class="app-shell">
    <aside class="sidebar">
      <div class="brand">
        <div class="brand-mark">招</div>
        <div>
          <h1>招聘管理平台</h1>
          <p>人力资源招聘管理系统 v3.0</p>
        </div>
      </div>
      <div class="nav-group">
        <div class="nav-title">主要功能</div>
        ${navHtml}
      </div>
    </aside>
    <main class="content">
      <div class="topbar">
        <div>
          <div class="crumbs">${pages[pageKey]?.crumbs || "招聘管理平台"}</div>
          <h2 class="page-title" style="margin-top:0;">${pages[pageKey]?.title || "招聘管理平台"}</h2>
          ${pages[pageKey]?.desc ? `<p class="page-lede">${pages[pageKey].desc}</p>` : ""}
        </div>
        <div class="top-actions">
          <div class="pill" aria-label="通知"><span class="nav-icon" style="background:var(--primary)"></span><strong>3</strong></div>
          <div class="user-chip"><div class="avatar"></div><div><div style="font-weight:700">${currentUser?.full_name || "管理员"}</div><div class="small-muted">${currentUser?.role || "超级管理员"}</div></div></div>
        </div>
      </div>
      ${body}
    </main>
  </div>`;
}

async function render() {
  const page = location.pathname.split("/").pop() || "dashboard.html";
  const key = page.replace(".html", "");
  const el = document.getElementById("app");
  if (!el) return;
  let currentUser = null;
  try {
    currentUser = await window.hrApi.me();
  } catch (err) {
    console.warn(err);
  }
  const visible = getNavVisibility(currentUser?.role || currentUser?.role_name || "超级管理员");
  if (!visible.has(page) && page !== "dashboard.html") {
    el.innerHTML = shell("dashboard", `
      <section class="panel">
        <h3>当前角色无访问权限</h3>
        <p class="panel-sub">当前登录角色暂未开放 ${page} 对应页面，请联系管理员开通权限。</p>
        <div class="list"><div class="list-item"><div class="item-meta">权限矩阵已在页面菜单上收口，直接访问该页面也会被拦截。</div></div></div>
      </section>
    `, currentUser);
    bindActionButtons();
    return;
  }
  el.innerHTML = shell(key, window.__PAGE_BODY__ || "", currentUser);
  bindActionButtons();
}

function ensureToastHost() {
  let host = document.getElementById("toast-host");
  if (!host) {
    host = document.createElement("div");
    host.id = "toast-host";
    host.style.position = "fixed";
    host.style.right = "16px";
    host.style.bottom = "16px";
    host.style.display = "grid";
    host.style.gap = "8px";
    host.style.zIndex = "9999";
    host.style.pointerEvents = "none";
    document.body.appendChild(host);
  }
  return host;
}

function showToast(message) {
  const host = ensureToastHost();
  const toast = document.createElement("div");
  toast.textContent = message;
  toast.style.padding = "10px 12px";
  toast.style.borderRadius = "10px";
  toast.style.background = "rgba(24,35,53,0.96)";
  toast.style.color = "#fff";
  toast.style.boxShadow = "0 12px 28px rgba(0,0,0,.18)";
  toast.style.maxWidth = "320px";
  toast.style.pointerEvents = "none";
  host.appendChild(toast);
  setTimeout(() => toast.remove(), 2200);
}

function getCandidateFilterSummary() {
  const keyword = document.querySelector('[data-field="candidate-keyword"]')?.value?.trim() || "";
  const city = document.querySelector('[data-field="candidate-city"]')?.value?.trim() || "";
  const status = document.querySelector('[data-field="candidate-status"]')?.value?.trim() || "";
  const parts = [];
  parts.push(`关键词：${keyword || "全部"}`);
  parts.push(`城市：${city || "全部"}`);
  parts.push(`职位：${status || "全部"}`);
  return {
    keyword,
    city,
    status,
    summary: parts.join(" · "),
  };
}

function syncSearchPresetModal() {
  const modal = document.querySelector('[data-search-preset-modal]');
  if (!modal) return;
  const summary = document.querySelector('[data-search-preset-summary]');
  const nameInput = document.querySelector('[data-search-preset-name]');
  const filter = getCandidateFilterSummary();
  modal.dataset.filterSummary = filter.summary;
  if (summary) summary.textContent = filter.summary;
  if (nameInput && !nameInput.value.trim()) {
    nameInput.value = `快捷搜索-${Date.now().toString(36)}`;
  }
}

async function handleGlobalButton(button) {
  const text = (button.textContent || "").trim();
  const page = location.pathname.split("/").pop() || "";
  const uniq = `${Date.now().toString(36)}-${Math.random().toString(36).slice(2, 6)}`;
  const refreshUserStats = async () => {
    const users = await window.hrApi.users();
    const total = document.querySelector('[data-user-total]');
    const active = document.querySelector('[data-user-active]');
    const pending = document.querySelector('[data-user-pending]');
    const leader = document.querySelector('[data-user-leader]');
    if (total) total.textContent = String(users.length);
    if (active) active.textContent = String(users.filter(u => u.is_active).length);
    if (pending) pending.textContent = String(users.filter(u => !u.is_active).length);
    if (leader) leader.textContent = String(users.filter(u => String(u.role).includes('组长') || String(u.role).includes('主管')).length);
  };
  const refreshRoleList = async () => {
    const roles = await window.hrApi.roles();
    const list = document.querySelector('[data-role-list]');
    if (list) list.innerHTML = roles.map(r => `<div class="list-item"><div class="item-top"><div><div class="item-title">${r.name}</div><div class="item-meta">${r.code} · ${r.description}</div></div><div class="table-actions"><button class="btn-sm" data-action="toggle-role" data-id="${r.id}">操作</button></div><span class="chip primary">角色</span></div></div>`).join('');
  };
  const refreshCompanyMetrics = async () => {
    const [companies, projects, deliveries] = await Promise.all([window.hrApi.companies(), window.hrApi.projects(), window.hrApi.deliveries()]);
    const total = document.querySelector('[data-company-total]');
    const project = document.querySelector('[data-company-projects]');
    const delivery = document.querySelector('[data-company-delivery]');
    const score = document.querySelector('[data-company-score]');
    if (total) total.textContent = String(companies.length);
    if (project) project.textContent = String(projects.length);
    if (delivery) delivery.textContent = String(deliveries.length);
    if (score) score.textContent = deliveries.length ? (4.0 + Math.min(0.9, deliveries.length / 100)).toFixed(1) : '0.0';
  };
  const refreshProjectMetrics = async () => {
    const projects = await window.hrApi.projects();
    const total = document.querySelector('[data-project-total]');
    const active = document.querySelector('[data-project-active]');
    const finished = document.querySelector('[data-project-finished]');
    const urgent = document.querySelector('[data-project-urgent]');
    if (total) total.textContent = String(projects.length);
    if (active) active.textContent = String(projects.filter(p => p.status !== '招聘完毕').length);
    if (finished) finished.textContent = String(projects.filter(p => p.status === '招聘完毕').length);
    if (urgent) urgent.textContent = String(projects.filter(p => (p.hiring_count || 0) > 5).length);
  };
  const downloadCsv = (rows) => {
    const header = ['id','actor','module','action','target_type','target_id','result','detail','created_at'];
    const lines = [header.join(',')];
    rows.forEach((row) => {
      const values = header.map((key) => `"${String(row?.[key] ?? '').replaceAll('"', '""')}"`);
      lines.push(values.join(','));
    });
    const blob = new Blob([lines.join('\n')], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `audit-logs-${new Date().toISOString().slice(0, 19).replaceAll(':', '-')}.csv`;
    a.click();
    URL.revokeObjectURL(url);
  };
  if (button.dataset.action === "nav-dashboard") return location.href = "./dashboard.html";
  if (button.dataset.action === "nav-candidates") return location.href = "./candidates.html";
  if (button.dataset.action === "nav-import") return location.href = "./import.html";
  if (button.dataset.action === "nav-projects") return location.href = "./projects.html";
  if (button.dataset.action === "refresh-page") return location.reload();
  if (button.dataset.action === "refresh-audit-logs") {
    const rows = await window.hrApi.auditLogs({ limit: 200 });
    const list = document.querySelector('[data-audit-list]');
    const detail = document.querySelector('[data-audit-detail]');
    if (list) {
      list.innerHTML = rows.map((log, index) => `
        <div class="list-item" data-log-index="${index}">
          <div class="item-top">
            <div>
              <div class="item-title">${log.actor}</div>
              <div class="item-meta">${log.module} · ${log.action} · ${log.created_at}</div>
              <div class="item-meta mono">${log.target_type || 'none'} / ${log.target_id || 'none'}</div>
            </div>
            <div class="table-actions">
              <button class="btn-sm" data-action="view-audit-log" data-log-index="${index}">查看详情</button>
              <button class="btn-sm" data-action="jump-audit-module" data-module="${log.module}">跳转模块</button>
            </div>
            <span class="chip ${log.result === '成功' ? 'success' : 'neutral'}">${log.result}</span>
          </div>
        </div>
      `).join('') || '<div class="list-item"><div class="item-meta">当前筛选条件下没有日志。</div></div>';
    }
    if (detail && rows[0]) {
      detail.innerHTML = `
        <div class="list-item"><div class="item-top"><div><div class="item-title">${rows[0].action}</div><div class="item-meta">${rows[0].module} · ${rows[0].actor}</div></div><span class="chip ${rows[0].result === '成功' ? 'success' : 'neutral'}">${rows[0].result}</span></div></div>
        <div class="list-item"><div class="item-top"><div><div class="item-title">对象</div><div class="item-meta">${rows[0].target_type || 'none'} / ${rows[0].target_id || 'none'}</div></div></div></div>
        <div class="list-item"><div class="item-top"><div><div class="item-title">详情</div><div class="item-meta">${rows[0].detail || '无'}</div></div></div></div>
        <div class="list-item"><div class="item-top"><div><div class="item-title">时间</div><div class="item-meta mono">${rows[0].created_at}</div></div></div></div>
      `;
    }
    showToast('日志已刷新');
    return;
  }
  if (button.dataset.action === "export-audit-logs") {
    const rows = await window.hrApi.auditLogs({ limit: 200 });
    downloadCsv(rows);
    showToast('已导出当前筛选结果');
    return;
  }
  if (button.dataset.action === "view-audit-log") {
    const index = Number(button.dataset.logIndex || 0);
    const rows = await window.hrApi.auditLogs({ limit: 200 });
    const row = rows[index];
    const detail = document.querySelector('[data-audit-detail]');
    if (detail && row) {
      detail.innerHTML = `
        <div class="list-item"><div class="item-top"><div><div class="item-title">${row.action}</div><div class="item-meta">${row.module} · ${row.actor}</div></div><span class="chip ${row.result === '成功' ? 'success' : 'neutral'}">${row.result}</span></div></div>
        <div class="list-item"><div class="item-top"><div><div class="item-title">对象</div><div class="item-meta">${row.target_type || 'none'} / ${row.target_id || 'none'}</div></div></div></div>
        <div class="list-item"><div class="item-top"><div><div class="item-title">详情</div><div class="item-meta">${row.detail || '无'}</div></div></div></div>
        <div class="list-item"><div class="item-top"><div><div class="item-title">时间</div><div class="item-meta mono">${row.created_at}</div></div></div></div>
      `;
    }
    return;
  }
  if (button.dataset.action === "jump-audit-module") {
    const module = String(button.dataset.module || '');
    const mapping = [
      ['候选人池', 'candidates.html'],
      ['客户公司管理', 'customers.html'],
      ['项目管理', 'projects.html'],
      ['岗位管理', 'positions.html'],
      ['权限管理', 'permissions.html'],
      ['数据权限', 'data-permissions.html'],
      ['操作日志', 'logs.html'],
      ['系统配置', 'system-config.html'],
      ['邮件配置', 'system-config.html'],
    ];
    const target = mapping.find(([key]) => module.includes(key));
    if (target) {
      window.location.href = `./${target[1]}`;
    } else {
      showToast(`未找到 ${module} 的跳转入口`);
    }
    return;
  }
  if (button.dataset.action === "refresh-ai-tasks") {
    const tasks = await window.hrApi.aiTasks();
    const list = document.querySelector('[data-ai-task-list]');
    if (list) {
      list.innerHTML = tasks.slice(0, 5).map(t => `<div class="list-item"><div class="item-top"><div><div class="item-title">${t.task_type}</div><div class="item-meta">${t.input_text}</div><div class="item-meta mono">${t.output_text || ''}</div></div><span class="chip ${t.status === '完成' ? 'success' : 'neutral'}">${t.status}</span></div></div>`).join('') || '<div class="list-item"><div class="item-meta">暂无 AI 任务</div></div>';
    }
    showToast('AI 任务已刷新');
    return;
  }
  if (button.dataset.action === "refresh-notifications") {
    const items = await window.hrApi.notifications();
    const list = document.querySelector('[data-notification-list]');
    const total = document.querySelector('[data-notice-total]');
    const unread = document.querySelector('[data-notice-unread]');
    const types = document.querySelector('[data-notice-types]');
    if (list) {
      list.innerHTML = items.length ? items.map((notice) => `
        <div class="list-item ${notice.read ? '' : 'soft'}">
          <div class="item-top">
            <div>
              <div class="item-title">${notice.title}</div>
              <div class="item-meta">${notice.type || '通知'} · ${notice.user || ''}</div>
              <div class="item-meta mono">${notice.created_at || ''}${notice.target_path ? ` · 跳转：${notice.target_path}` : ''}</div>
            </div>
            <div style="display:flex; gap:8px; align-items:center;">
              <span class="chip ${notice.read ? 'neutral' : 'primary'}">${notice.read ? '已读' : '未读'}</span>
              <button class="btn-sm" data-action="view-notification" data-id="${notice.id}" data-target="${notice.target_path || ''}">查看</button>
              ${notice.read ? '' : `<button class="btn-sm primary" data-action="read-notification" data-id="${notice.id}">标记已读</button>`}
            </div>
          </div>
        </div>
      `).join('') : '<div class="list-item"><div class="item-meta">当前筛选条件下没有通知。</div></div>';
    }
    if (total) total.textContent = String(items.length);
    if (unread) unread.textContent = String(items.filter((item) => !item.read).length);
    if (types) types.textContent = String(new Set(items.map((item) => item.type || '通知')).size);
    showToast('通知已刷新');
    return;
  }
  if (button.dataset.action === "view-notification") {
    const itemId = Number(button.dataset.id || 0);
    const items = await window.hrApi.notifications();
    const current = items.find(item => item.id === itemId);
    const preview = document.querySelector('[data-notice-preview]');
    if (current && preview) {
      preview.innerHTML = `
        <div class="list-item"><div class="item-top"><div><div class="item-title">${current.title}</div><div class="item-meta">${current.type} · ${current.user}</div></div><span class="chip ${current.read ? 'neutral' : 'primary'}">${current.read ? '已读' : '未读'}</span></div></div>
        <div class="list-item"><div class="item-meta">${current.target_path || '暂无跳转地址'}</div></div>
        <div class="list-item"><div class="item-meta mono">${current.created_at}</div></div>
      `;
    }
    return;
  }
  if (button.dataset.action === "read-notification") {
    const item = await window.hrApi.readNotification(button.dataset.id);
    const items = await window.hrApi.notifications();
    const list = document.querySelector('[data-notification-list]');
    if (list) {
      list.innerHTML = items.length ? items.map((notice) => `
        <div class="list-item ${notice.read ? '' : 'soft'}">
          <div class="item-top">
            <div>
              <div class="item-title">${notice.title}</div>
              <div class="item-meta">${notice.type || '通知'} · ${notice.user || ''}</div>
              <div class="item-meta mono">${notice.created_at || ''}${notice.target_path ? ` · 跳转：${notice.target_path}` : ''}</div>
            </div>
            <div style="display:flex; gap:8px; align-items:center;">
              <span class="chip ${notice.read ? 'neutral' : 'primary'}">${notice.read ? '已读' : '未读'}</span>
              <button class="btn-sm" data-action="view-notification" data-id="${notice.id}" data-target="${notice.target_path || ''}">查看</button>
              ${notice.read ? '' : `<button class="btn-sm primary" data-action="read-notification" data-id="${notice.id}">标记已读</button>`}
            </div>
          </div>
        </div>
      `).join('') : '<div class="list-item"><div class="item-meta">当前筛选条件下没有通知。</div></div>';
    }
    if (item.target_path) location.href = item.target_path;
    return;
  }
  if (button.dataset.action === "search-candidates") {
    if (window.candidatesPageState) {
      window.candidatesPageState.applyFilters();
      showToast(`已按条件筛选 ${window.candidatesPageState.list.length} 条候选人`);
      return;
    }
    const keyword = document.querySelector('[data-field="candidate-keyword"]')?.value?.trim() || "";
    const city = document.querySelector('[data-field="candidate-city"]')?.value?.trim() || "";
    const items = await window.hrApi.candidates({ keyword, city });
    const target = document.querySelector('[data-candidate-results]');
    if (target) {
      target.innerHTML = items.slice(0, 6).map(i => `<div class="list-item"><div class="item-top"><div><div class="item-title">${i.name}</div><div class="item-meta">${i.current_title || ''} · ${i.city || ''}</div></div><span class="chip ${i.locked ? 'warning' : 'success'}">${i.locked ? '已锁定' : '可操作'}</span></div></div>`).join("") || '<div class="list-item"><div class="item-meta">没有找到匹配候选人</div></div>';
    }
    return;
    const mainTable = document.querySelector('.table-card');
    if (mainTable) {
      const rowHtml = items.slice(0, 8).map(i => `
            <div class="table-row">
              <div><input type="checkbox" aria-label="选择${i.name}" /></div>
              <div>
                <div class="row-title">
                  <div class="avatar-sm"></div>
                  <div>
                    <strong>${i.name}</strong>
                    <div class="row-sub">${i.city || ''} · ${i.current_title || ''}</div>
                  </div>
                </div>
                <div class="skills">
                  <span class="skill-tag">${i.source || '来源'}</span>
                  <span class="skill-tag">${i.locked ? '已锁定' : '未锁定'}</span>
                </div>
              </div>
              <div>${[i.gender, i.age ? i.age+'岁' : '', i.education, i.experience_years ? i.experience_years+'年' : ''].filter(Boolean).join(' / ') || '--'}</div>
              <div>${i.current_title || '--'}</div>
              <div>${i.city || '--'}</div>
              <div class="mono">${i.expected_salary || '--'}</div>
              <div>${i.source || '--'}</div>
              <div><span class="state ${i.locked ? 'locked' : 'active'}">${i.status || '未知'}</span></div>
              <div>
                <div class="row-sub">${i.created_at || ''}</div>
                <div class="table-actions" style="margin-top:8px;">
                  <button class="btn-sm primary" data-action="view-detail" data-id="${i.id}" data-title="${i.name}">详情</button>
                </div>
              </div>
            </div>
          `).join('') || `<div class="table-row"><div><input type="checkbox" aria-label="候选人空状态" disabled /></div><div><div class="row-title"><div class="avatar-sm"></div><div><strong>等待真实候选人数据</strong><div class="row-sub">候选人列表来自接口返回的数据库记录。</div></div></div></div><div>--</div><div>--</div><div>--</div><div class="mono">--</div><div>--</div><div><span class="state active">待同步</span></div><div><div class="row-sub">--</div></div></div>`;
      const marker = mainTable.querySelector('[data-candidate-empty]') || mainTable.querySelector('.table-row');
      if (marker) {
        const container = document.createElement('div');
        container.innerHTML = rowHtml;
        marker.replaceWith(...Array.from(container.children));
      }
    }
    const foot = document.querySelector('[data-candidate-foot]');
    if (foot) foot.textContent = `共 ${items.length} 条记录 · 每页 10 条`;
    showToast(`已按条件筛选 ${items.length} 条候选人`);
    return;
  }
  if (button.dataset.action === "save-search-preset") {
    const modal = document.querySelector('[data-search-preset-modal]');
    if (modal) modal.style.display = 'block';
    syncSearchPresetModal();
    return;
  }
  if (button.dataset.action === "open-search-preset-modal") {
    const modal = document.querySelector('[data-search-preset-modal]');
    if (modal) modal.style.display = 'block';
    syncSearchPresetModal();
    return;
  }
  if (button.dataset.action === "close-search-preset-modal") {
    const modal = document.querySelector('[data-search-preset-modal]');
    if (modal) modal.style.display = 'none';
    return;
  }
  if (button.dataset.action === "confirm-search-preset-upload") {
    const { keyword, city, status } = getCandidateFilterSummary();
    const name = document.querySelector('[data-search-preset-name]')?.value?.trim() || `快捷搜索-${uniq}`;
    const preset = await window.hrApi.createSearchPreset({ name, keyword, city, status, created_by: "admin" });
    const list = document.querySelector('[data-search-presets]');
    if (list) {
      const items = await window.hrApi.searchPresets();
      list.innerHTML = items.slice(0, 5).map(p => `<div class="list-item"><div class="item-top"><div><div class="item-title">${p.name}</div><div class="item-meta">${p.keyword || '全部关键词'} · ${p.city || '全部城市'} · ${p.status || '全部状态'}</div></div><span class="chip primary">${p.created_by}</span></div></div>`).join('');
    }
    const modal = document.querySelector('[data-search-preset-modal]');
    if (modal) modal.style.display = 'none';
    await window.hrApi.createNotification({ user: 'admin', title: `快捷搜索已保存：${preset.name}`, type: '系统通知', content: `${preset.keyword} / ${preset.city} / ${preset.status}`, target_path: './candidates.html', read: false });
    showToast(`已保存快捷搜索：${preset.name}`);
    return;
  }
  if (button.dataset.action === "open-export-modal") {
    const modal = document.querySelector('[data-export-modal]');
    if (modal) modal.style.display = 'block';
    const [candidates, companies, projects, positions, records] = await Promise.all([
      window.hrApi.candidates(),
      window.hrApi.companies(),
      window.hrApi.projects(),
      window.hrApi.positions(),
      window.hrApi.exportRecords(),
    ]);
    const candidateSel = document.querySelector('[data-export-candidate]');
    const companySel = document.querySelector('[data-export-company]');
    const projectSel = document.querySelector('[data-export-project]');
    const positionSel = document.querySelector('[data-export-position]');
    const history = document.querySelector('[data-export-history-modal]');
    if (candidateSel) candidateSel.innerHTML = candidates.map(c => `<option value="${c.id}">${c.name} · ${c.current_title || ''} · ${c.city || ''}</option>`).join('');
    if (companySel) companySel.innerHTML = companies.map(c => `<option value="${c.id}">${c.name}</option>`).join('');
    if (projectSel) projectSel.innerHTML = projects.map(p => `<option value="${p.id}">${p.name}</option>`).join('');
    if (positionSel) positionSel.innerHTML = positions.map(p => `<option value="${p.id}">${p.name}</option>`).join('');
    if (candidateSel && candidates[0]) candidateSel.value = String(candidates[0].id);
    if (history) history.innerHTML = records.slice(0, 5).map(r => `<div class="list-item"><div class="item-top"><div><div class="item-title">${r.file_name}</div><div class="item-meta">${r.company_name} · ${r.project_name} · ${r.position_name}</div><div class="item-meta mono">${r.format} · ${r.created_at}</div></div><span class="chip ${r.watermarked ? 'success' : 'neutral'}">${r.watermarked ? '带水印' : '无水印'}</span></div></div>`).join('') || '<div class="list-item"><div class="item-meta">暂无导出记录</div></div>';
    return;
  }
  if (button.dataset.action === "close-export-modal") {
    const modal = document.querySelector('[data-export-modal]');
    if (modal) modal.style.display = 'none';
    return;
  }
  if (button.dataset.action === "confirm-export-upload") {
    const candidateId = Number(document.querySelector('[data-export-candidate]')?.value || 0);
    const companyId = Number(document.querySelector('[data-export-company]')?.value || 0);
    const projectId = Number(document.querySelector('[data-export-project]')?.value || 0);
    const positionId = Number(document.querySelector('[data-export-position]')?.value || 0);
    const format = document.querySelector('[data-export-format]')?.value || 'PDF';
    if (!candidateId || !companyId || !projectId || !positionId) throw new Error('请先选择候选人、客户公司、项目和岗位');
    const candidates = await window.hrApi.candidates();
    const companies = await window.hrApi.companies();
    const projects = await window.hrApi.projects();
    const positions = await window.hrApi.positions();
    const candidate = candidates.find(c => c.id === candidateId);
    const company = companies.find(c => c.id === companyId);
    const project = projects.find(p => p.id === projectId);
    const position = positions.find(p => p.id === positionId);
    const exportRecord = await window.hrApi.createExportRecord({
      candidate_id: candidateId,
      candidate_name: candidate?.name || '',
      company_name: company?.name || '',
      project_name: project?.name || '',
      position_name: position?.name || '',
      format,
      watermarked: true,
      exported_by: 'admin',
      file_name: `${candidate?.name || '候选人'}-${position?.name || '岗位'}.${format.toLowerCase()}`,
      file_path: `/exports/${candidate?.name || 'candidate'}.${format.toLowerCase()}`,
    });
    const modal = document.querySelector('[data-export-modal]');
    if (modal) modal.style.display = 'none';
    const history = document.querySelector('[data-export-history]');
    if (history) {
      const current = await window.hrApi.exportRecords({ candidate_id: candidateId });
      history.innerHTML = current.map(r => `<div class="list-item"><div class="item-top"><div><div class="item-title">${r.file_name}</div><div class="item-meta">${r.company_name} · ${r.project_name} · ${r.position_name}</div><div class="item-meta mono">${r.format} · ${r.created_at}</div></div><span class="chip ${r.watermarked ? 'success' : 'neutral'}">${r.watermarked ? '带水印' : '无水印'}</span></div></div>`).join('');
    }
    await window.hrApi.createNotification({
      user: 'admin',
      title: `简历已导出：${exportRecord.file_name}`,
      type: '导出通知',
      content: `${exportRecord.candidate_name} 的简历已导出为 ${exportRecord.format}`,
      target_path: './candidates.html',
      read: false,
    });
    showToast(`已导出：${exportRecord.file_name}`);
    return;
  }
  if (button.dataset.action === "export-selected") {
    const checkedBoxes = Array.from(document.querySelectorAll('.table-card .table-row input[type="checkbox"]:checked'));
    const checkedIds = checkedBoxes.map(cb => Number(cb.dataset.id)).filter(Boolean);
    
    if (checkedIds.length === 0) {
      showToast("请先勾选需要导出的候选人简历");
      return;
    }

    const modal = document.querySelector('[data-export-modal]');
    if (modal) modal.style.display = 'block';
    
    const [candidates, companies, projects, positions, records] = await Promise.all([
      window.hrApi.candidates(),
      window.hrApi.companies(),
      window.hrApi.projects(),
      window.hrApi.positions(),
      window.hrApi.exportRecords(),
    ]);
    
    const filteredCandidates = candidates.filter(c => checkedIds.includes(c.id));
    
    const candidateSel = document.querySelector('[data-export-candidate]');
    const companySel = document.querySelector('[data-export-company]');
    const projectSel = document.querySelector('[data-export-project]');
    const positionSel = document.querySelector('[data-export-position]');
    const history = document.querySelector('[data-export-history-modal]');
    
    if (candidateSel) {
      candidateSel.innerHTML = filteredCandidates.map(c => `<option value="${c.id}">${c.name} · ${c.current_title || ''} · ${c.city || ''}</option>`).join('');
      if (filteredCandidates[0]) {
        candidateSel.value = String(filteredCandidates[0].id);
      }
    }
    if (companySel) companySel.innerHTML = companies.map(c => `<option value="${c.id}">${c.name}</option>`).join('');
    if (projectSel) projectSel.innerHTML = projects.map(p => `<option value="${p.id}">${p.name}</option>`).join('');
    if (positionSel) positionSel.innerHTML = positions.map(p => `<option value="${p.id}">${p.name}</option>`).join('');
    if (history) history.innerHTML = records.slice(0, 5).map(r => `<div class="list-item"><div class="item-top"><div><div class="item-title">${r.file_name}</div><div class="item-meta">${r.company_name} · ${r.project_name} · ${r.position_name}</div><div class="item-meta mono">${r.format} · ${r.created_at}</div></div><span class="chip ${r.watermarked ? 'success' : 'neutral'}">${r.watermarked ? '带水印' : '无水印'}</span></div></div>`).join('') || '<div class="list-item"><div class="item-meta">暂无导出记录</div></div>';
    return;
  }
  if (button.dataset.action === "recommendation-status") {
    const modal = document.querySelector('[data-recommendation-modal]');
    const title = document.querySelector('[data-recommendation-modal-title]');
    const desc = document.querySelector('[data-recommendation-modal-desc]');
    const statusSelect = document.querySelector('[data-recommendation-modal-status]');
    const id = Number(button.dataset.id);
    const status = button.dataset.status || "客户已收";
    if (modal) {
      modal.style.display = 'block';
      modal.dataset.target = JSON.stringify({ id });
    }
    if (title) title.textContent = `推荐记录 ${id} 状态确认`;
    if (desc) desc.textContent = `确认后将把推荐记录更新为 ${status}。`;
    if (statusSelect) statusSelect.value = status;
    return;
  }
  if (button.dataset.action === "close-recommendation-modal") {
    const modal = document.querySelector('[data-recommendation-modal]');
    if (modal) modal.style.display = 'none';
    return;
  }
  if (button.dataset.action === "confirm-recommendation-status") {
    const modal = document.querySelector('[data-recommendation-modal]');
    const target = modal?.dataset.target ? JSON.parse(modal.dataset.target) : null;
    const status = document.querySelector('[data-recommendation-modal-status]')?.value || "客户已收";
    const feedback = document.querySelector('[data-recommendation-modal-feedback]')?.value?.trim() || '';
    const customer_comment = document.querySelector('[data-recommendation-modal-comment]')?.value?.trim() || '';
    if (!target) throw new Error('没有待执行的推荐操作');
    const rec = await window.hrApi.updateRecommendation(target.id, { status, feedback, customer_comment });
    await window.hrApi.createRecommendationFeedback({
      recommendation_id: target.id,
      status,
      feedback: feedback || rec.feedback || '',
      customer_comment: customer_comment || rec.customer_comment || '',
      operator: 'admin',
    });
    await window.hrApi.createNotification({
      user: 'admin',
      title: `推荐状态已更新：${rec.status}`,
      type: '推荐通知',
      content: `推荐记录 ${rec.id} 已更新为 ${rec.status}，反馈：${rec.customer_comment || ''}`,
      target_path: './dashboard.html',
      read: false,
    });
    const rList = document.querySelector('[data-recommendation-list]');
    if (rList) {
      const items = await window.hrApi.recommendations();
      rList.innerHTML = items.slice(0, 3).map(r => `<div class="list-item"><div class="item-top"><div><div class="item-title">候选人 ${r.candidate_id} → 岗位 ${r.position_id}</div><div class="item-meta">${r.recommender} · ${r.status} · ${r.feedback || ''}${r.customer_comment ? ` · ${r.customer_comment}` : ''}</div></div><div class="table-actions"><button class="btn-sm primary" data-action="recommendation-status" data-id="${r.id}" data-status="客户已收">客户已收</button><button class="btn-sm" data-action="recommendation-status" data-id="${r.id}" data-status="客户未收">客户未收</button><button class="btn-sm" data-action="recommendation-status" data-id="${r.id}" data-status="安排面试">安排面试</button><button class="btn-sm" data-action="recommendation-status" data-id="${r.id}" data-status="拒绝">拒绝</button></div></div></div>`).join('');
    }
    const feedbackList = document.querySelector('[data-recommendation-feedback-list]');
    if (feedbackList) {
      const feedbacks = await window.hrApi.recommendationFeedbacks({ recommendation_id: target.id });
      feedbackList.innerHTML = feedbacks.map(f => `<div class="list-item"><div class="item-top"><div><div class="item-title">${f.status}</div><div class="item-meta">${f.feedback || '无反馈'}${f.customer_comment ? ` · ${f.customer_comment}` : ''}</div><div class="item-meta mono">${f.created_at}</div></div><span class="tag blue">${f.operator || 'admin'}</span></div></div>`).join('');
    }
    if (modal) modal.style.display = 'none';
    showToast(`推荐状态已更新：${rec.status}`);
    return;
  }
  if (button.dataset.action === "view-detail") {
    const title = button.dataset.title || text || "详情";
    // 保留字符串形式的 ID，兼容来自 Recruit 的字符串 agent_id
    const rawId = button.dataset.id ? String(button.dataset.id) : '';
    const modal = document.querySelector('[data-candidate-detail-modal]');
    const list = await window.hrApi.candidates();
    // 优先按 ID 字符串匹配，找不到则按姓名匹配
    const item = rawId
      ? list.find(i => String(i.id) === rawId)
      : (list.find(i => i.name === title) || list[0]);
    if (modal) modal.style.display = 'block';
    const resolvedId = item?.id != null ? String(item.id) : '';
    document.body.dataset.candidateId = resolvedId;
    document.querySelector('[data-candidate-detail-title]').textContent = `${item?.name || title} 详情`;
    document.querySelector('[data-candidate-detail-sub]').textContent = `${item?.source || '来源未知'} · ${item?.status || '状态未知'}`;
    const set = (sel, val) => { const el = document.querySelector(sel); if (el) el.textContent = val || '--'; };
    set('[data-candidate-detail-name]', item?.name);
    set('[data-candidate-detail-gender]', item?.gender);
    set('[data-candidate-detail-birth-date]', item?.birth_date);
    set('[data-candidate-detail-hukou]', item?.hukou_location);
    set('[data-candidate-detail-city]', item?.city);
    set('[data-candidate-detail-phone]', item?.phone);
    set('[data-candidate-detail-email]', item?.email);
    set('[data-candidate-detail-family]', item?.family_status);
    set('[data-candidate-detail-title2]', item?.current_title);
    set('[data-candidate-detail-education]', item?.education);
    set('[data-candidate-detail-exp]', item?.experience_years ? item.experience_years + '年' : null);
    set('[data-candidate-detail-edu-detail]', item?.education_detail);
    set('[data-candidate-detail-work-history]', item?.work_history);
    set('[data-candidate-detail-project-history]', item?.project_history);
    set('[data-candidate-detail-certificates]', item?.certificates);
    set('[data-candidate-detail-salary]', item?.expected_salary);
    set('[data-candidate-detail-salary-structure]', item?.salary_structure);
    set('[data-candidate-detail-onboard]', item?.onboard_cycle);
    set('[data-candidate-detail-job-status]', item?.job_status);
    set('[data-candidate-detail-intention]', item?.job_intention);
    set('[data-candidate-detail-core-value]', item?.core_value);
    set('[data-candidate-detail-evaluation]', item?.comprehensive_evaluation);
    set('[data-candidate-detail-status]', item?.locked ? '已锁定' : (item?.status || '激活'));
    set('[data-candidate-detail-source]', item?.source);
    set('[data-candidate-detail-idnumber]', item?.id_number);
    set('[data-candidate-detail-tags]', item?.tags);
    if (modal) modal.dataset.candidateId = resolvedId;
    const editBtn = document.querySelector('[data-candidate-detail-modal] [data-action="edit-candidate"]');
    if (editBtn) {
      editBtn.dataset.id = resolvedId;
    }
    if (window.updateCandidatePanels) {
      window.updateCandidatePanels(item?.id);
    }
    return;

  }
  if (button.dataset.action === "edit-candidate") {
    const list = await window.hrApi.candidates();
    const rawId = button.dataset.id ? String(button.dataset.id) : '';
    const item = list.find(i => String(i.id) === rawId);
    if (!item) throw new Error('未找到候选人');
    const modal = document.querySelector('[data-candidate-edit-modal]');
    const fill = (sel, val) => { const el = document.querySelector(sel); if (el) el.value = val || ''; };
    fill('[data-candidate-edit-name]', item.name);
    fill('[data-candidate-edit-gender]', item.gender);
    fill('[data-candidate-edit-birth-date]', item.birth_date);
    fill('[data-candidate-edit-hukou]', item.hukou_location);
    fill('[data-candidate-edit-city]', item.city);
    fill('[data-candidate-edit-phone]', item.phone);
    fill('[data-candidate-edit-email]', item.email);
    fill('[data-candidate-edit-idnumber]', item.id_number);
    fill('[data-candidate-edit-family]', item.family_status);
    fill('[data-candidate-edit-title]', item.current_title);
    fill('[data-candidate-edit-education]', item.education);
    fill('[data-candidate-edit-exp-years]', item.experience_years);
    fill('[data-candidate-edit-certificates]', item.certificates);
    fill('[data-candidate-edit-edu-detail]', item.education_detail);
    fill('[data-candidate-edit-work-history]', item.work_history);
    fill('[data-candidate-edit-project-history]', item.project_history);
    fill('[data-candidate-edit-salary]', item.expected_salary);
    fill('[data-candidate-edit-salary-structure]', item.salary_structure);
    fill('[data-candidate-edit-onboard]', item.onboard_cycle);
    fill('[data-candidate-edit-job-status]', item.job_status);
    fill('[data-candidate-edit-intention]', item.job_intention);
    fill('[data-candidate-edit-core-value]', item.core_value);
    fill('[data-candidate-edit-evaluation]', item.comprehensive_evaluation);
    fill('[data-candidate-edit-status]', item.locked ? '锁定' : (item.status || '激活'));
    fill('[data-candidate-edit-source]', item.source);
    fill('[data-candidate-edit-tags]', item.tags);
    if (modal) {
      modal.style.display = 'block';
      modal.dataset.candidateId = String(item.id);
      modal.dataset.target = JSON.stringify({ id: item.id });
    }
    return;
  }
  if (button.dataset.action === "close-candidate-edit-modal") {
    const modal = document.querySelector('[data-candidate-edit-modal]');
    if (modal) modal.style.display = 'none';
    return;
  }
  if (button.dataset.action === "confirm-candidate-edit") {
    const modal = document.querySelector('[data-candidate-edit-modal]');
    const target = modal?.dataset.target ? JSON.parse(modal.dataset.target) : null;
    if (!target) throw new Error('没有待编辑的候选人');
    const get = (sel) => document.querySelector(sel)?.value?.trim() || '';
    const payload = {
      phone: get('[data-candidate-edit-phone]'),
      email: get('[data-candidate-edit-email]'),
      current_title: get('[data-candidate-edit-title]'),
      city: get('[data-candidate-edit-city]'),
      status: get('[data-candidate-edit-status]') || '激活',
      source: get('[data-candidate-edit-source]'),
      gender: get('[data-candidate-edit-gender]'),
      birth_date: get('[data-candidate-edit-birth-date]'),
      hukou_location: get('[data-candidate-edit-hukou]'),
      id_number: get('[data-candidate-edit-idnumber]'),
      family_status: get('[data-candidate-edit-family]'),
      education: get('[data-candidate-edit-education]'),
      experience_years: parseInt(get('[data-candidate-edit-exp-years]')) || null,
      certificates: get('[data-candidate-edit-certificates]'),
      education_detail: get('[data-candidate-edit-edu-detail]'),
      work_history: get('[data-candidate-edit-work-history]'),
      project_history: get('[data-candidate-edit-project-history]'),
      expected_salary: get('[data-candidate-edit-salary]'),
      salary_structure: get('[data-candidate-edit-salary-structure]'),
      onboard_cycle: get('[data-candidate-edit-onboard]'),
      job_status: get('[data-candidate-edit-job-status]'),
      job_intention: get('[data-candidate-edit-intention]'),
      core_value: get('[data-candidate-edit-core-value]'),
      comprehensive_evaluation: get('[data-candidate-edit-evaluation]'),
      tags: get('[data-candidate-edit-tags]'),
    };
    const candidate = await window.hrApi.updateCandidate(target.id, payload);
    if (window.candidatesPageState) {
      const items = await window.hrApi.candidates();
      window.candidatesPageState.list = items;
      window.candidatesPageState.render();
      if (modal) modal.style.display = 'none';
      showToast(`候选人已更新：${candidate.name}`);
      
      const detailModal = document.querySelector('[data-candidate-detail-modal]');
      if (detailModal && detailModal.style.display === 'block') {
        const fakeBtn = {
          dataset: { action: 'view-detail', id: target.id },
          textContent: ''
        };
        handleGlobalButton(fakeBtn).catch(err => console.warn(err));
      }
      return;
    }
    const mainTable = document.querySelector('.table-card');
    if (mainTable) {
      const items = await window.hrApi.candidates();
      const rowHtml = items.slice(0, 8).map(i => `
            <div class="table-row">
              <div><input type="checkbox" aria-label="选择${i.name}" /></div>
              <div>
                <div class="row-title">
                  <div class="avatar-sm"></div>
                  <div>
                    <strong>${i.name}</strong>
                    <div class="row-sub">${i.city || ''} · ${i.current_title || ''}</div>
                  </div>
                </div>
                <div class="skills">
                  <span class="skill-tag">${i.source || '来源'}</span>
                  <span class="skill-tag">${i.locked ? '已锁定' : '未锁定'}</span>
                </div>
              </div>
              <div>${[i.gender, i.age ? i.age+'岁' : '', i.education, i.experience_years ? i.experience_years+'年' : ''].filter(Boolean).join(' / ') || '--'}</div>
              <div>${i.current_title || '--'}</div>
              <div>${i.city || '--'}</div>
              <div class="mono">${i.expected_salary || '--'}</div>
              <div>${i.source || '--'}</div>
              <div><span class="state ${i.locked ? 'locked' : 'active'}">${i.status || '未知'}</span></div>
              <div>
                <div class="row-sub">${i.created_at || ''}</div>
                <div class="table-actions" style="margin-top:8px;">
                  <button class="btn-sm primary" data-action="view-detail" data-id="${i.id}" data-title="${i.name}">详情</button>
                </div>
              </div>
            </div>
          `).join('');
      const marker = mainTable.querySelector('[data-candidate-empty]') || mainTable.querySelector('.table-row');
      if (marker) {
        const container = document.createElement('div');
        container.innerHTML = rowHtml;
        marker.replaceWith(...Array.from(container.children));
      }
    }
    if (modal) modal.style.display = 'none';
    showToast(`候选人已更新：${candidate.name}`);
    return;
  }
  if (button.dataset.action === "open-candidate-create-modal") {
    const modal = document.querySelector('[data-candidate-create-modal]');
    if (modal) modal.style.display = 'block';
    return;
  }
  if (button.dataset.action === "close-candidate-create-modal") {
    const modal = document.querySelector('[data-candidate-create-modal]');
    if (modal) modal.style.display = 'none';
    return;
  }
  if (button.dataset.action === "confirm-candidate-create") {
    const name = document.querySelector('[data-candidate-name]')?.value?.trim() || '';
    const phone = document.querySelector('[data-candidate-phone]')?.value?.trim() || '';
    const email = document.querySelector('[data-candidate-email]')?.value?.trim() || '';
    const currentTitle = document.querySelector('[data-candidate-title]')?.value?.trim() || '';
    const city = document.querySelector('[data-candidate-city-create]')?.value?.trim() || '';
    const source = document.querySelector('[data-candidate-source]')?.value?.trim() || '页面创建';
    if (!name || !phone) throw new Error('请先填写姓名和电话');
    const candidate = await window.hrApi.createCandidate({ name, phone, email, current_title: currentTitle, city, status: '激活', source });
    const modal = document.querySelector('[data-candidate-create-modal]');
    if (modal) modal.style.display = 'none';
    if (window.candidatesPageState) {
      const items = await window.hrApi.candidates();
      window.candidatesPageState.list = items;
      window.candidatesPageState.render();
      showToast(`已创建候选人：${candidate.name}`);
      return;
    }
    const mainTable = document.querySelector('.table-card');
    if (mainTable) {
      const items = await window.hrApi.candidates();
      const rowHtml = items.slice(0, 8).map(i => `
            <div class="table-row">
              <div><input type="checkbox" aria-label="选择${i.name}" /></div>
              <div>
                <div class="row-title">
                  <div class="avatar-sm"></div>
                  <div>
                    <strong>${i.name}</strong>
                    <div class="row-sub">${i.city || ''} · ${i.current_title || ''}</div>
                  </div>
                </div>
                <div class="skills">
                  <span class="skill-tag">${i.source || '来源'}</span>
                  <span class="skill-tag">${i.locked ? '已锁定' : '未锁定'}</span>
                </div>
              </div>
              <div>${[i.gender, i.age ? i.age+'岁' : '', i.education, i.experience_years ? i.experience_years+'年' : ''].filter(Boolean).join(' / ') || '--'}</div>
              <div>${i.current_title || '--'}</div>
              <div>${i.city || '--'}</div>
              <div class="mono">${i.expected_salary || '--'}</div>
              <div>${i.source || '--'}</div>
              <div><span class="state ${i.locked ? 'locked' : 'active'}">${i.status || '未知'}</span></div>
              <div>
                <div class="row-sub">${i.created_at || ''}</div>
                <div class="table-actions" style="margin-top:8px;">
                  <button class="btn-sm primary" data-action="view-detail" data-id="${i.id}" data-title="${i.name}">详情</button>
                </div>
              </div>
            </div>
          `).join('');
      const marker = mainTable.querySelector('[data-candidate-empty]') || mainTable.querySelector('.table-row');
      if (marker) {
        const container = document.createElement('div');
        container.innerHTML = rowHtml;
        marker.replaceWith(...Array.from(container.children));
      }
    }
    showToast(`已创建候选人：${candidate.name}`);
    return;
  }
  if (button.dataset.action === "close-candidate-detail-modal") {
    const modal = document.querySelector('[data-candidate-detail-modal]');
    if (modal) modal.style.display = 'none';
    return;
  }
  if (button.dataset.action === "toggle-candidate-lock") {
    const editModal = document.querySelector('[data-candidate-edit-modal]');
    const detailModal = document.querySelector('[data-candidate-detail-modal]');
    const candidateId = String(button.dataset.candidateId || editModal?.dataset.candidateId || detailModal?.dataset.candidateId || '');
    if (!candidateId || candidateId === '0') throw new Error('请先选择候选人');
    const candidate = await window.hrApi.candidates().then(list => list.find(i => String(i.id) === candidateId));
    if (!candidate) throw new Error('未找到候选人');
    const actionModal = document.querySelector('[data-candidate-action-modal]');
    const actionTitle = document.querySelector('[data-candidate-action-title]');
    const actionDesc = document.querySelector('[data-candidate-action-desc]');
    const nextAction = candidate.locked ? 'release-candidate' : 'lock-candidate';
    if (actionModal) {
      actionModal.style.display = 'block';
      actionModal.dataset.target = JSON.stringify({ id: candidateId, action: nextAction });
    }
    if (actionTitle) actionTitle.textContent = candidate.locked ? `释放候选人 ${candidate.name}` : `锁定候选人 ${candidate.name}`;
    if (actionDesc) actionDesc.textContent = candidate.locked ? '确认后将解除锁定，允许继续流转。' : '确认后将锁定该候选人，避免重复操作。';
    return;
  }
  if (button.dataset.action === "open-candidate-mail-modal") {
    const candidateId = String(button.dataset.candidateId || document.querySelector('[data-candidate-detail-modal]')?.dataset.candidateId || '');
    if (!candidateId || candidateId === '0') throw new Error('请先打开候选人详情');
    const candidate = await window.hrApi.candidates().then(list => list.find(i => String(i.id) === candidateId));
    if (!candidate) throw new Error('未找到候选人');
    const modal = document.querySelector('[data-candidate-mail-modal]');
    const title = document.querySelector('[data-candidate-mail-title]');
    const toInput = document.querySelector('[data-candidate-mail-to]');
    const subjectInput = document.querySelector('[data-candidate-mail-subject]');
    const bodyInput = document.querySelector('[data-candidate-mail-body]');
    const attachmentInput = document.querySelector('[data-candidate-mail-attachment]');
    if (title) title.textContent = `发送邮件：${candidate.name}`;
    if (toInput) toInput.value = candidate.email || '';
    if (subjectInput) subjectInput.value = `${candidate.name}-${candidate.current_title || '候选人'}`;
    if (bodyInput) bodyInput.value = `候选人：${candidate.name}\n电话：${candidate.phone || '--'}\n城市：${candidate.city || '--'}\n当前职位：${candidate.current_title || '--'}\n状态：${candidate.locked ? '已锁定' : '激活'}\n\n请查收候选人资料。`;
    if (attachmentInput) attachmentInput.value = `${candidate.name}-${candidate.current_title || '候选人'}.pdf`;
    if (modal) {
      modal.style.display = 'block';
      modal.dataset.candidateId = String(candidateId);
    }
    return;
  }
  if (button.dataset.action === "close-candidate-mail-modal") {
    const modal = document.querySelector('[data-candidate-mail-modal]');
    if (modal) modal.style.display = 'none';
    return;
  }
  if (button.dataset.action === "confirm-candidate-mail") {
    const modal = document.querySelector('[data-candidate-mail-modal]');
    const candidateId = modal?.dataset.candidateId || '';
    if (!candidateId || candidateId === '0') throw new Error('没有待发送邮件的候选人');
    const recipientEmail = document.querySelector('[data-candidate-mail-to]')?.value?.trim() || '';
    const subject = document.querySelector('[data-candidate-mail-subject]')?.value?.trim() || '';
    const body = document.querySelector('[data-candidate-mail-body]')?.value?.trim() || '';
    const attachmentName = document.querySelector('[data-candidate-mail-attachment]')?.value?.trim() || '';
    if (!recipientEmail || !subject || !attachmentName) throw new Error('请先填写收件人、主题和附件名');
    const record = await window.hrApi.createCandidateMailRecord({
      candidate_id: candidateId,
      recipient_email: recipientEmail,
      mail_subject: subject,
      mail_body: body,
      attachment_name: attachmentName,
      sent_by: 'admin',
      status: '已发送',
    });
    await window.hrApi.createNotification({
      user: 'admin',
      title: `邮件已发送：${subject}`,
      type: '邮件通知',
      content: `已发送给 ${recipientEmail}，附件 ${attachmentName}`,
      target_path: './candidates.html',
      read: false,
    });
    const history = document.querySelector('[data-mail-history]');
    if (history) {
      const list = await window.hrApi.candidateMailRecords({ candidate_id: candidateId });
      history.innerHTML = list.map(item => `<div class="list-item"><div class="item-top"><div><div class="item-title">${item.mail_subject}</div><div class="item-meta">${item.recipient_email} · ${item.attachment_name}</div><div class="item-meta mono">${item.status} · ${item.created_at}</div></div><span class="chip success">${item.sent_by || '发送'}</span></div></div>`).join('');
    }
    if (modal) modal.style.display = 'none';
    showToast(`已发送邮件：${record.mail_subject}`);
    return;
  }
  if (button.dataset.action === "open-candidate-salary-modal") {
    const candidateId = String(button.dataset.candidateId || document.querySelector('[data-candidate-edit-modal]')?.dataset.candidateId || document.querySelector('[data-candidate-detail-modal]')?.dataset.candidateId || '');
    if (!candidateId || candidateId === '0') throw new Error('请先选择候选人');
    const candidate = await window.hrApi.candidates().then(list => list.find(i => String(i.id) === candidateId));
    if (!candidate) throw new Error('未找到候选人');
    const modal = document.querySelector('[data-candidate-salary-modal]');
    const expectedEl = document.querySelector('[data-candidate-salary-expected]');
    const offeredEl = document.querySelector('[data-candidate-salary-offered]');
    const statusEl = document.querySelector('[data-candidate-salary-status]');
    const noteEl = document.querySelector('[data-candidate-salary-note]');
    // 先从数据库读取已有记录并回填，没有记录则用候选人的 expected_salary 作为预填充
    const existingList = await window.hrApi.salaryRecords({ candidate_id: candidateId });
    const existing = existingList && existingList[0];
    if (expectedEl) expectedEl.value = existing?.expected_salary || candidate.expected_salary || '';
    if (offeredEl) offeredEl.value = existing?.offered_salary || '';
    if (statusEl) statusEl.value = existing?.service_status || '未进行';
    if (noteEl) noteEl.value = existing?.note || '';
    if (modal) {
      modal.style.display = 'block';
      modal.dataset.candidateId = String(candidateId);
    }
    return;
  }
  if (button.dataset.action === "close-candidate-salary-modal") {
    const modal = document.querySelector('[data-candidate-salary-modal]');
    if (modal) modal.style.display = 'none';
    return;
  }
  if (button.dataset.action === "confirm-candidate-salary") {
    const modal = document.querySelector('[data-candidate-salary-modal]');
    const candidateId = modal?.dataset.candidateId || '';
    if (!candidateId || candidateId === '0') throw new Error('没有待保存的薪资记录');
    const expected_salary = document.querySelector('[data-candidate-salary-expected]')?.value?.trim() || '';
    const offered_salary = document.querySelector('[data-candidate-salary-offered]')?.value?.trim() || '';
    const service_status = document.querySelector('[data-candidate-salary-status]')?.value?.trim() || '未进行';
    const note = document.querySelector('[data-candidate-salary-note]')?.value?.trim() || '';
    const record = await window.hrApi.createSalaryRecord({ candidate_id: candidateId, expected_salary, offered_salary, service_status, note });
    const lifecycle = document.querySelector('[data-lifecycle-events]');
    if (lifecycle) {
      const list = await window.hrApi.salaryRecords({ candidate_id: candidateId });
      const salary = list[0];
      const current = lifecycle.innerHTML;
      const salaryCard = salary ? `<div class="list-item"><div class="item-top"><div><div class="item-title">薪资</div><div class="item-meta">${salary.expected_salary} / ${salary.offered_salary}</div></div><span class="chip warning">${salary.service_status}</span></div></div>` : '';
      lifecycle.innerHTML = current.includes('薪资') ? current : current + salaryCard;
    }
    if (modal) modal.style.display = 'none';
    showToast(`已保存薪资记录：${record.service_status}`);
    return;
  }
  if (button.dataset.action === "open-candidate-employment-modal") {
    const candidateId = String(button.dataset.candidateId || document.querySelector('[data-candidate-edit-modal]')?.dataset.candidateId || document.querySelector('[data-candidate-detail-modal]')?.dataset.candidateId || '');
    if (!candidateId || candidateId === '0') throw new Error('请先选择候选人');
    const candidate = await window.hrApi.candidates().then(list => list.find(i => String(i.id) === candidateId));
    if (!candidate) throw new Error('未找到候选人');
    const modal = document.querySelector('[data-candidate-employment-modal]');
    const statusEl = document.querySelector('[data-candidate-employment-status]');
    const company = document.querySelector('[data-candidate-employment-company]');
    const position = document.querySelector('[data-candidate-employment-position]');
    const onboard = document.querySelector('[data-candidate-employment-onboard]');
    const note = document.querySelector('[data-candidate-employment-note]');
    // 先从数据库读取已有记录并回填，没有记录则使用空默认值
    const existingList = await window.hrApi.employmentRecords({ candidate_id: candidateId });
    const existing = existingList && existingList[0];
    if (statusEl) statusEl.value = existing?.status || '未入职';
    if (company) company.value = existing?.company_name || '';
    if (position) position.value = existing?.position_name || candidate.current_title || '';
    if (onboard) onboard.value = existing?.onboard_date ? existing.onboard_date.slice(0, 10) : '';
    if (note) note.value = existing?.note || `候选人 ${candidate.name} 的入职状态记录`;
    if (modal) {
      modal.style.display = 'block';
      modal.dataset.candidateId = String(candidateId);
    }
    return;
  }
  if (button.dataset.action === "close-candidate-employment-modal") {
    const modal = document.querySelector('[data-candidate-employment-modal]');
    if (modal) modal.style.display = 'none';
    return;
  }
  if (button.dataset.action === "confirm-candidate-employment") {
    const modal = document.querySelector('[data-candidate-employment-modal]');
    const candidateId = modal?.dataset.candidateId || '';
    if (!candidateId || candidateId === '0') throw new Error('没有待保存的入职状态');
    const status = document.querySelector('[data-candidate-employment-status]')?.value?.trim() || '未入职';
    const company_name = document.querySelector('[data-candidate-employment-company]')?.value?.trim() || '';
    const position_name = document.querySelector('[data-candidate-employment-position]')?.value?.trim() || '';
    const onboardValue = document.querySelector('[data-candidate-employment-onboard]')?.value?.trim() || '';
    const note = document.querySelector('[data-candidate-employment-note]')?.value?.trim() || '';
    const payload = {
      candidate_id: candidateId,
      status,
      company_name,
      position_name,
      onboard_date: onboardValue ? new Date(onboardValue).toISOString() : null,
      note,
    };
    const record = await window.hrApi.createEmploymentRecord(payload);
    const lifecycle = document.querySelector('[data-lifecycle-events]');
    if (lifecycle) {
      const list = await window.hrApi.employmentRecords({ candidate_id: candidateId });
      const employment = list[0];
      const current = lifecycle.innerHTML;
      const employmentCard = employment ? `<div class="list-item"><div class="item-top"><div><div class="item-title">${employment.company_name}</div><div class="item-meta">${employment.position_name} · ${employment.status}</div></div><span class="chip neutral">入职</span></div></div>` : '';
      lifecycle.innerHTML = current.includes('入职') ? current : current + employmentCard;
    }
    if (modal) modal.style.display = 'none';
    showToast(`已保存入职状态：${record.status}`);
    return;
  }
  if (button.dataset.action === "open-candidate-followup-modal") {
    const candidateId = String(button.dataset.candidateId || document.querySelector('[data-candidate-edit-modal]')?.dataset.candidateId || document.querySelector('[data-candidate-detail-modal]')?.dataset.candidateId || '');
    if (!candidateId || candidateId === '0') throw new Error('请先选择候选人');
    const candidate = await window.hrApi.candidates().then(list => list.find(i => String(i.id) === candidateId));
    if (!candidate) throw new Error('未找到候选人');
    if (candidate.status !== '已录用') {
      throw new Error('仅已录用候选人可添加随访记录');
    }
    const modal = document.querySelector('[data-candidate-followup-modal]');
    const timeEl = document.querySelector('[data-candidate-followup-time]');
    const contentEl = document.querySelector('[data-candidate-followup-content]');
    // 随访记录是追加型（每次新建一条），时间默认为当前时间，内容清空让用户自己填
    if (timeEl) timeEl.value = new Date().toISOString().slice(0, 16);
    if (contentEl) contentEl.value = '';
    if (modal) {
      modal.style.display = 'block';
      modal.dataset.candidateId = String(candidateId);
    }
    return;
  }
  if (button.dataset.action === "close-candidate-followup-modal") {
    const modal = document.querySelector('[data-candidate-followup-modal]');
    if (modal) modal.style.display = 'none';
    return;
  }
  if (button.dataset.action === "confirm-candidate-followup") {
    const modal = document.querySelector('[data-candidate-followup-modal]');
    const candidateId = modal?.dataset.candidateId || '';
    if (!candidateId || candidateId === '0') throw new Error('没有待保存的随访记录');
    const follow_up_time = document.querySelector('[data-candidate-followup-time]')?.value?.trim() || '';
    const content = document.querySelector('[data-candidate-followup-content]')?.value?.trim() || '';
    if (!content) throw new Error('请填写随访内容');
    const record = await window.hrApi.createCandidateFollowUpRecord({
      candidate_id: candidateId,
      status: '已录用',
      follow_up_time: follow_up_time ? new Date(follow_up_time).toISOString() : null,
      content,
      operator: 'admin',
    });
    const lifecycle = document.querySelector('[data-lifecycle-events]');
    if (lifecycle) {
      const records = await window.hrApi.candidateFollowUpRecords({ candidate_id: candidateId });
      const followHtml = records.map(item => `<div class="list-item"><div class="item-top"><div><div class="item-title">${item.follow_up_time || item.created_at}</div><div class="item-meta">${item.content}</div></div><span class="chip primary">${item.status}</span></div></div>`).join('');
      const block = document.querySelector('[data-followup-block]');
      if (block) block.innerHTML = followHtml;
    }
    if (modal) modal.style.display = 'none';
    showToast(`已保存随访记录`);
    return;
  }
  if (button.dataset.action === "close-candidate-action-modal") {
    const modal = document.querySelector('[data-candidate-action-modal]');
    if (modal) modal.style.display = 'none';
    return;
  }
  if (button.dataset.action === "confirm-candidate-action") {
    const modal = document.querySelector('[data-candidate-action-modal]');
    const target = modal?.dataset.target ? JSON.parse(modal.dataset.target) : null;
    if (!target) throw new Error('没有待执行的候选人操作');
    const result = target.action === 'release-candidate' ? await window.hrApi.releaseCandidate(target.id) : await window.hrApi.lockCandidate(target.id);
      const detailStatus = document.querySelector('[data-candidate-detail-status]');
      if (detailStatus) detailStatus.textContent = result.locked ? '已锁定' : '激活';
      const followupButton = document.querySelector('[data-action="open-candidate-followup-modal"]');
      if (followupButton) followupButton.style.display = result.status === '已录用' ? '' : 'none';
      if (window.candidatesPageState) {
        const itemIndex = window.candidatesPageState.list.findIndex(i => 
          String(i.id) === String(result.id) || 
          (i.candidate_agent_id && String(i.candidate_agent_id) === String(result.candidate_agent_id))
        );
        if (itemIndex > -1) {
          window.candidatesPageState.list[itemIndex] = {
            ...window.candidatesPageState.list[itemIndex],
            id: result.id,
            locked: result.locked,
            status: result.status
          };
          window.candidatesPageState.render();
        }
      }
      const detailModal = document.querySelector('[data-candidate-detail-modal]');
      if (detailModal) {
        detailModal.dataset.candidateId = String(result.id);
      }
      const rows = document.querySelectorAll('.table-row');
    rows.forEach((row) => {
      const name = row.querySelector('strong')?.textContent?.trim();
      if (name !== result.name) return;
      const state = row.querySelector('.state');
      if (state) {
        state.textContent = result.locked ? '锁定' : '激活';
        state.className = `state ${result.locked ? 'locked' : 'active'}`;
      }
    });
    if (modal) modal.style.display = 'none';
    showToast(result.locked ? `已锁定：${result.name}` : `已释放：${result.name}`);
    return;
  }
  if (button.dataset.action === "open-import-modal") {
    const modal = document.querySelector('[data-import-modal]');
    if (modal) modal.style.display = 'block';
    return;
  }
  if (button.dataset.action === "open-batch-import-modal") {
    const modal = document.querySelector('[data-batch-import-modal]');
    if (modal) modal.style.display = 'block';
    return;
  }
  if (button.dataset.action === "close-import-modal") {
    const modal = document.querySelector('[data-import-modal]');
    if (modal) modal.style.display = 'none';
    return;
  }
  if (button.dataset.action === "close-batch-import-modal") {
    const modal = document.querySelector('[data-batch-import-modal]');
    if (modal) modal.style.display = 'none';
    return;
  }
  if (button.dataset.action === "import-smoke") {
    const fileInput = document.querySelector('[data-import-file]');
    const file = fileInput?.files?.[0];
    if (!file) throw new Error("请先在导入窗口选择真实简历文件");
    const allowed = [".doc", ".docx", ".pdf"];
    const name = (file.name || "").toLowerCase();
    if (!allowed.some(ext => name.endsWith(ext))) throw new Error("格式文件不符，请重新上传");
    const result = await window.hrApi.importSmoke(file);
    await window.hrApi.createNotification({
      user: "admin",
      title: `新简历导入：${result.candidate.name}`,
      type: "导入通知",
      content: `${result.candidate.name} 已进入候选人池，来源：${result.candidate.source || "导入"}`,
      target_path: "./candidates.html",
      read: false,
    });
    const records = document.querySelector(".import-records .timeline");
    if (records) {
      const row = document.createElement("div");
      row.className = "list-item soft";
      row.innerHTML = `<div class="item-top"><div><div class="item-title">刚刚导入</div><div class="item-meta">${result.candidate.name} 已进入候选人池</div></div><span class="tag green">成功</span></div>`;
      records.prepend(row);
    }
    const snapshot = document.querySelector("[data-candidate-results]");
    if (snapshot) {
      const item = result.candidate;
      snapshot.prepend(Object.assign(document.createElement("div"), { className: "list-item", innerHTML: `<div class="item-top"><div><div class="item-title">${item.name}</div><div class="item-meta">${item.current_title || ""} · ${item.city || ""} · ${item.status || ""}</div></div><span class="chip success">可操作</span></div>` }));
    }
    showToast(`导入成功：${result.candidate.name}`);
    return;
  }
  if (button.dataset.action === "confirm-import-upload") {
    const fileInput = document.querySelector('[data-import-file]');
    const file = fileInput?.files?.[0];
    if (!file) throw new Error("请先选择简历文件");
    const allowed = [".doc", ".docx", ".pdf"];
    const name = (file.name || "").toLowerCase();
    if (!allowed.some(ext => name.endsWith(ext))) throw new Error("格式文件不符，请重新上传");
    const result = await window.hrApi.importSmoke(file);
    await window.hrApi.createNotification({
      user: "admin",
      title: `新简历导入：${result.candidate.name}`,
      type: "导入通知",
      content: `${result.candidate.name} 已进入候选人池，来源：${result.candidate.source || "导入"}`,
      target_path: "./candidates.html",
      read: false,
    });
    const modal = document.querySelector('[data-import-modal]');
    if (modal) modal.style.display = "none";
    const preview = document.querySelector('[data-import-preview]');
    if (preview) preview.textContent = `已导入 ${file.name}，候选人 ${result.candidate.name} 已进入数据池，若有同名记录请在导入历史中复核。`;
    const records = document.querySelector(".import-records .timeline");
    if (records) {
      const row = document.createElement("div");
      row.className = "list-item soft";
      row.innerHTML = `<div class="item-top"><div><div class="item-title">${file.name}</div><div class="item-meta">${result.candidate.name} 已进入候选人池</div></div><span class="tag green">成功</span></div>`;
      records.prepend(row);
    }
    const historyItems = await window.hrApi.importRecords();
    const success = document.querySelector('[data-import-success]');
    const failed = document.querySelector('[data-import-failed]');
    const rate = document.querySelector('[data-import-rate]');
    const review = document.querySelector('[data-import-review]');
    if (success) success.textContent = String(historyItems.reduce((sum, i) => sum + Number(i.imported_count || 0), 0));
    if (failed) failed.textContent = String(historyItems.reduce((sum, i) => sum + Number(i.failed_count || 0), 0));
    if (rate) rate.textContent = historyItems.length ? `${((historyItems.reduce((sum, i) => sum + Number(i.imported_count || 0), 0) / Math.max(1, historyItems.reduce((sum, i) => sum + Number(i.imported_count || 0) + Number(i.failed_count || 0), 0))) * 100).toFixed(1)}%` : '0%';
    if (review) review.textContent = String(historyItems.filter(i => String(i.note || '').includes('复核')).length);
    if (records) {
      records.innerHTML = historyItems.slice(0, 5).map(i => `<div class="list-item soft"><div class="item-top"><div><div class="item-title">${i.file_name}</div><div class="item-meta">${i.imported_count} 成功 / ${i.failed_count} 失败 · ${i.note}</div></div><span class="tag ${i.status === '成功' ? 'green' : 'blue'}">${i.status}</span></div></div>`).join('');
    }
    const snapshot = document.querySelector("[data-candidate-results]");
    if (snapshot) {
      const item = result.candidate;
      snapshot.prepend(Object.assign(document.createElement("div"), { className: "list-item", innerHTML: `<div class="item-top"><div><div class="item-title">${item.name}</div><div class="item-meta">${item.current_title || ""} · ${item.city || ""} · ${item.status || ""}</div></div><span class="chip success">可操作</span></div>` }));
    }
    showToast(`已导入：${result.candidate.name}`);
    return;
  }
  if (button.dataset.action === "confirm-batch-import-upload") {
    const fileInput = document.querySelector('[data-batch-import-files]');
    const files = Array.from(fileInput?.files || []);
    if (!files.length) throw new Error("请先选择一个或多个简历文件");
    const allowed = [".doc", ".docx", ".pdf"];
    for (const file of files) {
      const name = (file.name || "").toLowerCase();
      if (!allowed.some(ext => name.endsWith(ext))) throw new Error("格式文件不符，请重新上传");
    }
    const result = await window.hrApi.importBatch(files);
    await window.hrApi.createNotification({
      user: "admin",
      title: `批量简历导入：${result.imported} 成功`,
      type: "导入通知",
      content: `批量导入完成，成功 ${result.imported}，重复 ${result.duplicates || 0}`,
      target_path: "./import.html",
      read: false,
    });
    const modal = document.querySelector('[data-batch-import-modal]');
    if (modal) modal.style.display = "none";
    const historyItems = await window.hrApi.importRecords();
    const records = document.querySelector(".import-records .timeline");
    if (records) {
      records.innerHTML = historyItems.slice(0, 5).map(i => `<div class="list-item soft"><div class="item-top"><div><div class="item-title">${i.file_name}</div><div class="item-meta">${i.imported_count} 成功 / ${i.failed_count} 失败 · ${i.note}</div></div><span class="tag ${i.status === '成功' ? 'green' : 'blue'}">${i.status}</span></div></div>`).join('');
    }
    const success = document.querySelector('[data-import-success]');
    const failed = document.querySelector('[data-import-failed]');
    const rate = document.querySelector('[data-import-rate]');
    const review = document.querySelector('[data-import-review]');
    if (success) success.textContent = String(historyItems.reduce((sum, i) => sum + Number(i.imported_count || 0), 0));
    if (failed) failed.textContent = String(historyItems.reduce((sum, i) => sum + Number(i.failed_count || 0), 0));
    if (rate) rate.textContent = historyItems.length ? `${((historyItems.reduce((sum, i) => sum + Number(i.imported_count || 0), 0) / Math.max(1, historyItems.reduce((sum, i) => sum + Number(i.imported_count || 0) + Number(i.failed_count || 0), 0))) * 100).toFixed(1)}%` : '0%';
    if (review) review.textContent = String(historyItems.filter(i => String(i.note || '').includes('复核')).length);
    showToast(`批量导入完成：${result.imported} 条`);
    return;
  }
  if (button.dataset.action === "create-company") {
    const modal = document.querySelector('[data-company-modal]');
    if (modal) modal.style.display = 'block';
    return;
  }
  if (button.dataset.action === "toggle-company") {
    const modal = document.querySelector('[data-company-action-modal]');
    const title = document.querySelector('[data-company-action-title]');
    const desc = document.querySelector('[data-company-action-desc]');
    const companies = await window.hrApi.companies();
    const company = companies.find(item => item.id === Number(button.dataset.id));
    if (modal) {
      modal.style.display = 'block';
      modal.dataset.target = JSON.stringify({ kind: 'toggle-company', id: Number(button.dataset.id) });
    }
    if (title) title.textContent = `客户 ${company?.name || button.dataset.id} 状态变更`;
    if (desc) desc.textContent = `确认后将切换客户 ${company?.name || button.dataset.id} 的状态。`;
    return;
  }
  if (button.dataset.action === "delete-company") {
    const modal = document.querySelector('[data-company-action-modal]');
    const title = document.querySelector('[data-company-action-title]');
    const desc = document.querySelector('[data-company-action-desc]');
    const companies = await window.hrApi.companies();
    const company = companies.find(item => item.id === Number(button.dataset.id));
    if (modal) {
      modal.style.display = 'block';
      modal.dataset.target = JSON.stringify({ kind: 'delete-company', id: Number(button.dataset.id) });
    }
    if (title) title.textContent = `删除客户 ${company?.name || button.dataset.id}`;
    if (desc) desc.textContent = `确认后将永久删除客户 ${company?.name || button.dataset.id} 记录。`;
    return;
  }
  if (button.dataset.action === "close-company-action-modal") {
    const modal = document.querySelector('[data-company-action-modal]');
    if (modal) modal.style.display = 'none';
    return;
  }
  if (button.dataset.action === "confirm-company-action") {
    const modal = document.querySelector('[data-company-action-modal]');
    const target = modal?.dataset.target ? JSON.parse(modal.dataset.target) : null;
    if (!target) throw new Error('没有待执行的客户操作');
    if (target.kind === 'toggle-company') {
      const company = await window.hrApi.toggleCompany(target.id);
      const list = document.querySelector(".content .panel .list");
      if (list) {
        const companies = await window.hrApi.companies();
        list.innerHTML = companies.slice(0, 3).map(c => `<div class="list-item"><div class="item-top"><div><div class="item-title">${c.name}</div><div class="item-meta">${c.contact_name || ''} · ${c.contact_phone || ''}${c.contact_email ? ` · ${c.contact_email}` : ''}${c.address ? ` · ${c.address}` : ''}${c.cooperation_period ? ` · ${c.cooperation_period}` : ''}</div></div><div class="table-actions"><button class="btn-sm" data-action="toggle-company" data-id="${c.id}">${c.status === '招聘完毕' ? '恢复' : '完结'}</button><button class="btn-sm" data-action="delete-company" data-id="${c.id}">删除</button></div><span class="chip ${c.status === '招聘完毕' ? 'neutral' : 'success'}">${c.status || '招聘中'}</span></div></div>`).join("");
      }
      await refreshCompanyMetrics();
      showToast(`客户状态已更新：${company.name}`);
    } else if (target.kind === 'delete-company') {
      await window.hrApi.deleteCompany(target.id);
      const list = document.querySelector(".content .panel .list");
      if (list) {
        const companies = await window.hrApi.companies();
        list.innerHTML = companies.slice(0, 3).map(c => `<div class="list-item"><div class="item-top"><div><div class="item-title">${c.name}</div><div class="item-meta">${c.contact_name || ''} · ${c.contact_phone || ''}${c.contact_email ? ` · ${c.contact_email}` : ''}${c.address ? ` · ${c.address}` : ''}${c.cooperation_period ? ` · ${c.cooperation_period}` : ''}</div></div><div class="table-actions"><button class="btn-sm" data-action="toggle-company" data-id="${c.id}">${c.status === '招聘完毕' ? '恢复' : '完结'}</button><button class="btn-sm" data-action="delete-company" data-id="${c.id}">删除</button></div><span class="chip ${c.status === '招聘完毕' ? 'neutral' : 'success'}">${c.status || '招聘中'}</span></div></div>`).join("");
      }
      await refreshCompanyMetrics();
      showToast("客户已删除");
    }
    if (modal) modal.style.display = 'none';
    return;
  }
  if (button.dataset.action === "create-project") {
    const modal = document.querySelector('[data-project-modal]');
    if (modal) modal.style.display = 'block';
    return;
  }
  if (button.dataset.action === "toggle-project") {
    const modal = document.querySelector('[data-project-action-modal]');
    const title = document.querySelector('[data-project-action-title]');
    const desc = document.querySelector('[data-project-action-desc]');
    const projects = await window.hrApi.projects();
    const project = projects.find(item => item.id === Number(button.dataset.id));
    if (modal) {
      modal.style.display = 'block';
      modal.dataset.target = JSON.stringify({ kind: 'toggle-project', id: Number(button.dataset.id) });
    }
    if (title) title.textContent = `项目 ${project?.name || button.dataset.id} 状态变更`;
    if (desc) desc.textContent = `确认后将切换项目 ${project?.name || button.dataset.id} 的状态。`;
    return;
  }
  if (button.dataset.action === "delete-project") {
    const modal = document.querySelector('[data-project-action-modal]');
    const title = document.querySelector('[data-project-action-title]');
    const desc = document.querySelector('[data-project-action-desc]');
    const projects = await window.hrApi.projects();
    const project = projects.find(item => item.id === Number(button.dataset.id));
    if (modal) {
      modal.style.display = 'block';
      modal.dataset.target = JSON.stringify({ kind: 'delete-project', id: Number(button.dataset.id) });
    }
    if (title) title.textContent = `删除项目 ${project?.name || button.dataset.id}`;
    if (desc) desc.textContent = `确认后将永久删除项目 ${project?.name || button.dataset.id} 记录。`;
    return;
  }
  if (button.dataset.action === "close-project-action-modal") {
    const modal = document.querySelector('[data-project-action-modal]');
    if (modal) modal.style.display = 'none';
    return;
  }
  if (button.dataset.action === "confirm-project-action") {
    const modal = document.querySelector('[data-project-action-modal]');
    const target = modal?.dataset.target ? JSON.parse(modal.dataset.target) : null;
    if (!target) throw new Error('没有待执行的项目操作');
    if (target.kind === 'toggle-project') {
      const project = await window.hrApi.toggleProject(target.id);
      const list = document.querySelector(".content .panel .list");
      if (list) {
        const projects = await window.hrApi.projects();
        list.innerHTML = projects.slice(0, 3).map(p => `<div class="list-item"><div class="item-top"><div><div class="item-title">${p.name}</div><div class="item-meta">${p.company_name || ''} · ${p.work_location || ""} · 招聘人数 ${p.hiring_count}</div></div><div class="table-actions"><button class="btn-sm" data-action="toggle-project" data-id="${p.id}">${p.status === '招聘完毕' ? '恢复' : '完结'}</button><button class="btn-sm" data-action="delete-project" data-id="${p.id}">删除</button></div><span class="chip ${p.status==='招聘完毕'?'neutral':'success'}">${p.status}</span></div></div>`).join("");
      }
      showToast(`项目状态已更新：${project.name}`);
    } else if (target.kind === 'delete-project') {
      await window.hrApi.deleteProject(target.id);
      const list = document.querySelector(".content .panel .list");
      if (list) {
        const projects = await window.hrApi.projects();
        list.innerHTML = projects.slice(0, 3).map(p => `<div class="list-item"><div class="item-top"><div><div class="item-title">${p.name}</div><div class="item-meta">${p.company_name || ''} · ${p.work_location || ""} · 招聘人数 ${p.hiring_count}</div></div><div class="table-actions"><button class="btn-sm" data-action="toggle-project" data-id="${p.id}">${p.status === '招聘完毕' ? '恢复' : '完结'}</button><button class="btn-sm" data-action="delete-project" data-id="${p.id}">删除</button></div><span class="chip ${p.status==='招聘完毕'?'neutral':'success'}">${p.status}</span></div></div>`).join("");
      }
      showToast("项目已删除");
    }
    if (modal) modal.style.display = 'none';
    return;
  }
  if (button.dataset.action === "create-evaluation") {
    const modal = document.querySelector('[data-evaluation-modal]');
    if (modal) modal.style.display = 'block';
    const [candidates, positions] = await Promise.all([window.hrApi.candidates(), window.hrApi.positions()]);
    const candidateSel = document.querySelector('[data-eval-candidate]');
    const positionSel = document.querySelector('[data-eval-position]');
    if (candidateSel) candidateSel.innerHTML = candidates.map(c => `<option value="${c.id}">${c.name} · ${c.current_title || ''}</option>`).join('');
    if (positionSel) positionSel.innerHTML = positions.map(p => `<option value="${p.id}">${p.name}</option>`).join('');
    return;
  }
  if (button.dataset.action === "open-evaluation-modal") {
    const modal = document.querySelector('[data-evaluation-modal]');
    if (modal) modal.style.display = 'block';
    const [candidates, positions] = await Promise.all([window.hrApi.candidates(), window.hrApi.positions()]);
    const candidateSel = document.querySelector('[data-eval-candidate]');
    const positionSel = document.querySelector('[data-eval-position]');
    if (candidateSel) candidateSel.innerHTML = candidates.map(c => `<option value="${c.id}">${c.name} · ${c.current_title || ''}</option>`).join('');
    if (positionSel) positionSel.innerHTML = positions.map(p => `<option value="${p.id}">${p.name}</option>`).join('');
    return;
  }
  if (button.dataset.action === "close-evaluation-modal") {
    const modal = document.querySelector('[data-evaluation-modal]');
    if (modal) modal.style.display = 'none';
    return;
  }
  if (button.dataset.action === "confirm-evaluation-upload") {
    const candidateId = Number(document.querySelector('[data-eval-candidate]')?.value || 0);
    const positionId = Number(document.querySelector('[data-eval-position]')?.value || 0);
    const roundName = document.querySelector('[data-eval-round]')?.value?.trim() || '第 1 轮';
    const grade = document.querySelector('[data-eval-grade]')?.value || '良好';
    const score = Number(document.querySelector('[data-eval-score]')?.value || 4);
    const content = document.querySelector('[data-eval-content]')?.value?.trim() || '';
    if (!candidateId || !positionId) throw new Error('请先选择候选人和岗位');
    const evaluation = await window.hrApi.createEvaluation({ candidate_id: candidateId, position_id: positionId, evaluator: 'admin', round_name: roundName, grade, score, content });
    const modal = document.querySelector('[data-evaluation-modal]');
    if (modal) modal.style.display = 'none';
    const list = document.querySelector('[data-evaluation-list]');
    if (list) {
      const items = await window.hrApi.evaluations();
      list.innerHTML = items.slice(0, 3).map(i => `<div class="list-item"><div class="item-top"><div><div class="item-title">${i.evaluator} · ${i.round_name}</div><div class="item-meta">岗位 ID ${i.position_id}</div><div class="item-meta">${i.content}</div></div><span class="chip success">${i.grade} · ${i.score} 分</span></div></div>`).join('');
    }
    await window.hrApi.createNotification({
      user: 'admin',
      title: `评价已记录：${evaluation.round_name}`,
      type: '评价通知',
      content: `候选人 ID ${evaluation.candidate_id} 已新增评价，岗位 ID ${evaluation.position_id}，结果 ${evaluation.grade}`,
      target_path: './evaluations.html',
      read: false,
    });
    showToast(`已保存评价：${evaluation.grade}`);
    return;
  }
  if (button.dataset.action === "create-tag") {
    const modal = document.querySelector('[data-tag-modal]');
    if (modal) modal.style.display = 'block';
    return;
  }
  if (button.dataset.action === "refresh-tags") {
    const list = document.querySelector(".content .panel .list");
    if (list) {
      const tags = await window.hrApi.tags();
      list.innerHTML = tags.slice(0, 5).map(t => `<div class="list-item"><div class="item-top"><div><div class="item-title">${t.category}</div><div class="item-meta">${t.name}</div></div><span class="chip ${t.enabled ? 'success' : 'neutral'}">${t.enabled ? '启用' : '禁用'}</span></div></div>`).join("");
    }
    showToast("标签词库已刷新");
    return;
  }
  if (button.dataset.action === "toggle-tag") {
    const modal = document.querySelector('[data-tag-action-modal]');
    const title = document.querySelector('[data-tag-action-title]');
    const desc = document.querySelector('[data-tag-action-desc]');
    const tags = await window.hrApi.tags();
    const tag = tags.find(item => item.id === Number(button.dataset.id));
    if (modal) {
      modal.style.display = 'block';
      modal.dataset.target = JSON.stringify({ kind: 'toggle-tag', id: Number(button.dataset.id), enabled: button.dataset.enabled === 'true' });
    }
    if (title) title.textContent = `标签 ${tag?.name || button.dataset.id} 状态变更`;
    if (desc) desc.textContent = `确认后将切换标签 ${tag?.name || button.dataset.id} 的启用状态。`;
    return;
  }
  if (button.dataset.action === "delete-tag") {
    const modal = document.querySelector('[data-tag-action-modal]');
    const title = document.querySelector('[data-tag-action-title]');
    const desc = document.querySelector('[data-tag-action-desc]');
    const tags = await window.hrApi.tags();
    const tag = tags.find(item => item.id === Number(button.dataset.id));
    if (modal) {
      modal.style.display = 'block';
      modal.dataset.target = JSON.stringify({ kind: 'delete-tag', id: Number(button.dataset.id) });
    }
    if (title) title.textContent = `删除标签 ${tag?.name || button.dataset.id}`;
    if (desc) desc.textContent = `确认后将永久删除标签 ${tag?.name || button.dataset.id}。`;
    return;
  }
  if (button.dataset.action === "close-tag-action-modal") {
    const modal = document.querySelector('[data-tag-action-modal]');
    if (modal) modal.style.display = 'none';
    return;
  }
  if (button.dataset.action === "confirm-tag-action") {
    const modal = document.querySelector('[data-tag-action-modal]');
    const target = modal?.dataset.target ? JSON.parse(modal.dataset.target) : null;
    if (!target) throw new Error('没有待执行的标签操作');
    if (target.kind === 'toggle-tag') {
      const tag = await window.hrApi.updateTag(target.id, { enabled: !target.enabled });
      const list = document.querySelector(".content .panel .list");
      if (list) {
        const tags = await window.hrApi.tags();
        list.innerHTML = tags.slice(0, 5).map(t => `<div class="list-item"><div class="item-top"><div><div class="item-title">${t.category}</div><div class="item-meta">${t.name}</div></div><span class="chip ${t.enabled ? 'success' : 'neutral'}">${t.enabled ? '启用' : '禁用'}</span></div></div>`).join("");
      }
      showToast(`已更新标签：${tag.name}`);
    } else if (target.kind === 'delete-tag') {
      await window.hrApi.request(`/tags/${target.id}`, { method: "DELETE" });
      const list = document.querySelector(".content .panel .list");
      if (list) {
        const tags = await window.hrApi.tags();
        list.innerHTML = tags.slice(0, 5).map(t => `<div class="list-item"><div class="item-top"><div><div class="item-title">${t.category}</div><div class="item-meta">${t.name}</div></div><span class="chip ${t.enabled ? 'success' : 'neutral'}">${t.enabled ? '启用' : '禁用'}</span></div></div>`).join("");
      }
      showToast("已删除标签");
    }
    if (modal) modal.style.display = 'none';
    return;
  }
  if (button.dataset.action === "create-candidate") {
    const modal = document.querySelector('[data-candidate-create-modal]');
    if (modal) modal.style.display = 'block';
    return;
  }
  if (button.dataset.action === "lock-candidate") {
    const candidateId = Number(button.dataset.id || 0);
    const candidate = await window.hrApi.candidates().then(list => list.find(i => i.id === candidateId));
    if (!candidate) throw new Error('未找到候选人');
    const actionModal = document.querySelector('[data-candidate-action-modal]');
    const actionTitle = document.querySelector('[data-candidate-action-title]');
    const actionDesc = document.querySelector('[data-candidate-action-desc]');
    if (actionModal) {
      actionModal.style.display = 'block';
      actionModal.dataset.target = JSON.stringify({ id: candidateId, action: 'lock-candidate' });
    }
    if (actionTitle) actionTitle.textContent = `锁定候选人 ${candidate.name}`;
    if (actionDesc) actionDesc.textContent = '确认后将锁定该候选人，避免重复编辑。';
    return;
  }
  if (button.dataset.action === "release-candidate") {
    const candidateId = Number(button.dataset.id || 0);
    const candidate = await window.hrApi.candidates().then(list => list.find(i => i.id === candidateId));
    if (!candidate) throw new Error('未找到候选人');
    const actionModal = document.querySelector('[data-candidate-action-modal]');
    const actionTitle = document.querySelector('[data-candidate-action-title]');
    const actionDesc = document.querySelector('[data-candidate-action-desc]');
    if (actionModal) {
      actionModal.style.display = 'block';
      actionModal.dataset.target = JSON.stringify({ id: candidateId, action: 'release-candidate' });
    }
    if (actionTitle) actionTitle.textContent = `释放候选人 ${candidate.name}`;
    if (actionDesc) actionDesc.textContent = '确认后将解除锁定，允许继续流转。';
    return;
  }
  if (button.dataset.action === "create-warranty") {
    const modal = document.querySelector('[data-warranty-modal]');
    const scopeInput = document.querySelector('[data-warranty-scope]');
    const monthsInput = document.querySelector('[data-warranty-months]');
    const remindInput = document.querySelector('[data-warranty-remind]');
    const autoInput = document.querySelector('[data-warranty-auto]');
    const titleEl = document.querySelector('[data-warranty-modal-title]');
    const scope = button.dataset.scope || '';
    if (scopeInput && scope) scopeInput.value = scope;
    if (titleEl && scope) titleEl.textContent = `${scope} 质保规则`;
    // 查询已有同 scope 的质保规则并回填
    const rules = await window.hrApi.warrantyRules();
    const existing = rules.find(r => r.scope === scope);
    if (monthsInput) monthsInput.value = existing?.months || '';
    if (remindInput) remindInput.value = existing?.remind_days || '';
    if (autoInput) autoInput.value = existing?.auto_expire ? 'true' : 'false';
    if (modal) {
      modal.style.display = 'block';
      modal.dataset.ruleId = existing?.id ? String(existing.id) : '';
    }
    return;
  }
  if (button.dataset.action === "edit-warranty-rule") {
    const preview = document.querySelector('[data-warranty-preview]');
    const scope = String(button.dataset.scope || '');
    const months = String(button.dataset.months || '');
    const remindDays = String(button.dataset.remindDays || '');
    const autoExpire = button.dataset.autoExpire === 'true';
    if (preview) {
      preview.innerHTML = `<div class="list-item"><div class="item-top"><div><div class="item-title">${scope}</div><div class="item-meta">${months} 个月 · 提前 ${remindDays} 天提醒</div></div><span class="chip ${autoExpire ? 'success' : 'neutral'}">${autoExpire ? '自动失效' : '手动失效'}</span></div></div>`;
    }
    return;
  }
  if (button.dataset.action === "open-warranty-modal") {
    const modal = document.querySelector('[data-warranty-modal]');
    if (modal) {
      modal.style.display = 'block';
      modal.dataset.ruleId = '';
    }
    return;
  }
  if (button.dataset.action === "close-warranty-modal") {
    const modal = document.querySelector('[data-warranty-modal]');
    if (modal) modal.style.display = 'none';
    return;
  }
  if (button.dataset.action === "confirm-warranty-upload") {
    const modal = document.querySelector('[data-warranty-modal]');
    const ruleId = modal?.dataset.ruleId || '';
    const scope = document.querySelector('[data-warranty-scope]')?.value?.trim() || '';
    const months = Number(document.querySelector('[data-warranty-months]')?.value || 0);
    const remindDays = Number(document.querySelector('[data-warranty-remind]')?.value || 0);
    const autoExpire = document.querySelector('[data-warranty-auto]')?.value === 'true';
    if (!scope || !months || !remindDays) throw new Error('请先填写质保范围、月数和提醒天数');
    // Upsert：有 ruleId 则更新，无则新建
    let rule;
    if (ruleId) {
      rule = await window.hrApi.updateWarrantyRule(ruleId, { scope, months, remind_days: remindDays, auto_expire: autoExpire });
    } else {
      // 再次查询防止并发新建（用户手动改了 scope）
      const rules = await window.hrApi.warrantyRules();
      const sameScope = rules.find(r => r.scope === scope);
      if (sameScope) {
        rule = await window.hrApi.updateWarrantyRule(sameScope.id, { scope, months, remind_days: remindDays, auto_expire: autoExpire });
      } else {
        rule = await window.hrApi.createWarrantyRule({ scope, months, remind_days: remindDays, auto_expire: autoExpire });
      }
    }
    if (modal) modal.style.display = 'none';
    showToast(`已保存质保规则：${rule.scope}`);
    setTimeout(() => window.location.reload(), 250);
    return;
  }
  if (button.dataset.action === "open-system-config-modal") {
    const modal = document.querySelector('[data-system-config-modal]');
    if (modal) modal.style.display = 'block';
    const [configs, email] = await Promise.all([window.hrApi.systemConfigs(), window.hrApi.emailConfig()]);
    const nameInput = document.querySelector('[data-system-name-input]');
    const watermarkInput = document.querySelector('[data-system-watermark-input]');
    const logsInput = document.querySelector('[data-system-logs-input]');
    const emailList = document.querySelector('[data-email-config-list-modal]');
    if (nameInput) nameInput.value = configs.find(c => c.key === 'site_name')?.value || '';
    if (watermarkInput) watermarkInput.value = configs.find(c => c.key === 'watermark')?.value || '';
    if (logsInput) logsInput.value = configs.find(c => c.key === 'log_retention_days')?.value || '';
    if (emailList && email) {
      emailList.innerHTML = `<div class="list-item"><div class="item-top"><div><div class="item-title">${email.host}</div><div class="item-meta">${email.sender} · ${email.port}</div></div><span class="chip success">${email.enabled ? '启用' : '停用'}</span></div></div><div class="list-item"><div class="item-top"><div><div class="item-title">TLS</div><div class="item-meta">${email.use_tls ? '启用' : '关闭'}</div></div><span class="chip ${email.use_tls ? 'success' : 'neutral'}">真实配置</span></div></div>`;
    }
    return;
  }
  if (button.dataset.action === "open-email-config-modal") {
    const modal = document.querySelector('[data-email-config-modal]');
    if (modal) modal.style.display = 'block';
    const email = await window.hrApi.emailConfig();
    const hostInput = document.querySelector('[data-email-host-input]');
    const portInput = document.querySelector('[data-email-port-input]');
    const senderInput = document.querySelector('[data-email-sender-input]');
    const usernameInput = document.querySelector('[data-email-username-input]');
    const passwordInput = document.querySelector('[data-email-password-input]');
    const tlsInput = document.querySelector('[data-email-tls-input]');
    const enabledInput = document.querySelector('[data-email-enabled-input]');
    if (hostInput) hostInput.value = email?.host || '';
    if (portInput) portInput.value = String(email?.port || 25);
    if (senderInput) senderInput.value = email?.sender || '';
    if (usernameInput) usernameInput.value = email?.username || '';
    if (passwordInput) passwordInput.value = email?.password || '';
    if (tlsInput) tlsInput.value = email?.use_tls ? 'true' : 'false';
    if (enabledInput) enabledInput.value = email?.enabled ? 'true' : 'false';
    return;
  }
  if (button.dataset.action === "close-email-config-modal") {
    const modal = document.querySelector('[data-email-config-modal]');
    if (modal) modal.style.display = 'none';
    return;
  }
  if (button.dataset.action === "confirm-email-config-upload") {
    const host = document.querySelector('[data-email-host-input]')?.value?.trim() || '';
    const port = Number(document.querySelector('[data-email-port-input]')?.value || 0);
    const sender = document.querySelector('[data-email-sender-input]')?.value?.trim() || '';
    const username = document.querySelector('[data-email-username-input]')?.value?.trim() || '';
    const password = document.querySelector('[data-email-password-input]')?.value || '';
    const useTls = document.querySelector('[data-email-tls-input]')?.value === 'true';
    const enabled = document.querySelector('[data-email-enabled-input]')?.value === 'true';
    if (!host || !port || !sender || !username || !password) throw new Error('请先填写完整的邮件配置');
    const email = await window.hrApi.saveEmailConfig({ host, port, sender, username, password, use_tls: useTls, enabled });
    const modal = document.querySelector('[data-email-config-modal]');
    if (modal) modal.style.display = 'none';
    const list = document.querySelector('[data-email-config-list]');
    if (list) {
      list.innerHTML = `<div class="list-item"><div class="item-top"><div><div class="item-title">${email.host}</div><div class="item-meta">${email.sender} · ${email.port}</div></div><span class="chip success">${email.enabled ? '启用' : '停用'}</span></div></div><div class="list-item"><div class="item-top"><div><div class="item-title">TLS</div><div class="item-meta">${email.use_tls ? '启用' : '关闭'}</div></div><span class="chip ${email.use_tls ? 'success' : 'neutral'}">真实配置</span></div></div>`;
    }
    showToast('邮件配置已保存');
    return;
  }
  if (button.dataset.action === "test-email-config") {
    const payload = {
      host: document.querySelector('[data-email-host-input]')?.value?.trim() || '',
      port: Number(document.querySelector('[data-email-port-input]')?.value || 0),
      sender: document.querySelector('[data-email-sender-input]')?.value?.trim() || '',
      username: document.querySelector('[data-email-username-input]')?.value?.trim() || '',
      password: document.querySelector('[data-email-password-input]')?.value || '',
      use_tls: document.querySelector('[data-email-tls-input]')?.value === 'true',
      enabled: document.querySelector('[data-email-enabled-input]')?.value === 'true',
    };
    if (!payload.host || !payload.port || !payload.sender || !payload.username || !payload.password) throw new Error('请先填写完整的邮件配置再测试连接');
    const result = await window.hrApi.testEmailConfig(payload);
    const host = document.querySelector('[data-email-test-result]');
    if (host) {
      host.innerHTML = `<div class="list-item"><div class="item-top"><div><div class="item-title">${result.ok ? '连接成功' : '连接失败'}</div><div class="item-meta">${result.message}</div></div><span class="chip ${result.ok ? 'success' : 'neutral'}">${result.ok ? '通过' : '失败'}</span></div></div>`;
    }
    showToast(result.message);
    return;
  }
  if (button.dataset.action === "close-system-config-modal") {
    const modal = document.querySelector('[data-system-config-modal]');
    if (modal) modal.style.display = 'none';
    return;
  }
  if (button.dataset.action === "confirm-system-config-upload") {
    const siteName = document.querySelector('[data-system-name-input]')?.value?.trim() || '';
    const watermark = document.querySelector('[data-system-watermark-input]')?.value?.trim() || '';
    const logs = Number(document.querySelector('[data-system-logs-input]')?.value || 0);
    if (!siteName || !watermark || !logs) throw new Error('请先填写系统名称、水印内容和日志保留天数');
    await window.hrApi.saveSystemConfig({ key: 'site_name', value: siteName, description: '系统名称' });
    await window.hrApi.saveSystemConfig({ key: 'watermark', value: watermark, description: '水印内容' });
    await window.hrApi.saveSystemConfig({ key: 'log_retention_days', value: String(logs), description: '日志保留天数' });
    const modal = document.querySelector('[data-system-config-modal]');
    if (modal) modal.style.display = 'none';
    const panel = document.querySelector('.content .panel:first-of-type .list');
    if (panel) {
      const configs = await window.hrApi.systemConfigs();
      panel.innerHTML = configs.map(c => `<div class="list-item"><div class="item-top"><div><div class="item-title">${c.key}</div><div class="item-meta">${c.value}</div></div><span class="chip primary">配置</span></div></div>`).join('');
    }
    showToast('系统配置已保存');
    return;
  }
  if (button.dataset.action === "save-system-config") {
    const modal = document.querySelector('[data-system-config-modal]');
    if (modal) modal.style.display = 'block';
    return;
  }
  if (button.dataset.action === "save-email-config") {
    const modal = document.querySelector('[data-email-config-modal]');
    if (modal) modal.style.display = 'block';
    const email = await window.hrApi.emailConfig();
    const hostInput = document.querySelector('[data-email-host-input]');
    const portInput = document.querySelector('[data-email-port-input]');
    const senderInput = document.querySelector('[data-email-sender-input]');
    const usernameInput = document.querySelector('[data-email-username-input]');
    const passwordInput = document.querySelector('[data-email-password-input]');
    const tlsInput = document.querySelector('[data-email-tls-input]');
    const enabledInput = document.querySelector('[data-email-enabled-input]');
    if (hostInput) hostInput.value = email?.host || '';
    if (portInput) portInput.value = String(email?.port || 25);
    if (senderInput) senderInput.value = email?.sender || '';
    if (usernameInput) usernameInput.value = email?.username || '';
    if (passwordInput) passwordInput.value = email?.password || '';
    if (tlsInput) tlsInput.value = email?.use_tls ? 'true' : 'false';
    if (enabledInput) enabledInput.value = email?.enabled ? 'true' : 'false';
    return;
  }
  if (button.dataset.action === "ai-resume-parse") {
    const res = await window.hrApi.createAiTask({ task_type: "resume_parse", input_text: `自动简历-${uniq}` });
    await window.hrApi.createNotification({
      user: "admin",
      title: `AI 简历解析完成`,
      type: "AI通知",
      content: `任务 resume_parse 已完成，结果：${res.output_text}`,
      target_path: "./ai-center.html",
      read: false,
    });
    showToast(`AI 解析完成：${res.output_text}`);
    return;
  }
  if (button.dataset.action === "ai-jd-generate") {
    const res = await window.hrApi.createAiTask({ task_type: "jd_generate", input_text: `自动岗位-${uniq}` });
    await window.hrApi.createNotification({
      user: "admin",
      title: `AI JD 生成完成`,
      type: "AI通知",
      content: `任务 jd_generate 已完成，结果：${res.output_text}`,
      target_path: "./ai-center.html",
      read: false,
    });
    showToast(`AI 生成完成：${res.output_text}`);
    return;
  }
  if (button.dataset.action === "save-permissions") {
    const roleModal = document.querySelector('[data-role-permission-modal]');
    if (roleModal) roleModal.style.display = 'block';
    return;
  }
  if (button.dataset.action === "open-role-permission-modal") {
    const modal = document.querySelector('[data-role-permission-modal]');
    if (modal) modal.style.display = 'block';
    return;
  }
  if (button.dataset.action === "close-role-permission-modal") {
    const modal = document.querySelector('[data-role-permission-modal]');
    if (modal) modal.style.display = 'none';
    return;
  }
  if (button.dataset.action === "confirm-role-permission-upload") {
    const roleCode = document.querySelector('[data-role-permission-role]')?.value?.trim() || '';
    const permissionKey = document.querySelector('[data-role-permission-key]')?.value?.trim() || '';
    const permissionType = document.querySelector('[data-role-permission-type]')?.value || 'menu';
    const moduleName = document.querySelector('[data-role-permission-module]')?.value?.trim() || '';
    const enabled = document.querySelector('[data-role-permission-enabled]')?.value === 'true';
    if (!roleCode || !permissionKey || !moduleName) throw new Error('请先填写角色、权限标识和模块名称');
    await window.hrApi.saveRolePermission({ role_code: roleCode, permission_key: permissionKey, permission_type: permissionType, module: moduleName, enabled });
    const modal = document.querySelector('[data-role-permission-modal]');
    if (modal) modal.style.display = 'none';
    const [perms, data] = await Promise.all([window.hrApi.rolePermissions(), window.hrApi.dataPermissions()]);
    const total = document.querySelector('[data-permission-total]');
    const dataTotal = document.querySelector('[data-permission-data]');
    const roleList = document.querySelector('[data-role-permission-list]');
    const dataList = document.querySelector('[data-data-permission-list]');
    if (total) total.textContent = String(perms.length);
    if (dataTotal) dataTotal.textContent = String(data.length);
    if (roleList) roleList.innerHTML = perms.slice(0, 8).map(item => `<div class="list-item"><div class="item-top"><div><div class="item-title">${item.module || item.permission_key}</div><div class="item-meta">${item.role_code} · ${item.permission_type} · ${item.enabled ? '已启用' : '已停用'}</div></div><span class="chip ${item.enabled ? 'primary' : 'neutral'}">${item.permission_type}</span></div></div>`).join('');
    showToast("权限已保存到数据库");
    return;
  }
  if (button.dataset.action === "save-data-permissions") {
    const modal = document.querySelector('[data-data-permission-modal]');
    if (modal) modal.style.display = 'block';
    return;
  }
  if (button.dataset.action === "close-data-permission-modal") {
    const modal = document.querySelector('[data-data-permission-modal]');
    if (modal) modal.style.display = 'none';
    return;
  }
  if (button.dataset.action === "open-data-permission-modal") {
    const modal = document.querySelector('[data-data-permission-modal]');
    if (modal) modal.style.display = 'block';
    return;
  }
  if (button.dataset.action === "confirm-data-permission-upload") {
    const userId = Number(document.querySelector('[data-data-permission-user]')?.value || 0);
    const scopeType = document.querySelector('[data-data-permission-scope]')?.value || 'company';
    const scopeId = document.querySelector('[data-data-permission-scope-id]')?.value?.trim() || '';
    const scopeName = document.querySelector('[data-data-permission-scope-name]')?.value?.trim() || '';
    const grantedBy = document.querySelector('[data-data-permission-granted-by]')?.value?.trim() || 'admin';
    if (!userId || !scopeId || !scopeName) throw new Error('请先填写用户、范围 ID 和范围名称');
    await window.hrApi.saveDataPermission({ user_id: userId, scope_type: scopeType, scope_id: scopeId, scope_name: scopeName, granted_by: grantedBy, active: true });
    const modal = document.querySelector('[data-data-permission-modal]');
    if (modal) modal.style.display = 'none';
    const [perms, data] = await Promise.all([window.hrApi.rolePermissions(), window.hrApi.dataPermissions()]);
    const total = document.querySelector('[data-permission-total]');
    const dataTotal = document.querySelector('[data-permission-data]');
    const roleList = document.querySelector('[data-role-permission-list]');
    const dataList = document.querySelector('[data-data-permission-list]');
    if (total) total.textContent = String(perms.length);
    if (dataTotal) dataTotal.textContent = String(data.length);
    if (dataList) dataList.innerHTML = data.slice(0, 8).map(item => `<div class="list-item"><div class="item-top"><div><div class="item-title">${item.scope_name || item.scope_type}</div><div class="item-meta">${item.scope_type} · ${item.granted_by} · ${item.active ? '已启用' : '已停用'}</div></div><span class="chip ${item.active ? 'success' : 'neutral'}">${item.scope_type}</span></div></div>`).join('');
    showToast("数据权限已保存到数据库");
    return;
  }
  if (button.dataset.action === "toggle-role-permission") {
    await window.hrApi.saveRolePermission({
      role_code: button.dataset.roleCode || '',
      permission_key: button.dataset.key || '',
      permission_type: 'action',
      module: button.dataset.key || '',
      enabled: button.dataset.enabled !== 'true',
    });
    const perms = await window.hrApi.rolePermissions();
    const roleList = document.querySelector('[data-role-permission-list]');
    if (roleList) roleList.innerHTML = perms.slice(0, 8).map(item => `<div class="list-item"><div class="item-top"><div><div class="item-title">${item.module || item.permission_key}</div><div class="item-meta">${item.role_code} · ${item.permission_type} · ${item.enabled ? '已启用' : '已停用'}</div></div><div class="table-actions"><button class="btn-sm" data-action="toggle-role-permission" data-role-code="${item.role_code}" data-key="${item.permission_key}" data-enabled="${item.enabled}">${item.enabled ? '停用' : '启用'}</button></div><span class="chip ${item.enabled ? 'primary' : 'neutral'}">${item.permission_type}</span></div></div>`).join('');
    showToast("功能权限已更新");
    return;
  }
  if (button.dataset.action === "toggle-data-permission") {
    await window.hrApi.saveDataPermission({
      user_id: Number(button.dataset.userId || 0),
      scope_type: button.dataset.scopeType || 'company',
      scope_id: button.dataset.scopeId || '',
      scope_name: button.dataset.scopeName || '',
      granted_by: button.dataset.grantedBy || 'admin',
      active: button.dataset.active !== 'true',
    });
    const list = await window.hrApi.dataPermissions();
    const dataList = document.querySelector('[data-data-permission-list]') || document.querySelector('[data-permission-data]')?.closest('.panel')?.querySelector('.list');
    if (dataList) dataList.innerHTML = list.slice(0, 8).map(item => `<div class="list-item"><div class="item-top"><div><div class="item-title">${item.scope_name || item.scope_type}</div><div class="item-meta">${item.scope_type} · ${item.granted_by} · ${item.active ? '已启用' : '已停用'}</div></div><div class="table-actions"><button class="btn-sm" data-action="toggle-data-permission" data-user-id="${item.user_id}" data-scope-type="${item.scope_type}" data-scope-id="${item.scope_id}" data-scope-name="${item.scope_name}" data-granted-by="${item.granted_by}" data-active="${item.active}">${item.active ? '停用' : '启用'}</button></div><span class="chip ${item.active ? 'success' : 'neutral'}">${item.active ? '启用' : '停用'}</span></div></div>`).join('');
    showToast("数据权限已更新");
    return;
  }
  if (button.dataset.action === "nav-logs") return location.href = "./logs.html";
  if (button.dataset.action === "nav-notifications") return location.href = "./notifications.html";
  if (button.dataset.action === "open-user-modal") {
    const modal = document.querySelector('[data-user-modal]');
    if (modal) modal.style.display = 'block';
    return;
  }
  if (button.dataset.action === "close-user-modal") {
    const modal = document.querySelector('[data-user-modal]');
    if (modal) modal.style.display = 'none';
    return;
  }
  if (button.dataset.action === "confirm-user-upload") {
    const username = document.querySelector('[data-user-username]')?.value?.trim() || '';
    const fullName = document.querySelector('[data-user-fullname]')?.value?.trim() || '';
    const role = document.querySelector('[data-user-role]')?.value?.trim() || '操作员';
    const password = document.querySelector('[data-user-password]')?.value || 'dev';
    if (!username || !fullName) throw new Error('请先填写用户名和姓名');
    const user = await window.hrApi.createUser({ username, full_name: fullName, role, password_hash: password });
    const modal = document.querySelector('[data-user-modal]');
    if (modal) modal.style.display = 'none';
    const list = document.querySelector('[data-user-list]');
    if (list) {
      const items = await window.hrApi.users();
      list.innerHTML = items.map(u => `<div class="list-item"><div class="item-top"><div><div class="item-title">${u.username}</div><div class="item-meta">${u.full_name} · ${u.role}</div></div><div class="table-actions"><button class="btn-sm" data-action="toggle-user" data-id="${u.id}">${u.is_active ? '停用' : '启用'}</button></div><span class="chip ${u.is_active ? 'success' : 'neutral'}">${u.is_active ? '启用' : '停用'}</span></div></div>`).join('');
    }
    await refreshUserStats();
    await window.hrApi.createNotification({
      user: "admin",
      title: `用户已创建：${user.username}`,
      type: "系统通知",
      content: `用户 ${user.full_name} 已保存到用户管理`,
      target_path: "./users.html",
      read: false,
    });
    showToast(`已创建用户：${user.username}`);
    return;
  }
  if (button.dataset.action === "edit-user") {
    const modal = document.querySelector('[data-user-edit-modal]');
    const users = await window.hrApi.users();
    const user = users.find(item => item.id === Number(button.dataset.id));
    if (!user) throw new Error('用户不存在');
    const username = document.querySelector('[data-user-edit-username]');
    const fullName = document.querySelector('[data-user-edit-fullname]');
    const role = document.querySelector('[data-user-edit-role]');
    const active = document.querySelector('[data-user-edit-active]');
    if (username) username.value = user.username;
    if (fullName) fullName.value = user.full_name || '';
    if (role) role.value = user.role || '';
    if (active) active.value = user.is_active ? '启用' : '停用';
    if (modal) {
      modal.style.display = 'block';
      modal.dataset.target = JSON.stringify({ id: user.id });
    }
    return;
  }
  if (button.dataset.action === "close-user-edit-modal") {
    const modal = document.querySelector('[data-user-edit-modal]');
    if (modal) modal.style.display = 'none';
    return;
  }
  if (button.dataset.action === "confirm-user-edit") {
    const modal = document.querySelector('[data-user-edit-modal]');
    const target = modal?.dataset.target ? JSON.parse(modal.dataset.target) : null;
    if (!target) throw new Error('没有待编辑的用户');
    const fullName = document.querySelector('[data-user-edit-fullname]')?.value?.trim() || '';
    const role = document.querySelector('[data-user-edit-role]')?.value?.trim() || '';
    const isActiveText = document.querySelector('[data-user-edit-active]')?.value?.trim() || '';
    if (!fullName || !role) throw new Error('请先填写姓名和角色');
    const user = await window.hrApi.updateUser(target.id, {
      full_name: fullName,
      role,
      is_active: isActiveText !== '停用',
    });
    const list = document.querySelector('[data-user-list]');
    if (list) {
      const items = await window.hrApi.users();
      list.innerHTML = items.map(u => `<div class="list-item"><div class="item-top"><div><div class="item-title">${u.username}</div><div class="item-meta">${u.full_name} · ${u.role}</div></div><div class="table-actions"><button class="btn-sm" data-action="edit-user" data-id="${u.id}">编辑</button><button class="btn-sm" data-action="toggle-user" data-id="${u.id}">${u.is_active ? '停用' : '启用'}</button><button class="btn-sm" data-action="reset-user-password" data-id="${u.id}">重置密码</button></div><span class="chip ${u.is_active ? 'success' : 'neutral'}">${u.is_active ? '启用' : '停用'}</span></div></div>`).join('');
    }
    await refreshUserStats();
    if (modal) modal.style.display = 'none';
    showToast(`用户已保存：${user.username}`);
    return;
  }
  if (button.dataset.action === "toggle-user") {
    const modal = document.querySelector('[data-user-action-modal]');
    const title = document.querySelector('[data-user-action-title]');
    const desc = document.querySelector('[data-user-action-desc]');
    const users = await window.hrApi.users();
    const user = users.find(item => item.id === Number(button.dataset.id));
    if (modal) {
      modal.style.display = 'block';
      modal.dataset.target = JSON.stringify({ id: Number(button.dataset.id), action: 'toggle-user' });
    }
    if (title) title.textContent = `用户 ${user?.username || button.dataset.id} 状态确认`;
    if (desc) desc.textContent = `确认后才会切换用户 ${user?.username || button.dataset.id} 的状态。`;
    return;
  }
  if (button.dataset.action === "reset-user-password") {
    const modal = document.querySelector('[data-user-action-modal]');
    const title = document.querySelector('[data-user-action-title]');
    const desc = document.querySelector('[data-user-action-desc]');
    const users = await window.hrApi.users();
    const user = users.find(item => item.id === Number(button.dataset.id));
    if (modal) {
      modal.style.display = 'block';
      modal.dataset.target = JSON.stringify({ id: Number(button.dataset.id), action: 'reset-user-password' });
    }
    if (title) title.textContent = `重置用户 ${user?.username || button.dataset.id} 密码`;
    if (desc) desc.textContent = `确认后将把用户 ${user?.username || button.dataset.id} 的密码重置为新的默认值。`;
    return;
  }
  if (button.dataset.action === "close-user-action-modal") {
    const modal = document.querySelector('[data-user-action-modal]');
    if (modal) modal.style.display = 'none';
    return;
  }
  if (button.dataset.action === "confirm-user-action") {
    const modal = document.querySelector('[data-user-action-modal]');
    const target = modal?.dataset.target ? JSON.parse(modal.dataset.target) : null;
    if (!target) throw new Error('没有待执行的用户操作');
    let user;
    if (target.action === 'reset-user-password') {
      user = await window.hrApi.resetUserPassword(target.id, { password_hash: 'dev-2026' });
    } else {
      user = await window.hrApi.toggleUser(target.id);
    }
    const list = document.querySelector('[data-user-list]');
    if (list) {
      const items = await window.hrApi.users();
      list.innerHTML = items.map(u => `<div class="list-item"><div class="item-top"><div><div class="item-title">${u.username}</div><div class="item-meta">${u.full_name} · ${u.role}</div></div><div class="table-actions"><button class="btn-sm" data-action="edit-user" data-id="${u.id}">编辑</button><button class="btn-sm" data-action="toggle-user" data-id="${u.id}">${u.is_active ? '停用' : '启用'}</button><button class="btn-sm" data-action="reset-user-password" data-id="${u.id}">重置密码</button></div><span class="chip ${u.is_active ? 'success' : 'neutral'}">${u.is_active ? '启用' : '停用'}</span></div></div>`).join('');
    }
    await refreshUserStats();
    if (modal) modal.style.display = 'none';
    showToast(target.action === 'reset-user-password' ? `密码已重置：${user.username}` : `用户状态已切换：${user.username}`);
    return;
  }
  if (button.dataset.action === "open-role-modal") {
    const modal = document.querySelector('[data-role-modal]');
    if (modal) modal.style.display = 'block';
    return;
  }
  if (button.dataset.action === "close-role-modal") {
    const modal = document.querySelector('[data-role-modal]');
    if (modal) modal.style.display = 'none';
    return;
  }
  if (button.dataset.action === "confirm-role-upload") {
    const code = document.querySelector('[data-role-code]')?.value?.trim() || '';
    const name = document.querySelector('[data-role-name]')?.value?.trim() || '';
    const description = document.querySelector('[data-role-desc]')?.value?.trim() || '';
    if (!code || !name) throw new Error('请先填写角色编码和名称');
    const role = await window.hrApi.createRole({ code, name, description });
    const modal = document.querySelector('[data-role-modal]');
    if (modal) modal.style.display = 'none';
    const list = document.querySelector('[data-role-list]');
    if (list) {
      const items = await window.hrApi.roles();
      list.innerHTML = items.map(r => `<div class="list-item"><div class="item-top"><div><div class="item-title">${r.name}</div><div class="item-meta">${r.code} · ${r.description}</div></div><div class="table-actions"><button class="btn-sm" data-action="toggle-role" data-id="${r.id}">操作</button></div><span class="chip primary">角色</span></div></div>`).join('');
    }
    await refreshRoleList();
    await window.hrApi.createNotification({
      user: "admin",
      title: `角色已创建：${role.code}`,
      type: "系统通知",
      content: `角色 ${role.name} 已保存到角色管理`,
      target_path: "./roles.html",
      read: false,
    });
    showToast(`已创建角色：${role.code}`);
    return;
  }
  if (button.dataset.action === "toggle-role") {
    const modal = document.querySelector('[data-role-action-modal]');
    const title = document.querySelector('[data-role-action-title]');
    const desc = document.querySelector('[data-role-action-desc]');
    const roles = await window.hrApi.roles();
    const role = roles.find(item => item.id === Number(button.dataset.id));
    if (modal) {
      modal.style.display = 'block';
      modal.dataset.target = JSON.stringify({ id: Number(button.dataset.id), action: 'toggle-role' });
    }
    if (title) title.textContent = `角色 ${role?.name || button.dataset.id} 状态确认`;
    if (desc) desc.textContent = `确认后才会处理角色 ${role?.name || button.dataset.id} 的状态。`;
    return;
  }
  if (button.dataset.action === "delete-role") {
    const modal = document.querySelector('[data-role-action-modal]');
    const title = document.querySelector('[data-role-action-title]');
    const desc = document.querySelector('[data-role-action-desc]');
    const roles = await window.hrApi.roles();
    const role = roles.find(item => item.id === Number(button.dataset.id));
    if (modal) {
      modal.style.display = 'block';
      modal.dataset.target = JSON.stringify({ id: Number(button.dataset.id), action: 'delete-role' });
    }
    if (title) title.textContent = `删除角色 ${role?.name || button.dataset.id}`;
    if (desc) desc.textContent = role?.code && ["ADMIN", "LEADER", "OPERATOR"].includes(role.code)
      ? "预置角色不可删除。"
      : "确认后将先检查是否有关联用户，满足条件才会删除。";
    return;
  }
  if (button.dataset.action === "close-role-action-modal") {
    const modal = document.querySelector('[data-role-action-modal]');
    if (modal) modal.style.display = 'none';
    return;
  }
  if (button.dataset.action === "confirm-role-action") {
    const modal = document.querySelector('[data-role-action-modal]');
    const target = modal?.dataset.target ? JSON.parse(modal.dataset.target) : null;
    if (!target) throw new Error('没有待执行的角色操作');
    let role = null;
    if (target.action === 'delete-role') {
      await window.hrApi.deleteRole(target.id);
    } else {
      role = await window.hrApi.toggleRole(target.id);
    }
    const list = document.querySelector('[data-role-list]');
    if (list) {
      const items = await window.hrApi.roles();
      list.innerHTML = items.map(r => `<div class="list-item"><div class="item-top"><div><div class="item-title">${r.name}</div><div class="item-meta">${r.code} · ${r.description}</div></div><div class="table-actions"><button class="btn-sm" data-action="toggle-role" data-id="${r.id}">状态</button><button class="btn-sm" data-action="delete-role" data-id="${r.id}">删除</button></div><span class="chip primary">角色</span></div></div>`).join('');
    }
    await refreshRoleList();
    if (modal) modal.style.display = 'none';
    showToast(target.action === 'delete-role' ? '角色已删除' : `角色状态已处理：${role.code}`);
    return;
  }
  if (button.dataset.action === "open-company-modal") {
    const modal = document.querySelector('[data-company-modal]');
    if (modal) modal.style.display = 'block';
    return;
  }
  if (button.dataset.action === "edit-company") {
    const companies = await window.hrApi.companies();
    const item = companies.find(c => c.id === Number(button.dataset.id));
    if (!item) throw new Error('未找到客户');
    const modal = document.querySelector('[data-company-edit-modal]');
    if (modal) modal.style.display = 'block';
    document.querySelector('[data-company-edit-name]').value = item.name || '';
    document.querySelector('[data-company-edit-contact]').value = item.contact_name || '';
    document.querySelector('[data-company-edit-phone]').value = item.contact_phone || '';
    document.querySelector('[data-company-edit-email]').value = item.contact_email || '';
    document.querySelector('[data-company-edit-address]').value = item.address || '';
    document.querySelector('[data-company-edit-period]').value = item.cooperation_period || '';
    document.querySelector('[data-company-edit-status]').value = item.status || '招聘中';
    document.querySelector('[data-company-edit-remark]').value = item.remark || '';
    if (modal) modal.dataset.target = JSON.stringify({ id: item.id });
    return;
  }
  if (button.dataset.action === "close-company-edit-modal") {
    const modal = document.querySelector('[data-company-edit-modal]');
    if (modal) modal.style.display = 'none';
    return;
  }
  if (button.dataset.action === "confirm-company-edit") {
    const modal = document.querySelector('[data-company-edit-modal]');
    const target = modal?.dataset.target ? JSON.parse(modal.dataset.target) : null;
    if (!target) throw new Error('没有待执行的客户编辑');
    const name = document.querySelector('[data-company-edit-name]')?.value?.trim() || '';
    const contactName = document.querySelector('[data-company-edit-contact]')?.value?.trim() || '';
    const contactPhone = document.querySelector('[data-company-edit-phone]')?.value?.trim() || '';
    const contactEmail = document.querySelector('[data-company-edit-email]')?.value?.trim() || '';
    const address = document.querySelector('[data-company-edit-address]')?.value?.trim() || '';
    const period = document.querySelector('[data-company-edit-period]')?.value?.trim() || '';
    const status = document.querySelector('[data-company-edit-status]')?.value || '招聘中';
    const remark = document.querySelector('[data-company-edit-remark]')?.value?.trim() || '';
    const company = await window.hrApi.request(`/companies/${target.id}`, {
      method: 'PATCH',
      body: JSON.stringify({
        name,
        contact_name: contactName,
        contact_phone: contactPhone,
        contact_email: contactEmail,
        address,
        cooperation_period: period,
        status,
        remark,
      }),
    });
    if (modal) modal.style.display = 'none';
    const list = document.querySelector('.content .panel .list');
    if (list) {
      const companies = await window.hrApi.companies();
      list.innerHTML = companies.slice(0, 3).map(c => `<div class="list-item"><div class="item-top"><div><div class="item-title">${c.name}</div><div class="item-meta">${c.contact_name || ''} · ${c.contact_phone || ''}${c.remark ? ` · ${c.remark}` : ''}</div></div><div class="table-actions"><button class="btn-sm" data-action="edit-company" data-id="${c.id}">编辑</button><button class="btn-sm" data-action="toggle-company" data-id="${c.id}">${c.status === '失效' ? '恢复' : '失效'}</button><button class="btn-sm" data-action="delete-company" data-id="${c.id}">删除</button></div><span class="chip ${c.status === '失效' ? 'neutral' : 'success'}">${c.status || '招聘中'}</span></div></div>`).join('');
    }
    await refreshCompanyMetrics();
    showToast(`客户已更新：${company.name}`);
    return;
  }
  if (button.dataset.action === "close-company-modal") {
    const modal = document.querySelector('[data-company-modal]');
    if (modal) modal.style.display = 'none';
    return;
  }
  if (button.dataset.action === "confirm-company-upload") {
    const name = document.querySelector('[data-company-name]')?.value?.trim() || '';
    const contactName = document.querySelector('[data-company-contact]')?.value?.trim() || '';
    const contactPhone = document.querySelector('[data-company-phone]')?.value?.trim() || '';
    const contactEmail = document.querySelector('[data-company-email]')?.value?.trim() || '';
    const address = document.querySelector('[data-company-address]')?.value?.trim() || '';
    const period = document.querySelector('[data-company-period]')?.value?.trim() || '';
    const status = document.querySelector('[data-company-status]')?.value || '招聘中';
    const remark = document.querySelector('[data-company-remark]')?.value?.trim() || '';
    if (!name) throw new Error('请先填写客户名称');
    const company = await window.hrApi.createCompany({
      name,
      contact_name: contactName,
      contact_phone: contactPhone,
      contact_email: contactEmail,
      address,
      cooperation_period: period,
      status,
      remark,
    });
    const modal = document.querySelector('[data-company-modal]');
    if (modal) modal.style.display = 'none';
    const list = document.querySelector('.content .panel .list');
    if (list) {
      const companies = await window.hrApi.companies();
      list.innerHTML = companies.slice(0, 3).map(c => `<div class="list-item"><div class="item-top"><div><div class="item-title">${c.name}</div><div class="item-meta">${c.contact_name || ''} · ${c.contact_phone || ''}</div></div><div class="table-actions"><button class="btn-sm" data-action="toggle-company" data-id="${c.id}">${c.status === '招聘完毕' ? '恢复' : '完结'}</button><button class="btn-sm" data-action="delete-company" data-id="${c.id}">删除</button></div><span class="chip ${c.status === '招聘完毕' ? 'neutral' : 'success'}">${c.status || '招聘中'}</span></div></div>`).join('');
    }
    await refreshCompanyMetrics();
    showToast(`已创建客户：${company.name}`);
    return;
  }
  if (button.dataset.action === "open-project-modal") {
    const modal = document.querySelector('[data-project-modal]');
    if (modal) modal.style.display = 'block';
    return;
  }
  if (button.dataset.action === "edit-project") {
    const projects = await window.hrApi.projects();
    const item = projects.find(p => p.id === Number(button.dataset.id));
    if (!item) throw new Error('未找到项目');
    const modal = document.querySelector('[data-project-edit-modal]');
    if (modal) modal.style.display = 'block';
    document.querySelector('[data-project-edit-company]').value = String(item.company_id || '');
    document.querySelector('[data-project-edit-name]').value = item.name || '';
    document.querySelector('[data-project-edit-status]').value = item.status || '招聘中';
    document.querySelector('[data-project-edit-level]').value = item.level || 'A';
    document.querySelector('[data-project-edit-count]').value = String(item.hiring_count || 1);
    document.querySelector('[data-project-edit-location]').value = item.work_location || '';
    document.querySelector('[data-project-edit-period]').value = item.project_period || '';
    document.querySelector('[data-project-edit-desc]').value = item.description || '';
    if (modal) modal.dataset.target = JSON.stringify({ id: item.id });
    return;
  }
  if (button.dataset.action === "close-project-edit-modal") {
    const modal = document.querySelector('[data-project-edit-modal]');
    if (modal) modal.style.display = 'none';
    return;
  }
  if (button.dataset.action === "confirm-project-edit") {
    const modal = document.querySelector('[data-project-edit-modal]');
    const target = modal?.dataset.target ? JSON.parse(modal.dataset.target) : null;
    if (!target) throw new Error('没有待执行的项目编辑');
    const companyId = Number(document.querySelector('[data-project-edit-company]')?.value || 0);
    const name = document.querySelector('[data-project-edit-name]')?.value?.trim() || '';
    const status = document.querySelector('[data-project-edit-status]')?.value || '招聘中';
    const level = document.querySelector('[data-project-edit-level]')?.value || 'A';
    const hiringCount = Number(document.querySelector('[data-project-edit-count]')?.value || 1);
    const workLocation = document.querySelector('[data-project-edit-location]')?.value?.trim() || '';
    const period = document.querySelector('[data-project-edit-period]')?.value?.trim() || '';
    const description = document.querySelector('[data-project-edit-desc]')?.value?.trim() || '';
    const project = await window.hrApi.request(`/projects/${target.id}`, {
      method: 'PATCH',
      body: JSON.stringify({
        company_id: companyId,
        name,
        status,
        level,
        hiring_count: hiringCount,
        work_location: workLocation,
        project_period: period,
        description,
      }),
    });
    if (modal) modal.style.display = 'none';
    const list = document.querySelector('.content .panel .list');
    if (list) {
      const projects = await window.hrApi.projects();
      list.innerHTML = projects.slice(0, 3).map(p => `<div class="list-item"><div class="item-top"><div><div class="item-title">${p.name}</div><div class="item-meta">${p.company_name || ''} · ${p.work_location || ''} · ${p.project_period || ''} · 招聘人数 ${p.hiring_count}${p.description ? ` · ${p.description}` : ''}</div></div><div class="table-actions"><button class="btn-sm" data-action="edit-project" data-id="${p.id}">编辑</button><button class="btn-sm" data-action="toggle-project" data-id="${p.id}">${p.status === '招聘完毕' ? '恢复' : '完结'}</button><button class="btn-sm" data-action="delete-project" data-id="${p.id}">删除</button></div><span class="chip ${p.status==='招聘完毕'?'neutral':'success'}">${p.status}</span></div></div>`).join('');
    }
    await refreshProjectMetrics();
    showToast(`项目已更新：${project.name}`);
    return;
  }
  if (button.dataset.action === "close-project-modal") {
    const modal = document.querySelector('[data-project-modal]');
    if (modal) modal.style.display = 'none';
    return;
  }
  if (button.dataset.action === "confirm-project-upload") {
    const companyId = Number(document.querySelector('[data-project-company]')?.value || 0);
    const name = document.querySelector('[data-project-name]')?.value?.trim() || '';
    const status = document.querySelector('[data-project-status]')?.value || '招聘中';
    const level = document.querySelector('[data-project-level]')?.value || 'A';
    const hiringCount = Number(document.querySelector('[data-project-count]')?.value || 1);
    const workLocation = document.querySelector('[data-project-location]')?.value?.trim() || '';
    const period = document.querySelector('[data-project-period]')?.value?.trim() || '';
    const description = document.querySelector('[data-project-desc]')?.value?.trim() || '';
    if (!companyId || !name) throw new Error('请先选择客户并填写项目名称');
    const project = await window.hrApi.createProject({
      company_id: companyId,
      name,
      status,
      level,
      hiring_count: hiringCount,
      work_location: workLocation,
      project_period: period,
      description,
    });
    const modal = document.querySelector('[data-project-modal]');
    if (modal) modal.style.display = 'none';
    const list = document.querySelector('.content .panel .list');
    if (list) {
      const projects = await window.hrApi.projects();
      list.innerHTML = projects.slice(0, 3).map(p => `<div class="list-item"><div class="item-top"><div><div class="item-title">${p.name}</div><div class="item-meta">${p.company_name || ''} · ${p.work_location || ''} · 招聘人数 ${p.hiring_count}</div></div><div class="table-actions"><button class="btn-sm" data-action="toggle-project" data-id="${p.id}">${p.status === '招聘完毕' ? '恢复' : '完结'}</button><button class="btn-sm" data-action="delete-project" data-id="${p.id}">删除</button></div><span class="chip ${p.status==='招聘完毕'?'neutral':'success'}">${p.status}</span></div></div>`).join('');
    }
    await refreshProjectMetrics();
    showToast(`已创建项目：${project.name}`);
    return;
  }
  if (button.dataset.action === "open-tag-modal") {
    const modal = document.querySelector('[data-tag-modal]');
    if (modal) modal.style.display = 'block';
    return;
  }
  if (button.dataset.action === "close-tag-modal") {
    const modal = document.querySelector('[data-tag-modal]');
    if (modal) modal.style.display = 'none';
    return;
  }
  if (button.dataset.action === "confirm-tag-upload") {
    const category = document.querySelector('[data-tag-category]')?.value?.trim() || '';
    const name = document.querySelector('[data-tag-name]')?.value?.trim() || '';
    const color = document.querySelector('[data-tag-color]')?.value?.trim() || '';
    const enabled = document.querySelector('[data-tag-enabled-input]')?.value !== 'false';
    if (!category || !name) throw new Error('请先填写标签分类和名称');
    const tag = await window.hrApi.createTag({ category, name, color, enabled });
    const modal = document.querySelector('[data-tag-modal]');
    if (modal) modal.style.display = 'none';
    const list = document.querySelector('[data-tag-list]');
    if (list) {
      const tags = await window.hrApi.tags();
      list.innerHTML = tags.slice(0, 5).map(t => `<div class="list-item"><div class="item-top"><div><div class="item-title">${t.category}</div><div class="item-meta">${t.name}</div></div><div class="table-actions"><button class="btn-sm" data-action="toggle-tag" data-id="${t.id}" data-enabled="${t.enabled}">${t.enabled ? '禁用' : '启用'}</button><button class="btn-sm" data-action="delete-tag" data-id="${t.id}">删除</button></div></div></div>`).join('');
    }
    showToast(`已创建标签：${tag.name}`);
    return;
  }
  if (button.dataset.action === "delete-tag") {
    const modal = document.querySelector('[data-tag-action-modal]');
    const title = document.querySelector('[data-tag-action-title]');
    const desc = document.querySelector('[data-tag-action-desc]');
    if (modal) {
      modal.style.display = 'block';
      modal.dataset.target = JSON.stringify({ kind: 'delete-tag', id: Number(button.dataset.id) });
    }
    if (title) title.textContent = `删除标签 ${button.dataset.id}`;
    if (desc) desc.textContent = '确认后将永久删除该标签。';
    return;
  }
  if (button.dataset.action === "close-tag-action-modal") {
    const modal = document.querySelector('[data-tag-action-modal]');
    if (modal) modal.style.display = 'none';
    return;
  }
  if (button.dataset.action === "confirm-tag-action") {
    const modal = document.querySelector('[data-tag-action-modal]');
    const target = modal?.dataset.target ? JSON.parse(modal.dataset.target) : null;
    if (!target) throw new Error('没有待执行的标签操作');
    if (target.kind === 'delete-tag') {
      await window.hrApi.request(`/tags/${target.id}`, { method: "DELETE" });
      const list = document.querySelector(".content .panel .list");
      if (list) {
        const tags = await window.hrApi.tags();
        list.innerHTML = tags.slice(0, 5).map(t => `<div class="list-item"><div class="item-top"><div><div class="item-title">${t.category}</div><div class="item-meta">${t.name}</div></div><span class="chip ${t.enabled ? 'success' : 'neutral'}">${t.enabled ? '启用' : '禁用'}</span></div></div>`).join("");
      }
      showToast("已删除标签");
    }
    if (modal) modal.style.display = 'none';
    return;
  }
  if (button.dataset.action === "noop") {
    showToast(`已点击：${text || "操作"}`);
    return;
  }
  if (button.tagName === "BUTTON") {
    showToast(`已点击：${text || "按钮"}`);
  }
}

function bindActionButtons() {
  document.querySelectorAll("button[data-action]").forEach((btn) => {
    if (btn.dataset.bound === "true") return;
    btn.dataset.bound = "true";
    btn.addEventListener("click", (event) => {
      event.preventDefault();
      handleGlobalButton(btn).catch((err) => showToast(`操作失败：${err.message || err}`));
    });
  });
}

document.addEventListener("click", (event) => {
  const btn = event.target.closest("button");
  if (!btn) return;
  const explicitAction = btn.dataset.action;
  if (!explicitAction && !/^(详情|搜索|导入简历|导出选中|选择文件|查看项目进度|进入求职者数据池|查看待办)/.test((btn.textContent || "").trim())) return;
  if (btn.dataset.bound === "true") return;
  event.preventDefault();
  handleGlobalButton(btn).catch((err) => showToast(`操作失败：${err.message || err}`));
});

window.renderApp = render;
