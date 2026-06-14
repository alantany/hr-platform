const nav = [
  ["dashboard.html", "首页", "概览"],
  ["candidates.html", "求职者数据池", "资源"],
  ["import.html", "简历导入", "导入"],
  ["customers.html", "客户管理", "客户"],
  ["projects.html", "项目管理", "项目"],
  ["evaluations.html", "评价体系", "评价"],
  ["warranty.html", "质保期管理", "质保"],
  ["statistics.html", "统计管理", "报表"],
  ["users.html", "用户管理", "账号"],
  ["roles.html", "角色管理", "角色"],
  ["permissions.html", "权限管理", "权限"],
  ["data-permissions.html", "数据权限", "范围"],
  ["dictionary.html", "标签字典", "标签"],
  ["logs.html", "操作日志", "日志"],
];

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
  logs: { crumbs: "系统设置 / 操作日志", title: "操作日志", desc: "查看导入、推荐、权限变更等关键操作记录。" },
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

function shell(pageKey, body) {
  const active = (p) => p === `${pageKey}.html` || (pageKey === "index" && p === "dashboard.html");
  const navHtml = nav.map(([href, label, badge]) => `
    <a class="nav-item ${active(href) ? "active" : ""}" href="./${href}">
      <span class="nav-icon">${badge === "概览" ? icons.home : badge === "资源" ? icons.users : badge === "导入" ? icons.file : badge === "客户" ? icons.building : badge === "项目" ? icons.inbox : badge === "评价" ? icons.star : badge === "质保" ? icons.settings : badge === "报表" ? icons.chart : badge === "账号" ? icons.users : badge === "角色" ? icons.settings : badge === "权限" ? icons.settings : badge === "范围" ? icons.settings : badge === "标签" ? icons.settings : icons.log}</span>
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
          <div class="user-chip"><div class="avatar"></div><div><div style="font-weight:700">管理员</div><div class="small-muted">超级管理员</div></div></div>
        </div>
      </div>
      ${body}
    </main>
  </div>`;
}

function render() {
  const page = location.pathname.split("/").pop() || "dashboard.html";
  const key = page.replace(".html", "");
  const el = document.getElementById("app");
  if (!el) return;
  el.innerHTML = shell(key, window.__PAGE_BODY__ || "");
}

window.renderApp = render;
