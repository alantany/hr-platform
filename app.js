const navGroups = [
  {
    title: "主要功能",
    items: [
      { href: "dashboard.html", label: "首页", badge: "概览", icon: "home" },
      { href: "candidates.html", label: "求职者数据池", badge: "资源", icon: "users" },
      { href: "import.html", label: "简历导入", badge: "导入", icon: "file" },
      { href: "customers.html", label: "客户管理", badge: "客户", icon: "building" },
      { href: "projects.html", label: "项目管理", badge: "项目", icon: "inbox" },
      { href: "positions.html", label: "岗位管理", badge: "岗位", icon: "settings" },
      { href: "evaluations.html", label: "评价体系", badge: "评价", icon: "star" },
      { href: "statistics.html", label: "统计管理", badge: "报表", icon: "chart" },
    ],
  },
  {
    title: "岗位管理",
    items: [
      { href: "recruit-job-publish.html", label: "岗位发布", badge: "发布", icon: "file" },
      { href: "recruit-job-list.html", label: "岗位列表", badge: "列表", icon: "inbox" },
      { href: "recruit-daily-tasks.html", label: "每日任务", badge: "任务", icon: "chart" },
    ],
  },
  {
    title: "系统设置",
    items: [
      { href: "dictionary.html", label: "标签字典", badge: "标签", icon: "settings" },
      { href: "users.html", label: "用户管理", badge: "账号", icon: "users" },
      { href: "roles.html", label: "角色管理", badge: "角色", icon: "settings" },
      { href: "permissions.html", label: "权限管理", badge: "权限", icon: "settings" },
      { href: "data-permissions.html", label: "数据权限", badge: "范围", icon: "settings" },
      { href: "warranty.html", label: "质保期管理", badge: "质保", icon: "settings" },
      { href: "logs.html", label: "操作日志", badge: "日志", icon: "log" },
    ],
  },
  {
    title: "开发工具",
    items: [
      { href: "db-explorer.html", label: "数据探针", badge: "探针", icon: "settings" },
    ],
  },
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
    desc: "统一管理项目下的岗位、紧急程度、招聘人数与薪资范围。",
  },
  "recruit-job-publish": {
    crumbs: "岗位管理 / 岗位发布",
    title: "岗位发布",
    desc: "发布供 Recruit 抓取后台读取的岗位条件，数据写入 PostgreSQL 的 recruit.job_postings。",
  },
  "recruit-job-list": {
    crumbs: "岗位管理 / 岗位列表",
    title: "岗位列表",
    desc: "查看和维护 Recruit 岗位库，控制岗位是否参与抓取任务。",
  },
  "recruit-daily-tasks": {
    crumbs: "岗位管理 / 每日任务",
    title: "每日任务",
    desc: "按日期查看 Recruit 抓取任务的打招呼、索要简历、下载和回执统计。",
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
    desc: "直接读取与呈现系统底层的 PostgreSQL 物理表数据，用于开发辅助及状态查验。"
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

const navItems = navGroups.flatMap((group) => group.items);

const renderCompanyListMarkup = (companies = []) => {
  if (!companies.length) {
    return '<div class="list-item"><div class="item-top"><div><div class="item-title">暂无客户列表</div><div class="item-meta">客户列表来自数据库。</div></div><span class="chip success">客户</span></div></div>';
  }
  return companies.map((c) => {
    const meta = [c.contact_name, c.contact_phone, c.contact_email, c.address, c.cooperation_period, c.remark].filter(Boolean).join(' · ');
    const chipClass = c.status === '招聘中' ? 'success' : 'neutral';
    return `<div class="list-item"><div class="item-top"><div><div class="item-title">${c.name}</div><div class="item-meta">${meta || '暂无补充信息'}</div></div><div class="table-actions"><button class="btn-sm" data-action="edit-company" data-id="${c.id}">编辑</button><button class="btn-sm" data-action="delete-company" data-id="${c.id}">删除</button></div><span class="chip ${chipClass}">${c.status || '未招聘'}</span></div></div>`;
  }).join('');
};

const treeState = {
  expandedCompanies: new Set(),
  expandedProjects: new Set(),
  expandedPositions: new Set(),
  projectsByCompany: new Map(),
  positionsByProject: new Map(),
  candidatesByPosition: new Map(),
  loadingCompanies: new Set(),
  loadingProjects: new Set(),
  loadingPositions: new Set(),
};

const getCompanyNodeState = (companyId) => {
  if (treeState.loadingCompanies.has(companyId)) return 'loading';
  return treeState.expandedCompanies.has(companyId) ? 'expanded' : 'collapsed';
};

const getProjectNodeState = (projectId) => {
  if (treeState.loadingProjects.has(projectId)) return 'loading';
  return treeState.expandedProjects.has(projectId) ? 'expanded' : 'collapsed';
};

const getPositionNodeState = (positionId) => {
  if (treeState.loadingPositions.has(positionId)) return 'loading';
  return treeState.expandedPositions.has(positionId) ? 'expanded' : 'collapsed';
};

const renderTreeToggle = (state, level = 'company', targetId = '') => {
  const isLoading = state === 'loading';
  const isExpanded = state === 'expanded';
  const symbol = isLoading ? '⏳' : isExpanded ? '▾' : '▸';
  const label = isLoading ? '加载中' : isExpanded ? '收起' : '展开';
  return `<button class="btn-sm tree-toggle${isLoading ? ' is-busy' : ''}" data-action="toggle-tree" data-tree-toggle="${level}" data-tree-id="${targetId}" aria-label="${label}" aria-expanded="${isExpanded}" type="button"${isLoading ? ' disabled' : ''}>${symbol}</button>`;
};

const renderCandidateTreeItem = (candidate, index = 1, depth = 3) => {
  const meta = [
    candidate.current_title || '暂无当前职位',
    candidate.city || '',
    candidate.source || '',
    `推荐状态 ${candidate.recommendation_status || '待推荐'}`,
  ].filter(Boolean).join(' · ');
  const isLocked = Boolean(candidate.locked) || candidate.status === '锁定';
  const isEven = index % 2 === 0;
  const bgStyle = isEven ? 'background-color: #f8fafc;' : 'background-color: #ffffff;';
  return `
    <div class="list-item tree-node tree-node-candidate" data-tree-node="candidate" data-id="${candidate.id}" style="${bgStyle}">
      <div class="item-top">
        <span style="font-size: 11px; font-weight: 600; color: #94a3b8; width: 18px; display: inline-block; flex-shrink: 0; text-align: center; margin-right: 4px;">${index}</span>
        <input type="checkbox" class="tree-candidate-checkbox" data-candidate-id="${candidate.id}" data-recommendation-id="${candidate.recommendation_id || ''}" aria-label="选择${candidate.name}" style="margin-right:8px;flex-shrink:0;" />
        <div style="flex: 1; min-width: 0;">
          <div class="item-title"><span>${escapeHtml(candidate.name || '未命名候选人')}</span></div>
          <div class="item-meta">${escapeHtml(meta)}</div>
        </div>
        <div class="table-actions" style="display: flex; gap: 8px; align-items: center; justify-content: flex-start; flex-shrink: 0; width: 420px; margin-right: 16px;">
          <button class="btn-sm" data-action="edit-candidate-tree" data-id="${candidate.id}">编辑</button>
        </div>
        <span class="chip ${isLocked ? 'warning' : 'neutral'}" style="flex-shrink: 0; width: 80px; text-align: center; display: inline-block;">${isLocked ? '已锁定' : escapeHtml(candidate.status || '未锁定')}</span>
      </div>
    </div>`;
};

const renderPositionTreeItem = (position, project, company, candidates = [], depth = 2) => {
  const state = getPositionNodeState(position.id);
  const meta = [
    company?.name || '未知客户',
    project?.name || `项目 ${position.project_id}`,
    position.location || '',
    `招聘人数 ${position.hiring_count || 1}`,
    position.salary_min || position.salary_max ? `${position.salary_min || ''}-${position.salary_max || ''}` : '',
  ].filter(Boolean).join(' · ');
  const children = treeState.expandedPositions.has(position.id)
    ? candidates.map((candidate, idx) => renderCandidateTreeItem(candidate, idx + 1, depth + 1)).join('') || `<div class="list-item tree-node tree-node-empty"><div class="item-meta">该岗位下暂无已推荐候选人。</div></div>`
    : '';

  const isOnPositionPage = Boolean(document.querySelector('[data-position-list]'));

  if (isOnPositionPage) {
    const stats = window.positionRecommendationStats?.get(position.id) || { total: 0, selected: 0, unselected: 0, rejected: 0 };
    const funnelHtml = `
      <div style="display: flex; gap: 8px; font-size: 12px; font-weight: 600; flex-wrap: nowrap; white-space: nowrap;">
        <span style="color: #64748b;">候选人 <strong style="color: #8b5cf6; font-size: 13px; margin-left: 2px;">${stats.total}</strong></span>
        <span style="color: #64748b;">选中 <strong style="color: #10b981; font-size: 13px; margin-left: 2px;">${stats.selected}</strong></span>
        <span style="color: #64748b;">未选 <strong style="color: #64748b; font-size: 13px; margin-left: 2px;">${stats.unselected}</strong></span>
        <span style="color: #64748b;">淘汰 <strong style="color: #ef4444; font-size: 13px; margin-left: 2px;">${stats.rejected}</strong></span>
      </div>
    `;

    // Urgency tag & chip
    const urgencyBg = position.urgency === '高' 
      ? 'background: #fee2e2; color: #ef4444; border: 1px solid #fecaca;' 
      : (position.urgency === '中' ? 'background: #ffedd5; color: #f97316; border: 1px solid #fed7aa;' : 'background: #eff6ff; color: #3b82f6; border: 1px solid #bfdbfe;');
    const urgencyText = position.urgency || '中';
    const urgencyBadge = `<span class="chip" style="${urgencyBg} width: 48px; text-align: center; display: inline-block; font-weight: 600;">${urgencyText}</span>`;
    const tagHtml = position.urgency === '高' 
      ? `<span class="chip" style="background:#fee2e2; color:#ef4444; border:1px solid #fecaca; margin-left:4px; padding: 2px 6px; font-size:10px; font-weight:600; border-radius: 4px; white-space: nowrap;">x 紧急</span>` 
      : '';

    return `
      <div class="list-item tree-node tree-node-position" data-tree-node="position" data-id="${position.id}" data-project-id="${position.project_id}">
        <div class="item-top" style="display: grid; grid-template-columns: 1.2fr 1.5fr 1.8fr 0.8fr 0.8fr 1fr 1.2fr 2.5fr 180px; gap: 10px; align-items: center; padding: 12px 16px; border-bottom: 1px solid #e2e8f0;">
          <div style="color: #475569; font-size: 13px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;" title="${escapeHtml(project?.company_name || company?.name || '未知公司')}">${escapeHtml(project?.company_name || company?.name || '未知公司')}</div>
          <div style="color: #475569; font-size: 13px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;" title="${escapeHtml(project?.name || '')}">${escapeHtml(project?.name || '--')}</div>
          <div class="item-title" style="display: flex; align-items: center; gap: 4px; min-width: 0; margin-right: 0;">
            ${renderTreeToggle(state, 'position', position.id)}
            <span style="font-weight: 600; color: #0f172a;">${escapeHtml(position.name)}</span>
            ${tagHtml}
          </div>
          <div style="text-align: center;">${urgencyBadge}</div>
          <div style="color: #475569; font-size: 13px; text-align: center;">${position.hiring_count || 1}人</div>
          <div style="color: #475569; font-size: 13px; text-align: center;">${position.salary_min || position.salary_max ? `${position.salary_min || ''}-${position.salary_max || ''}K` : '--'}</div>
          <div style="color: #475569; font-size: 13px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;" title="${escapeHtml(position.location || '')}">${escapeHtml(position.location || '--')}</div>
          <div>${funnelHtml}</div>
          <div class="table-actions" style="display: flex; gap: 8px; align-items: center; justify-content: flex-end;">
            <button class="btn-sm" data-action="edit-position" data-id="${position.id}">编辑</button>
            <button class="btn-sm" data-action="noop" data-title="分配权限">分配权限</button>
            <button class="btn-sm" data-action="delete-position" data-id="${position.id}">删除</button>
          </div>
        </div>
        ${children ? `<div class="tree-children">${children}</div>` : ''}
      </div>`;
  }

  return `
    <div class="list-item tree-node tree-node-position" data-tree-node="position" data-id="${position.id}" data-project-id="${position.project_id}">
      <div class="item-top">
        <div style="flex: 1; min-width: 0;">
          <div class="item-title">
            ${renderTreeToggle(state, 'position', position.id)}
            <span>${position.name}</span>
          </div>
          <div class="item-meta">${meta || '暂无补充信息'}</div>
        </div>
        <div class="table-actions" style="display: flex; gap: 8px; align-items: center; justify-content: flex-start; flex-shrink: 0; width: 420px; margin-right: 16px;">
          <button class="btn-sm" data-action="edit-position" data-id="${position.id}">编辑</button>
          <button class="btn-sm" data-action="delete-position" data-id="${position.id}">删除</button>
          <span style="border-left: 1px solid rgba(15,23,42,.1); height: 16px; margin: 0 24px; display: inline-block;"></span>
          <button class="btn-sm primary" data-action="search-add-candidates" data-id="${position.id}">添加候选人</button>
          <button class="btn-sm danger" data-action="batch-delete-candidates-tree" data-position-batch-delete="${position.id}" disabled style="opacity:0.4;cursor:not-allowed;">批量移除</button>
        </div>
      </div>
      ${children ? `<div class="tree-children">${children}</div>` : ''}
    </div>`;
};

const renderProjectTreeItem = (project, company, positions = [], candidatesByPosition = new Map(), depth = 1) => {
  const state = getProjectNodeState(project.id);

  const meta = [company?.name || project.company_name || '', project.work_location || '', project.project_period || '', `招聘人数 ${project.hiring_count || 0}人`, project.description ? project.description : ''].filter(Boolean).join(' · ');
  const chipClass = project.status === '招聘完毕' ? 'neutral' : 'success';
  const children = treeState.expandedProjects.has(project.id)
    ? positions.map((position) => renderPositionTreeItem(position, project, company, candidatesByPosition.get(position.id) || [], depth + 1)).join('') || '<div class="list-item tree-node tree-node-empty"><div class="item-meta">该项目下暂无岗位。</div></div>'
    : '';

  const isOnProjectPage = Boolean(document.querySelector('[data-project-list]'));
  
  if (isOnProjectPage) {
    const formatDate = (isoString) => {
      if (!isoString) return '--';
      return isoString.split('T')[0];
    };
    
    // Level badge styling: supporting both legacy A/B/C and new 高/中/低
    const isLevelHigh = project.level === 'A' || project.level === '高';
    const isLevelMedium = project.level === 'B' || project.level === '中';
    const levelBg = isLevelHigh
      ? 'background: #fee2e2; color: #ef4444; border: 1px solid #fecaca;' 
      : (isLevelMedium ? 'background: #ffedd5; color: #f97316; border: 1px solid #fed7aa;' : 'background: #eff6ff; color: #3b82f6; border: 1px solid #bfdbfe;');
    const levelText = isLevelHigh ? '高' : (isLevelMedium ? '中' : '低');
    const levelBadge = `<span class="chip" style="${levelBg} width: 48px; text-align: center; display: inline-block; font-weight: 600;">${levelText}</span>`;

    return `
      <div class="list-item tree-node tree-node-project" data-tree-node="project" data-id="${project.id}" data-company-id="${project.company_id}">
        <div class="item-top" style="display: grid; grid-template-columns: 1.2fr 1.5fr 1fr 0.8fr 0.8fr 1.2fr 0.8fr 1.2fr 180px; gap: 10px; align-items: center; padding: 12px 16px; border-bottom: 1px solid #e2e8f0;">
          <div style="color: #475569; font-size: 13px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;" title="${escapeHtml(project.company_name || company?.name || '未知公司')}">${escapeHtml(project.company_name || company?.name || '未知公司')}</div>
          <div class="item-title" style="display: flex; align-items: center; gap: 6px; min-width: 0; margin-right: 0;">
            ${renderTreeToggle(state, 'project', project.id)}
            <span style="font-weight: 600; color: #0f172a;">${escapeHtml(project.name)}</span>
          </div>
          <div style="text-align: center;">
            <span class="chip ${chipClass}" style="width: 80px; text-align: center; display: inline-block; margin: 0 auto;">${project.status}</span>
          </div>
          <div style="text-align: center;">${levelBadge}</div>
          <div style="color: #475569; font-size: 13px; text-align: center;">${project.hiring_count || 0}人</div>
          <div style="color: #475569; font-size: 13px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;" title="${escapeHtml(project.work_location || '')}">${escapeHtml(project.work_location || '--')}</div>
          <div style="color: #475569; font-size: 13px; text-align: center;">${project.position_count || 0}</div>
          <div style="color: #475569; font-size: 13px;">${formatDate(project.created_at)}</div>
          <div class="table-actions" style="display: flex; gap: 8px; align-items: center; justify-content: flex-end;">
            <button class="btn-sm" data-action="noop" data-title="项目岗位列表" onclick="const tab = document.querySelector('[data-subtab=position-tab]'); if(tab){tab.click(); const select = document.querySelector('#search-position-project'); if(select){select.value='${project.id}'; document.querySelector('#btn-position-search').click();}}">岗位</button>
            <button class="btn-sm" data-action="edit-project" data-id="${project.id}">编辑</button>
            <button class="btn-sm" data-action="delete-project" data-id="${project.id}">删除</button>
          </div>
        </div>
        ${children ? `<div class="tree-children">${children}</div>` : ''}
      </div>`;
  }

  return `
    <div class="list-item tree-node tree-node-project" data-tree-node="project" data-id="${project.id}" data-company-id="${project.company_id}">
      <div class="item-top">
        <div style="flex: 1; min-width: 0;">
          <div class="item-title">
            ${renderTreeToggle(state, 'project', project.id)}
            <span>${project.name}</span>
          </div>
          <div class="item-meta">${meta || '暂无补充信息'}</div>
        </div>
        <div class="table-actions" style="display: flex; gap: 8px; align-items: center; justify-content: flex-start; flex-shrink: 0; width: 220px; margin-right: 16px;">
          <button class="btn-sm" data-action="edit-project" data-id="${project.id}">编辑</button>
          <button class="btn-sm" data-action="delete-project" data-id="${project.id}">删除</button>
        </div>
        <span class="chip ${chipClass}" style="flex-shrink: 0; width: 80px; text-align: center; display: inline-block;">${project.status}</span>
      </div>
      ${children ? `<div class="tree-children">${children}</div>` : ''}
    </div>`;
};

const renderCompanyTreeItem = (company, projects = [], positionsByProject = new Map(), candidatesByPosition = new Map()) => {
  const state = getCompanyNodeState(company.id);
  const children = treeState.expandedCompanies.has(company.id)
    ? projects.map((project) => renderProjectTreeItem(project, company, positionsByProject.get(project.id) || [], candidatesByPosition, 1)).join('') || '<div class="list-item tree-node tree-node-empty"><div class="item-meta">该客户下暂无项目。</div></div>'
    : '';
  
  const computedStatus = company.status || '未招聘';
  const chipClass = computedStatus === '未招聘' ? 'neutral' : 'success';

  return `
    <div class="list-item tree-node tree-node-company" data-tree-node="company" data-id="${company.id}">
      <div class="item-top" style="display: grid; grid-template-columns: 1.5fr 1fr 1.2fr 1.5fr 0.8fr 0.8fr 1.2fr 100px; gap: 10px; align-items: center; padding: 12px 16px; border-bottom: 1px solid #e2e8f0;">
        <div class="item-title" style="display: flex; align-items: center; gap: 6px; min-width: 0; margin-right: 0;">
          ${renderTreeToggle(state, 'company', company.id)}
          <span style="font-weight: 600; color: #0f172a;">${escapeHtml(company.name)}</span>
        </div>
        <div style="color: #475569; font-size: 13px;">${escapeHtml(company.contact_name || '--')}</div>
        <div style="color: #475569; font-size: 13px;">${escapeHtml(company.contact_phone || '--')}</div>
        <div style="color: #475569; font-size: 13px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;" title="${escapeHtml(company.address || '')}">${escapeHtml(company.address || '--')}</div>
        <div style="color: #475569; font-size: 13px; text-align: center;">${company.project_count || 0}</div>
        <div style="color: #475569; font-size: 13px; text-align: center;">${company.position_count || 0}</div>
        <div style="text-align: center;">
          <span class="chip ${chipClass}" style="width: 80px; text-align: center; display: inline-block; margin: 0 auto;">${computedStatus}</span>
        </div>
        <div class="table-actions" style="display: flex; gap: 6px; align-items: center; justify-content: flex-end;">
          <button class="btn-sm" data-action="edit-company" data-id="${company.id}">编辑</button>
          <button class="btn-sm" data-action="delete-company" data-id="${company.id}">删除</button>
        </div>
      </div>
      ${children ? `<div class="tree-children">${children}</div>` : ''}
    </div>`;
};

const renderCompanyTreeMarkup = (companies = [], projectsByCompany = new Map(), positionsByProject = new Map(), candidatesByPosition = new Map()) => {
  if (!companies.length) {
    return '<div class="list-item"><div class="item-top"><div><div class="item-title">暂无客户列表</div><div class="item-meta">客户列表来自数据库。</div></div><span class="chip success">客户</span></div></div>';
  }
  return companies.map((company) => renderCompanyTreeItem(company, projectsByCompany.get(company.id) || [], positionsByProject, candidatesByPosition)).join('');
};

const getProjectActionLabel = (status = '') => {
  if (status === '招聘中') return '完结';
  if (status === '招聘完毕') return '中止';
  if (status === '招聘中止') return '恢复';
  return '完结';
};

const getProjectNextStatus = (status = '') => {
  if (status === '招聘中') return '招聘完毕';
  if (status === '招聘完毕') return '招聘中止';
  if (status === '招聘中止') return '招聘中';
  return '招聘中';
};

const renderProjectListMarkup = (projects = []) => {
  if (!projects.length) {
    return '<div class="list-item"><div class="item-top"><div><div class="item-title">当前暂无项目列表</div><div class="item-meta">项目表中的真实项目来自数据库。</div></div><span class="chip success">项目</span></div></div>';
  }
  return projects.slice(0, 3).map((p) => {
    const meta = [p.company_name || '', p.work_location || '', p.project_period || '', `招聘人数 ${p.hiring_count}`, p.description ? p.description : ''].filter(Boolean).join(' · ');
    const chipClass = p.status === '招聘完毕' ? 'neutral' : 'success';
    return `<div class="list-item"><div class="item-top"><div><div class="item-title">${p.name}</div><div class="item-meta">${meta || '暂无补充信息'}</div></div><div class="table-actions"><button class="btn-sm" data-action="edit-project" data-id="${p.id}">编辑</button><button class="btn-sm" data-action="toggle-project" data-id="${p.id}">${getProjectActionLabel(p.status)}</button><button class="btn-sm" data-action="delete-project" data-id="${p.id}">删除</button></div><span class="chip ${chipClass}">${p.status}</span></div></div>`;
  }).join('');
};

const renderProjectTreeMarkup = (projects = [], positionsByProject = new Map(), candidatesByPosition = new Map()) => {
  if (!projects.length) {
    return '<div class="list-item"><div class="item-top"><div><div class="item-title">当前暂无项目列表</div><div class="item-meta">项目表中的真实项目来自数据库。</div></div><span class="chip success">项目</span></div></div>';
  }
  return projects.map((project) => {
    const company = { name: project.company_name || '未知客户' };
    const positions = positionsByProject.get(project.id) || [];
    return renderProjectTreeItem(project, company, positions, candidatesByPosition, 1);
  }).join('');
};

const renderPositionTreeMarkup = (positions = [], projectsById = new Map(), candidatesByPosition = new Map()) => {
  if (!positions.length) {
    return '<div class="list-item"><div class="item-meta">暂无岗位数据。</div></div>';
  }
  return positions.map((position) => {
    const project = projectsById.get(position.project_id) || { id: position.project_id, name: `项目 ${position.project_id}`, company_name: '未知客户' };
    return renderPositionTreeItem(position, project, { name: project.company_name || '未知客户' }, candidatesByPosition.get(position.id) || [], 0);
  }).join('');
};

window.hrRenderCompanyList = renderCompanyListMarkup;
window.hrRenderProjectList = renderProjectListMarkup;
window.hrRenderCompanyTree = renderCompanyTreeMarkup;
window.hrRenderProjectTree = renderProjectTreeMarkup;
window.hrRenderPositionTree = renderPositionTreeMarkup;

async function refreshCustomerTree() {
  const list = document.querySelector('[data-company-list]');
  if (!list) return;
  const [companies, projects, positions] = await Promise.all([
    window.hrApi.companies(),
    window.hrApi.projects(),
    window.hrApi.positions(),
  ]);
  const projectsByCompany = new Map();
  projects.forEach((project) => {
    const bucket = projectsByCompany.get(project.company_id) || [];
    bucket.push(project);
    projectsByCompany.set(project.company_id, bucket);
  });
  const positionsByProject = new Map();
  positions.forEach((position) => {
    const bucket = positionsByProject.get(position.project_id) || [];
    bucket.push(position);
    positionsByProject.set(position.project_id, bucket);
  });
  list.innerHTML = window.hrRenderCompanyTree
    ? window.hrRenderCompanyTree(companies, projectsByCompany, positionsByProject, treeState.candidatesByPosition)
    : renderCompanyListMarkup(companies);
}

async function renderCustomerTreeFromState() {
  const list = document.querySelector('[data-company-list]');
  if (!list) return;
  const companies = await window.hrApi.companies();
  const projects = Array.from(treeState.projectsByCompany.entries()).flatMap(([, items]) => items);
  const positions = Array.from(treeState.positionsByProject.entries()).flatMap(([, items]) => items);
  const projectsByCompany = new Map();
  projects.forEach((project) => {
    const bucket = projectsByCompany.get(project.company_id) || [];
    bucket.push(project);
    projectsByCompany.set(project.company_id, bucket);
  });
  const positionsByProject = new Map();
  positions.forEach((position) => {
    const bucket = positionsByProject.get(position.project_id) || [];
    bucket.push(position);
    positionsByProject.set(position.project_id, bucket);
  });
  list.innerHTML = window.hrRenderCompanyTree
    ? window.hrRenderCompanyTree(companies, projectsByCompany, positionsByProject, treeState.candidatesByPosition)
    : renderCompanyListMarkup(companies);
}

async function loadCompanyProjects(companyId) {
  const companyKey = Number(companyId);
  if (!companyKey) return [];
  if (!treeState.projectsByCompany.has(companyKey)) {
    treeState.loadingCompanies.add(companyKey);
    try {
      const projects = await window.hrApi.projects({ company_id: companyKey });
      treeState.projectsByCompany.set(companyKey, projects);
    } finally {
      treeState.loadingCompanies.delete(companyKey);
    }
  }
  return treeState.projectsByCompany.get(companyKey) || [];
}

async function loadProjectPositions(projectId) {
  const projectKey = Number(projectId);
  if (!projectKey) return [];
  if (!treeState.positionsByProject.has(projectKey)) {
    treeState.loadingProjects.add(projectKey);
    try {
      const positions = await window.hrApi.positions({ project_id: projectKey });
      treeState.positionsByProject.set(projectKey, positions);
    } finally {
      treeState.loadingProjects.delete(projectKey);
    }
  }
  return treeState.positionsByProject.get(projectKey) || [];
}

async function loadPositionCandidates(positionId) {
  const positionKey = Number(positionId);
  if (!positionKey) return [];
  if (!treeState.candidatesByPosition.has(positionKey)) {
    treeState.loadingPositions.add(positionKey);
    try {
      const recommendations = await window.hrApi.recommendations({ position_id: positionKey });
      const latestByCandidate = new Map();
      recommendations.forEach((recommendation) => {
        if (!latestByCandidate.has(recommendation.candidate_id)) {
          latestByCandidate.set(recommendation.candidate_id, recommendation);
        }
      });
      const candidates = await Promise.all(Array.from(latestByCandidate.entries()).map(async ([candidateId, recommendation]) => {
        try {
          const candidate = await window.hrApi.candidate(String(candidateId));
          return {
            ...candidate,
            recommendation_id: recommendation.id,
            recommendation_status: recommendation.status,
            recommendation_feedback: recommendation.feedback || '',
          };
        } catch (err) {
          console.warn(`Failed to load candidate ${candidateId} for position ${positionKey}`, err);
          return null;
        }
      }));
      treeState.candidatesByPosition.set(positionKey, candidates.filter(Boolean));
    } finally {
      treeState.loadingPositions.delete(positionKey);
    }
  }
  return treeState.candidatesByPosition.get(positionKey) || [];
}

async function renderProjectTreeFromState() {
  const projectList = document.querySelector('[data-project-list]');
  if (!projectList) return;
  const [projects, positions] = await Promise.all([
    window.hrApi.projects(),
    window.hrApi.positions(),
  ]);

  let filteredProjects = projects;
  if (window.projectFilters) {
    const { name, companyId, status, level } = window.projectFilters;
    if (name) {
      filteredProjects = filteredProjects.filter(p => p.name && p.name.toLowerCase().includes(name.toLowerCase()));
    }
    if (companyId) {
      filteredProjects = filteredProjects.filter(p => p.company_id === Number(companyId));
    }
    if (status) {
      filteredProjects = filteredProjects.filter(p => p.status === status);
    }
    if (level) {
      filteredProjects = filteredProjects.filter(p => p.level === level);
    }
  }

  const projectTitle = document.querySelector('#project-list-title');
  if (projectTitle) {
    projectTitle.textContent = `项目列表 (共 ${filteredProjects.length} 个)`;
  }

  const positionsByProject = new Map();
  positions.forEach((position) => {
    const bucket = positionsByProject.get(position.project_id) || [];
    bucket.push(position);
    positionsByProject.set(position.project_id, bucket);
  });
  projectList.innerHTML = window.hrRenderProjectTree
    ? window.hrRenderProjectTree(filteredProjects, positionsByProject, treeState.candidatesByPosition)
    : (window.hrRenderProjectList ? window.hrRenderProjectList(filteredProjects) : '');
}

async function renderPositionTreeFromState() {
  const positionList = document.querySelector('[data-position-list]');
  if (!positionList) return;
  const [positions, projects, recommendations] = await Promise.all([
    window.hrApi.positions(),
    window.hrApi.projects(),
    window.hrApi.recommendations(),
  ]);

  // Compute funnel stats globally
  const statsMap = new Map();
  recommendations.forEach(r => {
    const pId = r.position_id;
    if (!statsMap.has(pId)) {
      statsMap.set(pId, { total: 0, selected: 0, unselected: 0, rejected: 0 });
    }
    const bucket = statsMap.get(pId);
    bucket.total++;
    if (['合适', '已录用', '已入职', '面试中'].includes(r.status)) {
      bucket.selected++;
    } else if (['不合适', '淘汰', '放弃'].includes(r.status)) {
      bucket.rejected++;
    } else {
      bucket.unselected++;
    }
  });
  window.positionRecommendationStats = statsMap;

  let filteredPositions = positions;
  if (window.positionFilters) {
    const { name, companyId, projectId, urgency, salaryRange } = window.positionFilters;
    if (name) {
      filteredPositions = filteredPositions.filter(p => p.name && p.name.toLowerCase().includes(name.toLowerCase()));
    }
    if (companyId) {
      const companyProjects = projects.filter(pr => pr.company_id === Number(companyId)).map(pr => pr.id);
      filteredPositions = filteredPositions.filter(p => companyProjects.includes(p.project_id));
    }
    if (projectId) {
      filteredPositions = filteredPositions.filter(p => p.project_id === Number(projectId));
    }
    if (urgency) {
      filteredPositions = filteredPositions.filter(p => p.urgency === urgency);
    }
    if (salaryRange) {
      filteredPositions = filteredPositions.filter(p => {
        const min = p.salary_min || 0;
        const max = p.salary_max || Infinity;
        if (salaryRange === '10K以下') return min < 10;
        if (salaryRange === '10-20K') return (min >= 10 && min <= 20) || (max >= 10 && max <= 20);
        if (salaryRange === '20-30K') return (min >= 20 && min <= 30) || (max >= 20 && max <= 30);
        if (salaryRange === '30-50K') return (min >= 30 && min <= 50) || (max >= 30 && max <= 50);
        if (salaryRange === '50K以上') return max > 50 || min >= 50;
        return true;
      });
    }
  }

  const positionTitle = document.querySelector('#position-list-title');
  if (positionTitle) {
    positionTitle.textContent = `岗位列表 (共 ${filteredPositions.length} 个)`;
  }

  const projectsById = new Map(projects.map((project) => [project.id, project]));
  positionList.innerHTML = window.hrRenderPositionTree
    ? window.hrRenderPositionTree(filteredPositions, projectsById, treeState.candidatesByPosition)
    : '';
}

window.refreshTreePage = async () => {
  const expandedPositionIds = Array.from(treeState.expandedPositions);
  treeState.candidatesByPosition.clear();
  await Promise.all(expandedPositionIds.map(pid => loadPositionCandidates(pid)));
  const page = location.pathname.split("/").pop() || "";
  if (page === "customers.html") {
    await renderCustomerTreeFromState();
  } else if (page === "projects.html") {
    await renderProjectTreeFromState();
    await renderPositionTreeFromState();
  } else if (page === "positions.html") {
    await renderPositionTreeFromState();
  }
};

window.hrToggleProjectTree = async function(projectId) {
  const projectKey = Number(projectId);
  if (!projectKey) return;
  if (treeState.expandedProjects.has(projectKey)) {
    treeState.expandedProjects.delete(projectKey);
  } else {
    treeState.expandedProjects.add(projectKey);
    await loadProjectPositions(projectKey);
  }
  if (document.querySelector('[data-project-list]')) await renderProjectTreeFromState();
  if (document.querySelector('[data-company-list]')) {
    await renderCustomerTreeFromState();
  }
};

window.hrTogglePositionTree = async function(positionId) {
  const positionKey = Number(positionId);
  if (!positionKey) return;
  if (treeState.expandedPositions.has(positionKey)) {
    treeState.expandedPositions.delete(positionKey);
  } else {
    treeState.expandedPositions.add(positionKey);
    await loadPositionCandidates(positionKey);
  }
  if (document.querySelector('[data-company-list]')) await renderCustomerTreeFromState();
  if (document.querySelector('[data-project-list]')) await renderProjectTreeFromState();
  if (document.querySelector('[data-position-list]')) await renderPositionTreeFromState();
};

window.hrToggleCompanyTree = async function(companyId) {
  const companyKey = Number(companyId);
  if (!companyKey) return;
  if (treeState.expandedCompanies.has(companyKey)) {
    treeState.expandedCompanies.delete(companyKey);
  } else {
    treeState.expandedCompanies.add(companyKey);
    await loadCompanyProjects(companyKey);
  }
  if (document.querySelector('[data-company-list]')) {
    await renderCustomerTreeFromState();
  }
};

function getNavVisibility(role, permissions = null) {
  const permissionSet = permissions ? new Set(permissions) : null;
  if (permissionSet?.has("all")) {
    return new Set(navItems.map(({ href }) => href));
  }
  if (permissionSet?.size) {
    const allowed = new Set(["dashboard.html"]);
    navItems.forEach(({ href }) => {
      const key = href.replace(".html", "");
      if (permissionSet.has(`page:${key}`)) allowed.add(href);
    });
    return allowed;
  }
  const normalized = String(role || "").toLowerCase();
  if (String(role || "").includes("超级") || normalized.includes("admin")) {
    return new Set(navItems.map(({ href }) => href));
  }
  if (String(role || "").includes("组长") || String(role || "").includes("主管") || normalized.includes("leader")) {
    return new Set([
      "dashboard.html",
      "candidates.html",
      "import.html",
      "customers.html",
      "positions.html",
      "recruit-job-publish.html",
      "recruit-job-list.html",
      "recruit-daily-tasks.html",
      "projects.html",
      "evaluations.html",
      "notifications.html",
      "statistics.html",
      "db-explorer.html",
    ]);
  }
  return new Set([
      "dashboard.html",
      "candidates.html",
      "import.html",
      "positions.html",
      "recruit-job-publish.html",
      "recruit-job-list.html",
      "recruit-daily-tasks.html",
      "projects.html",
      "evaluations.html",
      "notifications.html",
    "db-explorer.html",
  ]);
}

function shell(pageKey, body, currentUser = null, unreadCount = 0) {
  const active = (p) => p === `${pageKey}.html` || (pageKey === "index" && p === "dashboard.html");
  const visible = getNavVisibility(currentUser?.role || currentUser?.role_name || "超级管理员", currentUser?.permissions);
  const navHtml = navGroups.map((group) => {
    const items = group.items.filter(({ href }) => visible.has(href));
    if (!items.length) return "";
    return `
      <div class="nav-group">
        <div class="nav-title">${group.title}</div>
        ${items.map(({ href, label, badge, icon }) => `
          <a class="nav-item ${active(href) ? "active" : ""}" href="./${href}">
            <span class="nav-icon">${icons[icon] || icons.settings}</span>
            <span>${label}</span>
            <span class="nav-badge">${badge}</span>
          </a>`).join("")}
      </div>`;
  }).join("");
  return `
  <div class="app-shell">
    <aside class="sidebar">
      <div class="brand">
        <div class="brand-mark">招</div>
        <div>
          <h1>AI招聘管理平台</h1>
          <p>人力资源招聘管理系统 v3.0</p>
        </div>
      </div>
      ${navHtml}
    </aside>
    <main class="content">
      <div class="topbar">
        <div>
          <div class="crumbs">${pages[pageKey]?.crumbs || "AI招聘管理平台"}</div>
          <h2 class="page-title" style="margin-top:0;">${pages[pageKey]?.title || "AI招聘管理平台"}</h2>
          ${pages[pageKey]?.desc ? `<p class="page-lede">${pages[pageKey].desc}</p>` : ""}
        </div>
        <div class="top-actions">
          <a class="top-action top-notice" aria-label="未读通知" href="./notifications.html">
            <span class="notice-dot"></span>
            <strong>${unreadCount}</strong>
          </a>
          <div class="top-action user-chip">
            <div class="avatar"></div>
            <div><div style="font-weight:700">${currentUser?.full_name || "管理员"}</div><div class="small-muted">${currentUser?.role || "超级管理员"}</div></div>
          </div>
          <button class="top-action top-logout" data-action="logout">退出</button>
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

  // 注入选择模式样式，隐藏导航外壳
  const urlParams = new URLSearchParams(location.search);
  const isSelectMode = urlParams.get('select_mode') === '1';
  if (isSelectMode) {
    const style = document.createElement('style');
    style.innerHTML = `
      .sidebar { display: none !important; }
      .topbar { display: none !important; }
      .app-shell { min-height: 100% !important; display: block !important; }
      body { background: #fff !important; }
      .content { padding: 12px !important; margin: 0 !important; }
      .metrics { display: none !important; }
      .grid-2 { grid-template-columns: 1.2fr 1fr !important; gap: 12px !important; }
      .toolbar { display: flex !important; flex-direction: row !important; gap: 10px !important; }
      .input.wide { min-width: 0 !important; }
      .grid-2 .panel { margin-bottom: 0 !important; }
      .grid-2 .panel .list { display: flex !important; flex-direction: row !important; flex-wrap: wrap !important; gap: 12px !important; padding: 8px 12px !important; }
      .grid-2 .panel .list-item { flex: 1 1 130px !important; border: none !important; padding: 0 !important; margin: 0 !important; }
      .grid-2 .panel .list-item:not(:last-child) { border-bottom: none !important; }
      .grid-2 .panel .list-item .item-top { padding: 0 !important; }
      .table-head, .table-row {
        display: grid !important;
        grid-template-columns: 48px 1.5fr 1fr 1fr 1fr 1fr 0.8fr 1fr !important;
        gap: 10px !important;
        align-items: center !important;
      }
    `;
    document.head.appendChild(style);
  }
  let currentUser = null;
  let unreadCount = 0;
  try {
    currentUser = await window.hrApi.me();
    if (currentUser) {
      window.currentUser = currentUser;
    }
    const notices = await window.hrApi.notifications({ read: false });
    unreadCount = notices.length;
  } catch (err) {
    console.warn(err);
    if (!page.endsWith("login.html")) {
      location.href = `./login.html?next=${encodeURIComponent(page)}`;
      return;
    }
  }
  const visible = getNavVisibility(currentUser?.role || currentUser?.role_name || "超级管理员", currentUser?.permissions);
  if (!visible.has(page) && page !== "dashboard.html") {
    el.innerHTML = shell("dashboard", `
      <section class="panel">
        <h3>当前角色无访问权限</h3>
        <p class="panel-sub">当前登录角色暂未开放 ${page} 对应页面，请联系管理员开通权限。</p>
        <div class="list"><div class="list-item"><div class="item-meta">权限矩阵已在页面菜单上收口，直接访问该页面也会被拦截。</div></div></div>
      </section>
    `, currentUser, unreadCount);
    bindActionButtons();
    return;
  }
  el.innerHTML = shell(key, window.__PAGE_BODY__ || "", currentUser, unreadCount);
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

function showLoadingToast(message) {
  const host = ensureToastHost();
  const toast = document.createElement("div");
  toast.textContent = message;
  toast.style.padding = "10px 12px";
  toast.style.borderRadius = "10px";
  toast.style.background = "rgba(15,23,42,0.96)";
  toast.style.color = "#fff";
  toast.style.boxShadow = "0 12px 28px rgba(0,0,0,.18)";
  toast.style.maxWidth = "320px";
  toast.style.pointerEvents = "none";
  host.appendChild(toast);
  return () => toast.remove();
}

const busyLabelByAction = {
  "open-export-modal": "加载导出数据...",
  "export-selected": "加载导出数据...",
  "confirm-export-upload": "导出中...",
  "confirm-ai-search": "匹配中...",
  "search-candidates": "筛选中...",
  "view-detail": "加载详情...",
  "toggle-details": "加载详情...",
  "confirm-search-preset-upload": "保存中...",
  "confirm-recommendation-status": "保存中...",
  "open-batch-recommend-modal": "加载岗位...",
  "confirm-candidate-edit": "保存中...",
  "confirm-candidate-create": "创建中...",
  "confirm-recommend": "推荐中...",
  "confirm-add-note": "保存中...",
  "confirm-add-tracking": "保存中...",
  "confirm-candidate-mail": "发送中...",
  "confirm-salary-tracking": "保存中...",
  "confirm-candidate-action": "处理中...",
  "confirm-import-upload": "导入中...",
  "confirm-batch-import-upload": "导入中...",
  "confirm-not-onboard": "保存中...",
  "confirm-onboard": "保存中...",
};

function escapeHtml(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function shouldShowButtonBusy(button) {
  if (button?.dataset?.treeToggle) return false;
  const action = button?.dataset?.action || "";
  if (!action || button?.dataset?.busy === "true") return false;
  if (["logout", "refresh-page"].includes(action)) return false;
  if (action.startsWith("close-") || action.startsWith("nav-")) return false;
  return Boolean(
    busyLabelByAction[action] ||
    /^(confirm|refresh|read|delete|toggle|search|export|import)-/.test(action) ||
    ["view-detail", "toggle-details", "edit-candidate", "edit-company", "edit-project", "edit-salary-record", "open-batch-recommend-modal", "open-candidate-mail-modal", "open-add-salary-modal"].includes(action)
  );
}

function getButtonBusyLabel(button, label) {
  if (label) return label;
  const action = button?.dataset?.action || "";
  if (button?.dataset?.busyLabel) return button.dataset.busyLabel;
  if (busyLabelByAction[action]) return busyLabelByAction[action];
  if (action.startsWith("refresh-")) return "刷新中...";
  if (action.startsWith("delete-")) return "删除中...";
  if (action.startsWith("toggle-")) return "处理中...";
  if (action.startsWith("read-")) return "处理中...";
  if (action.startsWith("confirm-")) return "保存中...";
  return "处理中...";
}

function setButtonBusyLabel(button, label) {
  if (!button || button.dataset?.busy !== "true") return;
  button.innerHTML = `<span class="btn-busy-spinner" aria-hidden="true"></span><span>${escapeHtml(label)}</span>`;
}

function setButtonBusy(button, busy, label) {
  if (!button || typeof button !== "object" || !("dataset" in button) || !("classList" in button)) {
    return () => {};
  }
  if (!busy) {
    if (button.dataset.busyOriginalHtml !== undefined) {
      button.innerHTML = button.dataset.busyOriginalHtml;
    }
    if (button.dataset.busyOriginalDisabled !== undefined) {
      button.disabled = button.dataset.busyOriginalDisabled === "true";
    }
    delete button.dataset.busy;
    delete button.dataset.busyOriginalHtml;
    delete button.dataset.busyOriginalDisabled;
    button.classList.remove("is-busy");
    button.removeAttribute("aria-busy");
    return () => {};
  }
  if (button.dataset.busy === "true") return () => setButtonBusy(button, false);
  button.dataset.busy = "true";
  button.dataset.busyOriginalHtml = button.innerHTML;
  button.dataset.busyOriginalDisabled = String(Boolean(button.disabled));
  button.disabled = true;
  button.classList.add("is-busy");
  button.setAttribute("aria-busy", "true");
  setButtonBusyLabel(button, getButtonBusyLabel(button, label));
  return () => setButtonBusy(button, false);
}

async function waitForBusyPaint() {
  await new Promise((resolve) => {
    if (typeof requestAnimationFrame === "function") {
      requestAnimationFrame(() => resolve());
    } else {
      setTimeout(resolve, 0);
    }
  });
}

async function withButtonBusy(button, task, label) {
  if (!button || !shouldShowButtonBusy(button)) {
    return task();
  }
  const restore = setButtonBusy(button, true, label);
  try {
    await waitForBusyPaint();
    return await task();
  } finally {
    restore();
  }
}

window.withButtonBusy = withButtonBusy;
window.setButtonBusyLabel = setButtonBusyLabel;

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

function syncAiSearchModal() {
  const modal = document.querySelector('[data-ai-search-modal]');
  if (!modal) return;
  const summary = modal.querySelector('[data-ai-search-summary]');
  const textarea = modal.querySelector('[data-ai-search-textarea]');
  const keyword = document.querySelector('[data-field="candidate-keyword"]')?.value?.trim() || "";
  const count = window.candidatesPageState?.list?.length || 0;
  if (textarea && !textarea.value.trim() && keyword) {
    textarea.value = keyword;
  }
  if (summary) {
    summary.textContent = `当前候选池：${count} 条`;
  }
}

/**
 * \u5019\u9009\u4eba\u5bfc\u51fa\u5361\u7247\uff1a\u5c55\u793a\u5e94\u7528\u4eba\u4fe1\u606f + \u4e09\u4e2a\u53ef\u7f16\u8f91\u5143\u6570\u636e\u5b57\u6bb5
 * \u6bcf\u4f4d\u5019\u9009\u4eba\u72ec\u7acb\u5361\u7247\uff0c\u652f\u6301\u5355\u72ec\u586b\u5199 \u5408\u540c\u7f16\u53f7 / \u9879\u76ee\u7f16\u53f7 / \u730e\u5934\u804c\u4f4d
 */
function renderExportCard(c) {
  const cid = String(c.id);
  const labelStyle = 'font-size:11px;font-weight:600;color:#64748b;white-space:nowrap;width:60px;flex-shrink:0;';
  const inputStyle = 'flex:1;height:28px;border:1px solid rgba(15,23,42,.12);border-radius:4px;padding:0 8px;font-size:12px;color:#1e293b;background:#fff;outline:none;';
  return `<div style="background:#fff;border:1px solid rgba(15,23,42,.09);border-radius:8px;overflow:hidden;box-shadow:0 1px 3px rgba(0,0,0,.04);">
    <!-- \u5019\u9009\u4eba\u4fe1\u606f\u884c -->
    <div style="display:flex;align-items:center;gap:10px;padding:10px 14px;background:#f8fafc;border-bottom:1px solid rgba(15,23,42,.06);">
      <div style="width:32px;height:32px;border-radius:50%;background:linear-gradient(135deg,#6366f1,#8b5cf6);display:flex;align-items:center;justify-content:center;font-size:13px;font-weight:700;color:#fff;flex-shrink:0;">${(c.name||'?').charAt(0)}</div>
      <div style="flex:1;min-width:0;">
        <div style="font-size:13px;font-weight:600;color:#1e293b;line-height:1.3;">${c.name || '--'}</div>
        <div style="font-size:11px;color:#64748b;line-height:1.3;">${c.current_title || '\u672a\u77e5\u804c\u4f4d'}${c.city ? ' \u00b7 ' + c.city : ''}</div>
      </div>
      <span style="font-size:10px;color:#94a3b8;background:#f1f5f9;border-radius:4px;padding:2px 6px;flex-shrink:0;">PDF</span>
    </div>
    <!-- \u4e09\u4e2a\u5143\u6570\u636e\u8f93\u5165\u6846 -->
    <div style="padding:10px 14px;display:flex;flex-direction:column;gap:7px;">
      <div style="display:flex;align-items:center;gap:8px;">
        <span style="${labelStyle}">\u5408\u540c\u7f16\u53f7</span>
        <input style="${inputStyle}" type="text" placeholder="\u9009\u586b\uff0c\u5982 HT-2024-001" data-export-contract-no="${cid}" />
      </div>
      <div style="display:flex;align-items:center;gap:8px;">
        <span style="${labelStyle}">\u9879\u76ee\u7f16\u53f7</span>
        <input style="${inputStyle}" type="text" placeholder="\u9009\u586b\uff0c\u5982 PRJ-2024-008" data-export-project-no="${cid}" />
      </div>
      <div style="display:flex;align-items:center;gap:8px;">
        <span style="${labelStyle}">\u730e\u5934\u804c\u4f4d</span>
        <input style="${inputStyle}" type="text" placeholder="\u9009\u586b\uff0c\u5982 \u9ad8\u7ea7\u5de5\u7a0b\u5e08" data-export-headhunter-pos="${cid}" />
      </div>
    </div>
  </div>`;
}

async function handleGlobalButton(button) {
  const text = (button.textContent || "").trim();
  const page = location.pathname.split("/").pop() || "";
  if (page === "positions.html" && [
    "open-position-modal",
    "close-position-modal",
    "confirm-position-create",
    "edit-position",
    "close-position-edit-modal",
    "confirm-position-edit",
    "delete-position",
  ].includes(button.dataset.action || "")) {
    return;
  }
  if (button.dataset.action === "logout") {
    try {
      await window.hrApi.logout();
    } catch (err) {
      console.warn(err);
    }
    localStorage.removeItem("hr_token");
    window.hrApi.token = "";
    location.href = "./login.html";
    return;
  }
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
    const position = document.querySelector('[data-company-positions]');
    if (total) total.textContent = String(companies.length);
    if (project) project.textContent = String(projects.filter(item => item.status === '招聘中').length);
    if (delivery) delivery.textContent = String(deliveries.length);
    if (position) position.textContent = String(companies.reduce((sum, company) => sum + (company.position_count || 0), 0));
  };
  const refreshProjectMetrics = async () => {
    const [projects, positions] = await Promise.all([window.hrApi.projects(), window.hrApi.positions()]);
    const total = document.querySelector('[data-project-total]');
    const active = document.querySelector('[data-project-active]');
    const finished = document.querySelector('[data-project-finished]');
    const urgent = document.querySelector('[data-project-urgent]');
    if (total) total.textContent = String(projects.length);
    if (active) active.textContent = String(projects.filter(p => p.status === '招聘中').length);
    if (finished) finished.textContent = String(projects.filter(p => p.status === '招聘完毕').length);
    if (urgent) urgent.textContent = String(positions.filter(position => position.urgency === '高').length);
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
  if (button.dataset.action === "search-add-candidates") {
    const positionId = button.dataset.id;
    if (!positionId) throw new Error('岗位 ID 缺失');
    
    let modal = document.querySelector('[data-search-candidates-modal]');
    if (!modal) {
      const div = document.createElement('div');
      div.innerHTML = `
        <div class="modal" data-search-candidates-modal style="display:none; position:fixed; inset:0; background:rgba(14,22,34,.45); z-index:2500; padding:24px;">
          <div class="panel" style="max-width:1200px; width:95%; height:90vh; margin:2vh auto; background:#fff; display:flex; flex-direction:column; padding: 0; overflow: hidden; border-radius: 12px; box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);">
            <div class="section-head" style="padding: 16px 24px; border-bottom: 1px solid rgba(15,23,42,.08); margin:0; display:flex; justify-content:space-between; align-items:center; background:#f8fafc;">
              <div>
                <h3 style="font-size:18px; font-weight:600; color:#0f172a; margin:0;">选择候选人并加入岗位</h3>
                <div class="section-sub" style="font-size:13px; color:#64748b; margin-top:2px;">搜索人才池中的候选人并一键加入当前岗位。</div>
              </div>
              <div>
                <button class="btn" data-action="close-search-candidates-modal" style="padding: 8px 16px; font-size:14px; font-weight:500; border-radius:6px; cursor:pointer;">关闭窗口</button>
              </div>
            </div>
            <div style="flex:1; width:100%; height:100%; position:relative; overflow:hidden;">
              <iframe data-search-candidates-iframe style="width:100%; height:100%; border:none;" src=""></iframe>
            </div>
          </div>
        </div>
      `;
      document.body.appendChild(div.firstElementChild);
      modal = document.querySelector('[data-search-candidates-modal]');
    }
    
    const iframe = modal.querySelector('[data-search-candidates-iframe]');
    if (iframe) {
      const base = location.pathname.replace(/\/[^\/]+$/, '');
      iframe.src = `${base}/candidates.html?select_mode=1&position_id=${positionId}`;
    }
    
    modal.style.display = 'block';
    return;
  }
  if (button.dataset.action === "close-search-candidates-modal") {
    const modal = document.querySelector('[data-search-candidates-modal]');
    if (modal) modal.style.display = 'none';
    return;
  }
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
                  <div class="avatar-sm" style="display:flex; align-items:center; justify-content:center; background:#f3f4f6;">${i.status === '锁定' ? '<svg viewBox="0 0 24 24" width="16" height="16" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round" style="color:#f59e0b;"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect><path d="M7 11V7a5 5 0 0 1 10 0v4"></path></svg>' : '<svg viewBox="0 0 24 24" width="16" height="16" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round" style="color:#10b981;"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect><path d="M7 11V7a5 5 0 0 1 9.9-1"></path></svg>'}</div>
                  <div>
                    <strong>${i.name}</strong>
                  </div>
                </div>
              </div>
              <div>${i.current_title || '--'}</div>
              <div>${i.city || '--'}</div>
              <div class="mono">${i.expected_salary || '--'}</div>
              <div>${i.source || '--'}</div>
              <div>${i.age ? i.age + '岁' : '--'}</div>
              <div>
                <div class="table-actions">
                  <button class="btn-sm primary" data-action="view-detail" data-id="${i.record_key || `candidate:${i.id}`}" data-row-key="${i.record_key || `candidate:${i.id}`}" data-candidate-key="${i.record_key || `candidate:${i.id}`}" data-title="${i.name}">详情</button>
                </div>
              </div>
            </div>
          `).join('') || `<div class="table-row"><div><input type="checkbox" aria-label="候选人空状态" disabled /></div><div><div class="row-title"><div class="avatar-sm"></div><div><strong>等待真实候选人数据</strong><div class="row-sub">候选人列表来自接口返回的数据库记录。</div></div></div></div><div>--</div><div>--</div><div class="mono">--</div><div>--</div><div>--</div><div>--</div></div>`;
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
  if (button.dataset.action === "open-ai-search-modal") {
    const modal = document.querySelector('[data-ai-search-modal]');
    if (modal) modal.style.display = 'block';
    syncAiSearchModal();
    return;
  }
  if (button.dataset.action === "close-ai-search-modal") {
    const modal = document.querySelector('[data-ai-search-modal]');
    if (modal) modal.style.display = 'none';
    return;
  }
  if (button.dataset.action === "confirm-ai-search") {
    const modal = document.querySelector('[data-ai-search-modal]');
    const textarea = modal?.querySelector('[data-ai-search-textarea]');
    const jobDescription = textarea?.value?.trim() || "";
    if (!jobDescription) throw new Error("请输入岗位描述");
    const list = window.candidatesPageState?.list || [];
    if (!list.length) throw new Error("当前筛选条件下没有可检索的候选人");
    const recordKeys = list.map(item => String(item.record_key || `candidate:${item.id}`));
    const hideLoading = showLoadingToast("AI深度匹配中...");
    try {
      await new Promise(resolve => requestAnimationFrame(() => resolve()));
      const result = await window.hrApi.candidateAiSearch({
        job_description: jobDescription,
        record_keys: recordKeys,
      });
      if (!result?.candidate) throw new Error("AI 未能返回候选人结果");
      if (window.candidatesPageState) {
        window.candidatesPageState.list = [result.candidate];
        window.candidatesPageState.currentPage = 1;
        window.candidatesPageState.renderOnly();
      }
      if (modal) modal.style.display = 'none';
      showToast(result.reason ? `AI检索命中：${result.candidate.name} · ${result.reason}` : `AI检索命中：${result.candidate.name}`);
    } finally {
      hideLoading();
    }
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
    const candidateList = document.querySelector('[data-export-candidates-list]');
    const history = document.querySelector('[data-export-history-modal]');
    if (candidateList) {
      candidateList.innerHTML = '<div class="list-item"><div class="item-meta">正在加载可导出的候选人...</div></div>';
    }
    if (history) {
      history.innerHTML = '<div class="list-item"><div class="item-meta">正在加载导出历史...</div></div>';
    }
    const [candidates, records] = await Promise.all([
      window.hrApi.candidates(),
      window.hrApi.exportRecords(),
    ]);
    // 渲染候选人卡片列表（全部）
    if (candidateList) {
      modal.dataset.exportIds = JSON.stringify(candidates.map(c => String(c.id)));
      candidateList.innerHTML = candidates.length
        ? candidates.map(c => renderExportCard(c)).join('')
        : '<div style="color:#94a3b8;font-size:13px;padding:12px;text-align:center;">暂无候选人数据</div>';
    }
    // 渲染导出历史
    if (history) history.innerHTML = records.slice(0, 5).map(r => `<div class="list-item"><div class="item-top"><div><div class="item-title">${r.file_name}</div><div class="item-meta">${r.company_name || ''} · ${r.project_name || ''}</div><div class="item-meta mono">${r.format} · ${r.created_at}</div></div><span class="chip success">PDF</span></div></div>`).join('') || '<div class="list-item"><div class="item-meta">暂无导出记录</div></div>';
    return;
  }
  if (button.dataset.action === "close-export-modal") {
    const modal = document.querySelector('[data-export-modal]');
    if (modal) modal.style.display = 'none';
    return;
  }
  if (button.dataset.action === "confirm-export-upload") {
    const modal = document.querySelector('[data-export-modal]');
    let exportIds = [];
    try { exportIds = JSON.parse(modal?.dataset.exportIds || '[]'); } catch(e) {}
    if (exportIds.length === 0) throw new Error('没有可导出的候选人，请先选择或勾选候选人');

    const candidates = await window.hrApi.candidates();
    const exportList = exportIds.map(id => candidates.find(c => String(c.id) === String(id))).filter(Boolean);
    if (exportList.length === 0) throw new Error('未找到对应的候选人信息');

    // 批量逐一导出，每个候选人生成一份 PDF
    let successCount = 0;
    for (const [index, candidate] of exportList.entries()) {
      setButtonBusyLabel(button, `导出中 ${index + 1}/${exportList.length}...`);
      // 从对应卡片的输入框读取三个元数据字段
      const cid = String(candidate.id);
      const contractNo = document.querySelector(`[data-export-contract-no="${cid}"]`)?.value?.trim() || '';
      const projectNo = document.querySelector(`[data-export-project-no="${cid}"]`)?.value?.trim() || '';
      const headhunterPos = document.querySelector(`[data-export-headhunter-pos="${cid}"]`)?.value?.trim() || '';
      try {
        const exportRecord = await window.hrApi.createExportRecord({
          candidate_id: candidate.id,
          candidate_name: candidate.name || '',
          company_name: '',
          project_name: '',
          position_name: candidate.current_title || '',
          format: 'PDF',
          watermarked: true,
          exported_by: 'admin',
          file_name: `${candidate.name || '候选人'}-简历报告.pdf`,
          file_path: '',
          contract_no: contractNo,
          project_no: projectNo,
          headhunter_position: headhunterPos,
        });
        // 自动触发物理下载
        if (exportRecord && exportRecord.file_path) {
          await new Promise(resolve => setTimeout(resolve, 500));
          const link = document.createElement('a');
          link.href = exportRecord.file_path;
          link.download = exportRecord.file_name;
          document.body.appendChild(link);
          link.click();
          document.body.removeChild(link);
        }
        await window.hrApi.createNotification({
          user: 'admin',
          title: `简历已导出：${candidate.name}`,
          type: '导出通知',
          content: `${candidate.name} 的简历已导出为 PDF 格式`,
          target_path: './candidates.html',
          read: false,
        });
        successCount++;
      } catch(err) {
        console.error(`导出 ${candidate.name} 失败：`, err);
      }
    }
    if (modal) modal.style.display = 'none';
    showToast(exportList.length === 1
      ? `已导出：${exportList[0].name} 的 PDF 简历`
      : `批量导出完成：共 ${successCount}/${exportList.length} 份 PDF 简历`);
    return;
  }
  if (button.dataset.action === "export-selected") {
    const checkedBoxes = Array.from(document.querySelectorAll('.table-card .table-row input[type="checkbox"]:checked'));
    const checkedIds = checkedBoxes.map(cb => String(cb.dataset.id)).filter(Boolean);
    
    if (checkedIds.length === 0) {
      showToast("请先勾选需要导出的候选人简历");
      return;
    }

    const modal = document.querySelector('[data-export-modal]');
    if (modal) modal.style.display = 'block';
    const candidateList = document.querySelector('[data-export-candidates-list]');
    const history = document.querySelector('[data-export-history-modal]');
    if (candidateList) {
      candidateList.innerHTML = '<div class="list-item"><div class="item-meta">正在加载选中候选人...</div></div>';
    }
    if (history) {
      history.innerHTML = '<div class="list-item"><div class="item-meta">正在加载导出历史...</div></div>';
    }
    
    const [candidates, records] = await Promise.all([
      window.hrApi.candidates(),
      window.hrApi.exportRecords(),
    ]);
    
    const filteredCandidates = candidates.filter(c => checkedIds.includes(String(c.id)));
    
    // 渲染勾选的候选人卡片
    if (candidateList) {
      modal.dataset.exportIds = JSON.stringify(filteredCandidates.map(c => String(c.id)));
      candidateList.innerHTML = filteredCandidates.length
        ? filteredCandidates.map(c => renderExportCard(c)).join('')
        : '<div style="color:#94a3b8;font-size:13px;padding:12px;text-align:center;">未匹配到候选人数据</div>';
    }
    // 渲染导出历史
    if (history) history.innerHTML = records.slice(0, 5).map(r => `<div class="list-item"><div class="item-top"><div><div class="item-title">${r.file_name}</div><div class="item-meta">${r.company_name || ''} · ${r.project_name || ''}</div><div class="item-meta mono">${r.format} · ${r.created_at}</div></div><span class="chip success">PDF</span></div></div>`).join('') || '<div class="list-item"><div class="item-meta">暂无导出记录</div></div>';
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
  if (button.dataset.action === "toggle-details") {
    const candidateKey = button.dataset.candidateKey || button.dataset.rowKey || button.dataset.id || "";
    const wrapper = document.getElementById(`details-wrapper-${candidateKey}`);
    const details = document.getElementById(`details-${candidateKey}`);
    if (!wrapper || !details) return;
    
    const isOpen = wrapper.style.gridTemplateRows === '1fr';
    
    if (!isOpen) {
        wrapper.style.gridTemplateRows = '1fr';
        details.style.padding = '24px';
        details.style.opacity = '1';
        details.style.borderTopColor = '#e2e8f0';
        const icon = button.querySelector('svg');
        if (icon) icon.style.transform = 'rotate(180deg)';
        if (!details.dataset.fetched) {
            const resolved = candidateKey ? await window.hrApi.candidate(candidateKey) : null;
            if (resolved && window.fetchCandidatePanels) {
                await window.fetchCandidatePanels(resolved.id, details);
                details.dataset.candidateId = String(resolved.id);
            }
            details.dataset.fetched = 'true';
        }
    } else {
        wrapper.style.gridTemplateRows = '0fr';
        details.style.padding = '0 24px';
        details.style.opacity = '0';
        details.style.borderTopColor = 'transparent';
        const icon = button.querySelector('svg');
        if (icon) icon.style.transform = 'rotate(0deg)';
    }
    return;
  }
  
  if (button.dataset.action === "view-detail") {
    if (!document.querySelector('[data-candidate-detail-modal]')) {
      try {
        const res = await fetch('candidates.html');
        if (res.ok) {
          const htmlText = await res.text();
          const parser = new DOMParser();
          const doc = parser.parseFromString(htmlText, 'text/html');
          const modalSelectors = [
            '[data-candidate-detail-modal]',
            '[data-candidate-edit-modal]',
            '[data-candidate-mail-modal]',
            '[data-add-note-modal]',
            '[data-add-tracking-modal]',
            '[data-salary-tracking-modal]',
            '[data-candidate-followup-modal]'
          ];
          modalSelectors.forEach(sel => {
            if (!document.querySelector(sel)) {
              const modal = doc.querySelector(sel);
              if (modal) {
                document.body.appendChild(modal);
              }
            }
          });
        }
      } catch (err) {
        console.error("动态加载候选人详情 Modal 失败:", err);
      }
    }
    const title = button.dataset.title || text || "详情";
    const candidateKey = button.dataset.candidateKey || button.dataset.rowKey || button.dataset.id || '';
    const modal = document.querySelector('[data-candidate-detail-modal]');
    if (!modal) throw new Error("无法初始化详情窗口");
    const item = candidateKey ? await window.hrApi.candidate(candidateKey) : null;
    modal.style.display = 'block';
    const resolvedId = item?.id != null ? String(item.id) : '';
    document.body.dataset.candidateId = resolvedId;
    document.querySelector('[data-candidate-detail-title]').textContent = `${item?.name || title} 详情`;
    document.querySelector('[data-candidate-detail-sub]').textContent = `${item?.source || '来源未知'} · ${item?.status || '状态未知'}`;
    const set = (sel, val) => { const el = document.querySelector(sel); if (el) el.textContent = val || '--'; };
    set('[data-candidate-detail-name]', item?.name);
    set('[data-candidate-detail-gender]', item?.gender);
    set('[data-candidate-detail-age]', item?.age);
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
    const projectsContainer = document.querySelector('[data-candidate-detail-projects]');
    if (projectsContainer) {
      projectsContainer.innerHTML = '<div class="list-item"><div class="item-meta">加载中...</div></div>';
    }
    (async () => {
      try {
        const resolvedIdNum = item?.id != null ? Number(item.id) : null;
        if (resolvedIdNum) {
          const recs = await window.hrApi.recommendations({ candidate_id: resolvedIdNum });
          const [posList, projList, compList] = await Promise.all([
            window.hrApi.positions(),
            window.hrApi.projects(),
            window.hrApi.companies()
          ]);
          const posMap = new Map(posList.map(p => [p.id, p]));
          const projMap = new Map(projList.map(p => [p.id, p]));
          const compMap = new Map(compList.map(c => [c.id, c]));
          if (projectsContainer) {
            projectsContainer.innerHTML = recs.map(r => {
              const pos = posMap.get(r.position_id);
              const proj = pos ? projMap.get(pos.project_id) : null;
              const comp = proj ? compMap.get(proj.company_id) : null;
              const compName = comp?.name || '未知客户';
              const projName = proj?.name || '未知项目';
              const posName = pos?.name || '未知岗位';
              const statusText = r.status || '待推荐';
              const feedbackText = r.feedback || r.customer_comment || '暂无评语';
              return `
                <div class="list-item">
                  <div class="item-top">
                    <div>
                      <div class="item-title">${compName} · ${projName}</div>
                      <div class="item-meta">岗位：${posName} | 反馈：${feedbackText}</div>
                    </div>
                    <span class="chip primary">${statusText}</span>
                  </div>
                </div>
              `;
            }).join('') || '<div class="list-item"><div class="item-meta">暂无推荐项目记录</div></div>';
          }
        } else {
          if (projectsContainer) {
            projectsContainer.innerHTML = '<div class="list-item"><div class="item-meta">暂无推荐项目记录</div></div>';
          }
        }
      } catch (err) {
        console.warn("Failed to load recommendation history:", err);
        if (projectsContainer) {
          projectsContainer.innerHTML = '<div class="list-item"><div class="item-meta">加载推荐历史失败</div></div>';
        }
      }
    })();
    const openAddNoteBtn = document.querySelector('[data-candidate-detail-modal] [data-action="open-add-note-modal"]');
    if (openAddNoteBtn) {
      openAddNoteBtn.dataset.id = resolvedId;
    }
    const notesContainer = document.querySelector('[data-candidate-detail-notes]');
    if (notesContainer) {
      notesContainer.innerHTML = '<div class="list-item"><div class="item-meta">加载中...</div></div>';
    }
    (async () => {
      try {
        const resolvedIdNum = item?.id != null ? Number(item.id) : null;
        if (resolvedIdNum) {
          const notes = await window.hrApi.candidateNotes({ candidate_id: resolvedIdNum });
          const formatTime = (dtStr) => {
            if (!dtStr) return '--';
            try {
              const d = new Date(dtStr);
              if (isNaN(d.getTime())) return dtStr;
              const pad = (n) => String(n).padStart(2, '0');
              return `${d.getFullYear()}-${pad(d.getMonth()+1)}-${pad(d.getDate())} ${pad(d.getHours())}:${pad(d.getMinutes())}`;
            } catch (e) {
              return dtStr;
            }
          };
          if (notesContainer) {
            notesContainer.innerHTML = notes.map(n => `
              <div class="list-item" style="background:#f8fafc; border:1px solid #f1f5f9; border-radius:8px; padding:12px 16px; box-shadow:none; align-items: stretch; flex-direction: column; gap: 4px;">
                <div style="font-size:13px; color:#334155; line-height:1.5; white-space:pre-wrap;">${n.content}</div>
                <div style="font-size:11px; color:#94a3b8;">${n.operator} · ${formatTime(n.created_at)}</div>
              </div>
            `).join('') || '<div class="list-item"><div class="item-meta">暂无备注记录</div></div>';
          }
        } else {
          if (notesContainer) {
            notesContainer.innerHTML = '<div class="list-item"><div class="item-meta">暂无备注记录</div></div>';
          }
        }
      } catch (err) {
        console.warn("Failed to load notes history:", err);
        if (notesContainer) {
          notesContainer.innerHTML = '<div class="list-item"><div class="item-meta">加载备注历史失败</div></div>';
        }
      }
    })();

    // 渲染候选人跟踪表
    const openAddTrackingBtn = document.querySelector('[data-candidate-detail-modal] [data-action="open-add-tracking-modal"]');
    if (openAddTrackingBtn) {
      openAddTrackingBtn.dataset.id = resolvedId;
    }
    const trackingTbody = document.getElementById('candidate-detail-tracking-tbody');
    if (trackingTbody) {
      trackingTbody.innerHTML = '<tr><td style="padding:20px; text-align:center; color:#94a3b8;" colspan="13">加载中...</td></tr>';
    }
    (async () => {
      try {
        const resolvedIdNum = item?.id != null ? Number(item.id) : null;
        if (resolvedIdNum) {
          const events = await window.hrApi.candidateTrackingEvents({ candidate_id: resolvedIdNum });
          if (trackingTbody) {
            if (events.length === 0) {
              trackingTbody.innerHTML = '<tr><td style="padding:20px; text-align:center; color:#94a3b8;" colspan="13">暂无面试跟踪记录</td></tr>';
            } else {
              trackingTbody.innerHTML = events.map(evt => {
                // 面试轮次圆形微标
                const roundName = evt.interview_round || '面试';
                const roundShort = roundName.includes('初筛') ? '初筛' : roundName.replace('第', '').replace('轮', '') + '轮';
                const roundHtml = `<div style="background:#eceafc; color:#8b5cf6; width:36px; height:36px; border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:11px; font-weight:600; margin:0 auto; white-space:nowrap;">${roundShort}</div>`;
                
                // 初筛结果徽标
                let screeningHtml = '-';
                if (evt.screening_result === '通过') {
                  screeningHtml = `<div style="background:#10b981; color:#fff; width:36px; height:36px; border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:11px; font-weight:600; margin:0 auto; white-space:nowrap;">通过</div>`;
                } else if (evt.screening_result === '未通过') {
                  screeningHtml = `<div style="background:#ef4444; color:#fff; width:36px; height:36px; border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:11px; font-weight:600; margin:0 auto; white-space:nowrap;">未过</div>`;
                }

                // 入职状态胶囊
                const empStatus = evt.employment_status || '待设置';
                const empHtml = `<span style="border:1px solid #e2e8f0; border-radius:12px; padding:2px 8px; color:#94a3b8; font-size:11px; background:#fafafa; white-space:nowrap;">${empStatus}</span>`;

                // 备注说明
                const noteContent = evt.note || '-';

                // 操作栏：发送邮件（纯SVG图标）+ 编辑（纯SVG图标）+ 删除（纯SVG图标）并列
                const mailBtn = `<button class="btn-sm" data-action="open-candidate-mail-modal" data-candidate-id="${resolvedId}" title="发送邮件" style="background-color:#06b6d4; border-color:#06b6d4; color:#fff; border-radius:50%; width:24px; height:24px; padding:0; display:inline-flex; align-items:center; justify-content:center; cursor:pointer; border:none; transition: all 0.2s; box-shadow: 0 1px 3px rgba(0,0,0,0.1);"><svg viewBox="0 0 24 24" width="12" height="12" stroke="currentColor" stroke-width="2.5" fill="none"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"></path><polyline points="22,6 12,13 2,6"></polyline></svg></button>`;
                const editBtn = `<button class="btn-sm" data-action="edit-tracking-event" data-id="${evt.id}" data-candidate-id="${resolvedId}" title="编辑记录" style="background-color:#3b82f6; border-color:#3b82f6; color:#fff; border-radius:50%; width:24px; height:24px; padding:0; display:inline-flex; align-items:center; justify-content:center; cursor:pointer; border:none; transition: all 0.2s; box-shadow: 0 1px 3px rgba(0,0,0,0.1);"><svg viewBox="0 0 24 24" width="12" height="12" stroke="currentColor" stroke-width="2.5" fill="none"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path><path d="M18.5 2.5a2.121 2.121 0 1 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path></svg></button>`;
                const deleteBtn = `<button class="btn-sm" data-action="delete-tracking-event" data-id="${evt.id}" data-candidate-id="${resolvedId}" title="删除记录" style="background-color:#ef4444; border-color:#ef4444; color:#fff; border-radius:50%; width:24px; height:24px; padding:0; display:inline-flex; align-items:center; justify-content:center; cursor:pointer; border:none; transition: all 0.2s; box-shadow: 0 1px 3px rgba(0,0,0,0.1);"><svg viewBox="0 0 24 24" width="12" height="12" stroke="currentColor" stroke-width="2.5" fill="none"><polyline points="3 6 5 6 21 6"></polyline><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path><line x1="10" y1="11" x2="10" y2="17"></line><line x1="14" y1="11" x2="14" y2="17"></line></svg></button>`;
                
                const actionHtml = `<div style="display:flex; gap:6px; align-items:center; justify-content:flex-start;">${mailBtn}${editBtn}${deleteBtn}</div>`;

                return `
                  <tr style="border-bottom:1px solid #f1f5f9; hover:background-color:#fafafa;">
                    <td style="padding:10px 8px; text-align:center;">${roundHtml}</td>
                    <td style="padding:10px 8px; text-align:center;">${screeningHtml}</td>
                    <td style="padding:10px 8px; white-space:nowrap;">${evt.interview_date || '-'}</td>
                    <td style="padding:10px 8px;">${evt.interviewer || '-'}</td>
                    <td style="padding:10px 8px; max-width:140px; overflow:hidden; text-overflow:ellipsis; white-space:nowrap;" title="${evt.interview_location || ''}">${evt.interview_location || '-'}</td>
                    <td style="padding:10px 8px; max-width:140px; overflow:hidden; text-overflow:ellipsis; white-space:nowrap;" title="${evt.interview_requirements || ''}">${evt.interview_requirements || '-'}</td>
                    <td style="padding:10px 8px;">${evt.interview_contact || '-'}</td>
                    <td style="padding:10px 8px;">${evt.interview_result || '-'}</td>
                    <td style="padding:10px 8px;"><span class="chip success" style="font-size:10px; padding:2px 6px;">${evt.status || '已完成'}</span></td>
                    <td style="padding:10px 8px; max-width:200px; word-break:break-all;">${noteContent}</td>
                    <td style="padding:10px 8px; text-align:center;">${empHtml}</td>
                    <td style="padding:10px 8px;">${evt.operator || '-'}</td>
                    <td style="padding:10px 8px;">${actionHtml}</td>
                  </tr>
                `;
              }).join('');
            }
          }
        }
      } catch (err) {
        console.warn("Failed to load tracking events history:", err);
        if (trackingTbody) {
          trackingTbody.innerHTML = '<tr><td style="padding:20px; text-align:center; color:#ef4444;" colspan="13">加载面试记录失败</td></tr>';
        }
      }
    })();

    // 渲染薪资/福利/入职条件跟踪表
    const openAddSalaryBtn = document.querySelector('[data-candidate-detail-modal] [data-action="open-add-salary-modal"]');
    if (openAddSalaryBtn) {
      openAddSalaryBtn.dataset.id = resolvedId;
    }
    const salaryTbody = document.getElementById('candidate-detail-salary-tbody');
    if (salaryTbody) {
      salaryTbody.innerHTML = '<tr><td style="padding:20px; text-align:center; color:#94a3b8;" colspan="10">加载中...</td></tr>';
    }
    (async () => {
      try {
        const resolvedIdNum = item?.id != null ? Number(item.id) : null;
        if (resolvedIdNum) {
          const records = await window.hrApi.salaryRecords({ candidate_id: resolvedIdNum });
          if (salaryTbody) {
            if (records.length === 0) {
              salaryTbody.innerHTML = '<tr><td style="padding:20px; text-align:center; color:#94a3b8;" colspan="10">暂无薪资/福利/入职条件跟踪记录</td></tr>';
            } else {
              salaryTbody.innerHTML = records.map(rec => {
                const formatTime = (dtStr) => {
                  if (!dtStr) return '--';
                  try {
                    const d = new Date(dtStr);
                    if (isNaN(d.getTime())) return dtStr;
                    const pad = (n) => String(n).padStart(2, '0');
                    return `${d.getFullYear()}-${pad(d.getMonth()+1)}-${pad(d.getDate())} ${pad(d.getHours())}:${pad(d.getMinutes())}`;
                  } catch (e) {
                    return dtStr;
                  }
                };

                // 操作按钮：编辑（铅笔）+ 删除（垃圾桶）
                const editBtn = `<button class="btn-sm" data-action="edit-salary-record" data-id="${rec.id}" data-candidate-id="${resolvedId}" title="编辑记录" style="background-color:#3b82f6; border-color:#3b82f6; color:#fff; border-radius:50%; width:24px; height:24px; padding:0; display:inline-flex; align-items:center; justify-content:center; cursor:pointer; border:none; transition: all 0.2s; box-shadow: 0 1px 3px rgba(0,0,0,0.1);"><svg viewBox="0 0 24 24" width="12" height="12" stroke="currentColor" stroke-width="2.5" fill="none"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path><path d="M18.5 2.5a2.121 2.121 0 1 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path></svg></button>`;
                const deleteBtn = `<button class="btn-sm" data-action="delete-salary-record" data-id="${rec.id}" data-candidate-id="${resolvedId}" title="删除记录" style="background-color:#ef4444; border-color:#ef4444; color:#fff; border-radius:50%; width:24px; height:24px; padding:0; display:inline-flex; align-items:center; justify-content:center; cursor:pointer; border:none; transition: all 0.2s; box-shadow: 0 1px 3px rgba(0,0,0,0.1);"><svg viewBox="0 0 24 24" width="12" height="12" stroke="currentColor" stroke-width="2.5" fill="none"><polyline points="3 6 5 6 21 6"></polyline><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path><line x1="10" y1="11" x2="10" y2="17"></line><line x1="14" y1="11" x2="14" y2="17"></line></svg></button>`;
                const actionHtml = `<div style="display:flex; gap:6px; align-items:center; justify-content:flex-start;">${editBtn}${deleteBtn}</div>`;

                // 是否接受状态徽标
                let acceptHtml = '-';
                if (rec.candidate_accepted === '接受') {
                  acceptHtml = `<span style="background-color:#e6fffa; color:#047481; border:1px solid #b2f5ea; border-radius:4px; padding:2px 8px; font-size:11px; font-weight:600; white-space:nowrap;">接受</span>`;
                } else if (rec.candidate_accepted === '不接受') {
                  acceptHtml = `<span style="background-color:#fff5f5; color:#c53030; border:1px solid #feb2b2; border-radius:4px; padding:2px 8px; font-size:11px; font-weight:600; white-space:nowrap;">不接受</span>`;
                }

                // 关联面试轮次徽标
                const roundName = rec.interview_round || '-';
                const roundHtml = roundName !== '-' ? `<span style="background-color:#eceafc; color:#8b5cf6; border-radius:12px; padding:2px 8px; font-size:11px; font-weight:600; white-space:nowrap;">${roundName}</span>` : '-';

                return `
                  <tr style="border-bottom:1px solid #f1f5f9; hover:background-color:#fafafa;">
                    <td style="padding:10px 8px; text-align:center;">${roundHtml}</td>
                    <td style="padding:10px 8px; white-space:nowrap;">${rec.position_name || '-'}</td>
                    <td style="padding:10px 8px; white-space:nowrap;">${rec.company_name || '-'}</td>
                    <td style="padding:10px 8px; color:#8b5cf6; font-weight:600;">${rec.agreed_salary || '-'}</td>
                    <td style="padding:10px 8px; max-width:180px; overflow:hidden; text-overflow:ellipsis; white-space:nowrap;" title="${rec.welfare_desc || ''}">${rec.welfare_desc || '-'}</td>
                    <td style="padding:10px 8px; max-width:180px; overflow:hidden; text-overflow:ellipsis; white-space:nowrap;" title="${rec.onboard_cond || ''}">${rec.onboard_cond || '-'}</td>
                    <td style="padding:10px 8px; text-align:center;">${acceptHtml}</td>
                    <td style="padding:10px 8px; white-space:nowrap;">${formatTime(rec.created_at)}</td>
                    <td style="padding:10px 8px;">${rec.operator || '-'}</td>
                    <td style="padding:10px 8px;">${actionHtml}</td>
                  </tr>
                `;
              }).join('');
            }
          }
        }
      } catch (err) {
        console.warn("Failed to load salary tracking records:", err);
      }
    })();

    // 渲染并初始化入职状态卡片 (常驻详情弹窗最下方)
    (async () => {
      try {
        const resolvedIdNum = item?.id != null ? Number(item.id) : null;
        if (resolvedIdNum) {
          const panel = document.querySelector('[data-detail-employment-panel]');
          if (panel) {
            panel.dataset.candidateId = String(resolvedIdNum);
            // 1. 获取最新一条薪资记录以带出公司与岗位
            const salaryList = await window.hrApi.salaryRecords({ candidate_id: resolvedIdNum });
            const latestSalary = salaryList && salaryList[0];
            const salaryPos = latestSalary?.position_name || '--';
            const salaryComp = latestSalary?.company_name || '--';
            
            // 2. 异步获取质保天数
            let warrantyDays = 60; // 默认 60 天
            try {
              const rules = await window.hrApi.warrantyRules();
              const rule = rules.find(r => r.scope === '入职质保期');
              if (rule) {
                warrantyDays = (rule.months || 2) * 30;
              }
            } catch (err) {
              console.warn("Failed to get warranty rules:", err);
            }
            panel.dataset.warrantyDays = String(warrantyDays);
            panel.dataset.salaryPos = salaryPos;
            panel.dataset.salaryComp = salaryComp;
            
            // 3. 定义开关切换 UI 处理函数
            window.setEmploymentPanelState = function(state) {
              panel.dataset.onboardState = state;
              const ball = document.getElementById('employment-toggle-ball');
              const label = document.getElementById('employment-toggle-label');
              const txtLeft = document.getElementById('employment-toggle-text-left');
              const txtRight = document.getElementById('employment-toggle-text-right');
              const notOnboardCard = document.getElementById('employment-not-onboard-card');
              const onboardCard = document.getElementById('employment-onboard-card');
              
              if (state === 'onboard') {
                if (ball) ball.style.transform = 'translateX(22px)';
                if (label) label.style.background = '#00c497';
                if (txtLeft) { txtLeft.style.color = '#94a3b8'; }
                if (txtRight) { txtRight.style.color = '#00c497'; }
                if (notOnboardCard) notOnboardCard.style.display = 'none';
                if (onboardCard) onboardCard.style.display = 'block';
              } else {
                if (ball) ball.style.transform = 'translateX(0)';
                if (label) label.style.background = '#8b5cf6';
                if (txtLeft) { txtLeft.style.color = '#8b5cf6'; }
                if (txtRight) { txtRight.style.color = '#94a3b8'; }
                if (notOnboardCard) notOnboardCard.style.display = 'block';
                if (onboardCard) onboardCard.style.display = 'none';
              }
            };
            
            // 绑定 Toggle 开关点击事件 (滑到“已入职”直接生效，滑到“未入职”则进入编辑备注态)
            const toggleLabel = document.getElementById('employment-toggle-label');
            if (toggleLabel) {
              toggleLabel.onclick = function() {
                const nextState = panel.dataset.onboardState === 'onboard' ? 'not-onboard' : 'onboard';
                
                if (nextState === 'onboard') {
                  const position_name = panel.dataset.salaryPos;
                  const company_name = panel.dataset.salaryComp;
                  if (position_name === '--' || company_name === '--') {
                    showToast('当前候选人缺少关联岗位或客户公司，请先在薪资/福利/入职条件跟踪表中录入约定薪资记录！');
                    return;
                  }
                  
                  const todayStr = new Date().toISOString().slice(0, 10);
                  const payload = {
                    candidate_id: Number(resolvedIdNum),
                    status: "已入职",
                    company_name: company_name,
                    position_name: position_name,
                    onboard_date: new Date(todayStr).toISOString(),
                    note: "确认入职"
                  };
                  
                  window.hrApi.createEmploymentRecord(payload).then(async (record) => {
                    showToast(`入职状态切换为已入职，已直接生效！`);
                    
                    document.getElementById('employment-display-onboard-date').textContent = todayStr;
                    document.getElementById('employment-display-position').textContent = position_name;
                    document.getElementById('employment-display-position').title = position_name;
                    document.getElementById('employment-display-company').textContent = company_name;
                    document.getElementById('employment-display-company').title = company_name;
                    
                    const warrantyEl = document.getElementById('employment-display-warranty');
                    if (warrantyEl) {
                      warrantyEl.textContent = "质保在职";
                      warrantyEl.style.backgroundColor = 'rgba(255,255,255,0.25)';
                      warrantyEl.style.color = '#fff';
                    }
                    
                    window.setEmploymentPanelState('onboard');

                    // 联动刷新候选人生命周期
                    const lifecycle = document.querySelector(`[data-lifecycle-events="${resolvedIdNum}"]`);
                    if (lifecycle) {
                      const container = lifecycle.closest('[id^="details-"]');
                      if (container) {
                        await window.fetchCandidatePanels(resolvedIdNum, container);
                      }
                    }
                    
                    // 联动刷新详情面板
                    const detailModal = document.querySelector('[data-candidate-detail-modal]');
                    if (detailModal && detailModal.dataset.candidateId === String(resolvedIdNum)) {
                      const fakeBtn = document.createElement("button");
                      fakeBtn.dataset.action = "view-detail";
                      fakeBtn.dataset.id = String(resolvedIdNum);
                      handleGlobalButton(fakeBtn).catch(err => console.warn(err));
                    }
                  }).catch(err => {
                    showToast('入职状态变更失败：' + err.message);
                  });
                } else {
                  // 滑到未入职时，进入编辑输入态
                  window.setEmploymentPanelState('not-onboard');
                  const editView = document.getElementById('employment-not-onboard-edit-view');
                  const displayView = document.getElementById('employment-not-onboard-display-view');
                  if (editView) editView.style.display = 'flex';
                  if (displayView) displayView.style.display = 'none';
                  const noteArea = document.getElementById('employment-note-textarea');
                  if (noteArea) noteArea.value = '';
                }
              };
            }
            
            // 4. 读取已有入职记录并初始化面板
            const existingList = await window.hrApi.employmentRecords({ candidate_id: resolvedIdNum });
            const existing = existingList && existingList[0];
            
            const editView = document.getElementById('employment-not-onboard-edit-view');
            const displayView = document.getElementById('employment-not-onboard-display-view');
            const savedNoteText = document.getElementById('employment-saved-note-text');
            const noteArea = document.getElementById('employment-note-textarea');
            
            if (existing && existing.status === '已入职') {
              window.setEmploymentPanelState('onboard');
              
              const obDateStr = existing.onboard_date ? existing.onboard_date.slice(0, 10) : new Date().toISOString().slice(0, 10);
              
              // 计算已有记录的质保期
              const diffTime = new Date() - new Date(obDateStr);
              const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24));
              const isUnderWarranty = diffDays <= warrantyDays;
              const warrantyText = isUnderWarranty ? "质保在职" : "超过质保期";
              
              document.getElementById('employment-display-onboard-date').textContent = obDateStr;
              document.getElementById('employment-display-position').textContent = existing.position_name || salaryPos;
              document.getElementById('employment-display-position').title = existing.position_name || salaryPos;
              document.getElementById('employment-display-company').textContent = existing.company_name || salaryComp;
              document.getElementById('employment-display-company').title = existing.company_name || salaryComp;
              
              const warrantyEl = document.getElementById('employment-display-warranty');
              if (warrantyEl) {
                warrantyEl.textContent = warrantyText;
                if (isUnderWarranty) {
                  warrantyEl.style.backgroundColor = 'rgba(255,255,255,0.25)';
                  warrantyEl.style.color = '#fff';
                } else {
                  warrantyEl.style.backgroundColor = '#fee2e2';
                  warrantyEl.style.color = '#b91c1c';
                }
              }
            } else {
              window.setEmploymentPanelState('not-onboard');
              if (existing && existing.status === '未入职' && existing.note) {
                // 已有未入职记录且填写过备注，展示已保存态
                if (editView) editView.style.display = 'none';
                if (displayView) displayView.style.display = 'block';
                if (savedNoteText) savedNoteText.textContent = existing.note;
              } else {
                // 没有记录，或者没填写过备注，展示编辑输入态
                if (editView) editView.style.display = 'flex';
                if (displayView) displayView.style.display = 'none';
                if (noteArea) noteArea.value = existing?.note || '';
              }
            }
          }
        }
      } catch (err) {
        console.warn("Failed to initialize employment status panel in details view:", err);
      }
    })();

    if (window.updateCandidatePanels) {
      window.updateCandidatePanels(item?.id);
    }
    return;

  }
  if (button.dataset.action === "edit-candidate") {
    const candidateKey = button.dataset.candidateKey || button.dataset.rowKey || button.dataset.id || '';
    const item = candidateKey ? await window.hrApi.candidate(candidateKey) : null;
    if (!item) throw new Error('未找到候选人');
    const modal = document.querySelector('[data-candidate-edit-modal]');
    const fill = (sel, val) => { const el = document.querySelector(sel); if (el) el.value = val || ''; };
    fill('[data-candidate-edit-name]', item.name);
    fill('[data-candidate-edit-gender]', item.gender);
    fill('[data-candidate-edit-age]', item.age || '');
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
    
    // 获取表单值
    const phone = get('[data-candidate-edit-phone]');
    const email = get('[data-candidate-edit-email]');
    const id_number = get('[data-candidate-edit-idnumber]');
    
    // 正则表达式验证
    if (phone) {
      const phoneRegex = /^1[3-9]\d{9}$/;
      if (!phoneRegex.test(phone)) {
        throw new Error('请输入有效的中国11位手机号码');
      }
    }
    
    if (email) {
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailRegex.test(email)) {
        throw new Error('请输入有效的电子邮箱地址');
      }
    }
    
    if (id_number) {
      const idRegex = /(^\d{15}$)|(^\d{18}$)|(^\d{17}(\d|X|x)$)/;
      if (!idRegex.test(id_number)) {
        throw new Error('请输入符合国家标准的身份证号码');
      }
    }
    
    const payload = {
      name: get('[data-candidate-edit-name]'),
      phone,
      email,
      current_title: get('[data-candidate-edit-title]'),
      city: get('[data-candidate-edit-city]'),
      status: get('[data-candidate-edit-status]') || '激活',
      source: get('[data-candidate-edit-source]'),
      gender: get('[data-candidate-edit-gender]'),
      age: get('[data-candidate-edit-age]') ? parseInt(get('[data-candidate-edit-age]'), 10) : null,
      birth_date: get('[data-candidate-edit-birth-date]'),
      hukou_location: get('[data-candidate-edit-hukou]'),
      id_number,
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
      window.candidatesPageState.rawList = items;
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
                  <div class="avatar-sm" style="display:flex; align-items:center; justify-content:center; font-size:18px;">${i.locked ? '🔒' : '🔓'}</div>
                  <div>
                    <strong>${i.name}</strong>
                  </div>
                </div>
              </div>
              <div>${i.current_title || '--'}</div>
              <div>${i.city || '--'}</div>
              <div class="mono">${i.expected_salary || '--'}</div>
              <div>${i.source || '--'}</div>
              <div><span class="state ${i.status === '锁定' ? 'locked' : 'active'}">${i.status || '未知'}</span></div>
              <div>
                <div class="table-actions">
                  <button class="btn-sm primary" data-action="view-detail" data-id="${i.record_key || `candidate:${i.id}`}" data-row-key="${i.record_key || `candidate:${i.id}`}" data-candidate-key="${i.record_key || `candidate:${i.id}`}" data-title="${i.name}">详情</button>
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
    const source = document.querySelector('[data-candidate-source]')?.value?.trim() || '手工导入';
    if (!name || !phone) throw new Error('请先填写姓名和电话');
    const candidate = await window.hrApi.createCandidate({ name, phone, email, current_title: currentTitle, city, status: '激活', source });
    const modal = document.querySelector('[data-candidate-create-modal]');
    if (modal) modal.style.display = 'none';
    if (window.candidatesPageState) {
      const items = await window.hrApi.candidates();
      window.candidatesPageState.rawList = items;
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
                  <div class="avatar-sm" style="display:flex; align-items:center; justify-content:center; font-size:18px;">${i.locked ? '🔒' : '🔓'}</div>
                  <div>
                    <strong>${i.name}</strong>
                  </div>
                </div>
              </div>
              <div>${i.current_title || '--'}</div>
              <div>${i.city || '--'}</div>
              <div class="mono">${i.expected_salary || '--'}</div>
              <div>${i.source || '--'}</div>
              <div><span class="state ${i.status === '锁定' ? 'locked' : 'active'}">${i.status || '未知'}</span></div>
              <div>
                <div class="table-actions">
                  <button class="btn-sm primary" data-action="view-detail" data-id="${i.record_key || `candidate:${i.id}`}" data-row-key="${i.record_key || `candidate:${i.id}`}" data-candidate-key="${i.record_key || `candidate:${i.id}`}" data-title="${i.name}">详情</button>
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
  if (button.dataset.action === "open-batch-recommend-modal") {
    const selectedCandidates = Array.from(window.candidatesPageState?.selectedCandidates?.entries?.() || []);
    if (!selectedCandidates.length) throw new Error('请先勾选需要推荐的候选人');

    const urlParams = new URLSearchParams(location.search);
    const isSelectMode = urlParams.get('select_mode') === '1';
    const targetPositionId = urlParams.get('position_id');
    if (isSelectMode && targetPositionId) {
      if (!confirm(`确定要将这 ${selectedCandidates.length} 名候选人加入当前岗位吗？`)) return;
      const recordKeys = selectedCandidates.map(([recordKey]) => recordKey);
      const result = await window.hrApi.createBatchRecommendations({
        record_keys: recordKeys,
        position_id: Number(targetPositionId),
        recommender: 'admin',
        status: '待推荐',
        feedback: '通过岗位快捷搜索加入'
      });
      showToast(`成功添加 ${result.succeeded} 名候选人到当前岗位`);
      
      if (window.candidatesPageState) {
        window.candidatesPageState.clearSelection();
      }
      
      // 让父页面刷新树
      if (window.parent && typeof window.parent.refreshTreePage === 'function') {
        window.parent.refreshTreePage().catch(err => console.warn(err));
      }
      return;
    }

    const modal = document.querySelector('[data-recommend-modal]');
    if (modal) {
      modal.dataset.recordKeys = JSON.stringify(selectedCandidates.map(([recordKey]) => recordKey));
      modal.style.display = 'block';
    }
    const selectedSummary = document.querySelector('[data-recommend-selected-summary]');
    const candidateSummary = document.querySelector('[data-recommend-candidate-summary]');
    const resultPanel = document.querySelector('[data-recommend-result]');
    if (selectedSummary) selectedSummary.textContent = `已选择 ${selectedCandidates.length} 位候选人，将统一推荐至同一岗位`;
    if (candidateSummary) {
      const names = selectedCandidates.slice(0, 6).map(([, candidate]) => escapeHtml(candidate?.name || '未命名候选人'));
      const remaining = selectedCandidates.length - names.length;
      candidateSummary.innerHTML = `<div class="item-title">本次候选人</div><div class="item-meta">${names.join('、')}${remaining > 0 ? ` 等 ${selectedCandidates.length} 人` : ''}</div>`;
    }
    if (resultPanel) {
      resultPanel.style.display = 'none';
      resultPanel.innerHTML = '';
    }
    const companySelect = document.querySelector('[data-recommend-company-select]');
    const projectSelect = document.querySelector('[data-recommend-project-select]');
    const positionSelect = document.querySelector('[data-recommend-position-select]');
    const feedbackTextarea = document.querySelector('[data-recommend-feedback-textarea]');
    if (feedbackTextarea) feedbackTextarea.value = '';
    if (companySelect) {
      companySelect.innerHTML = '<option value="">加载中...</option>';
      try {
        const companies = await window.hrApi.companies();
        companySelect.innerHTML = '<option value="">-- 请选择客户公司 --</option>' +
          companies.map(c => `<option value="${c.id}">${c.name}</option>`).join('');
      } catch (err) {
        companySelect.innerHTML = '<option value="">加载失败</option>';
      }
    }
    if (projectSelect) projectSelect.innerHTML = '<option value="">-- 请先选择客户公司 --</option>';
    if (positionSelect) positionSelect.innerHTML = '<option value="">-- 请先选择猎头项目 --</option>';
    return;
  }
  if (button.dataset.action === "close-recommend-modal") {
    const modal = document.querySelector('[data-recommend-modal]');
    if (modal) modal.style.display = 'none';
    return;
  }
  if (button.dataset.action === "edit-candidate-tree") {
    const id = button.dataset.id || '';
    if (!id) throw new Error('候选人 ID 缺失');
    // 动态注入候选人编辑弹窗（如果当前页面不存在）
    if (!document.querySelector('[data-candidate-edit-modal]')) {
      const div = document.createElement('div');
      div.innerHTML = `<div class="modal" data-candidate-edit-modal style="display:none;position:fixed;inset:0;background:rgba(14,22,34,.45);z-index:2000;padding:24px;overflow-y:auto;"><div class="panel" style="max-width:960px;margin:4vh auto 24px;background:#fff;"><div class="section-head"><div><h3>编辑候选人</h3><div class="section-sub">保存后会写入候选人表并刷新列表。</div></div><div style="display:flex;gap:8px;align-items:center;flex-wrap:wrap;"><span style="border-left:1px solid rgba(15,23,42,.1);height:24px;margin:0 8px;"></span><button class="btn" data-action="close-candidate-edit-modal">取消</button><button class="btn primary" data-action="confirm-candidate-edit">确认保存</button></div></div><div class="grid-2" style="max-height:70vh;overflow-y:auto;padding:2px;"><div class="panel" style="box-shadow:none;border:1px solid rgba(15,23,42,.08);margin:0;"><div style="font-size:11px;font-weight:600;color:#64748b;text-transform:uppercase;letter-spacing:.06em;margin-bottom:8px;">基本信息</div><div class="list"><div class="list-item"><div class="item-top"><div><div class="item-title">姓名</div><div class="item-meta">可根据原件信息修正拼写错误</div></div></div><input class="input" data-candidate-edit-name /></div><div class="list-item"><div class="item-top"><div><div class="item-title">性别</div><div class="item-meta">男 / 女</div></div></div><select class="input" data-candidate-edit-gender><option value="">不填</option><option value="男">男</option><option value="女">女</option></select></div><div class="list-item"><div class="item-top"><div><div class="item-title">年龄</div><div class="item-meta">纯数字</div></div></div><input type="number" class="input" data-candidate-edit-age placeholder="如: 28" /></div><div class="list-item"><div class="item-top"><div><div class="item-title">出生日期</div><div class="item-meta">请选择日期</div></div></div><input class="input" type="date" data-candidate-edit-birth-date /></div><div class="list-item"><div class="item-top"><div><div class="item-title">户口所在地</div></div></div><input class="input" data-candidate-edit-hukou placeholder="请输入户口所在地" /></div><div class="list-item"><div class="item-top"><div><div class="item-title">城市</div></div></div><input class="input" data-candidate-edit-city placeholder="请输入城市" /></div><div class="list-item"><div class="item-top"><div><div class="item-title">电话</div><div class="item-meta">仅限中国11位手机号</div></div></div><input class="input" data-candidate-edit-phone placeholder="13912345678" /></div><div class="list-item"><div class="item-top"><div><div class="item-title">邮筱</div></div></div><input class="input" type="email" data-candidate-edit-email placeholder="example@domain.com" /></div><div class="list-item"><div class="item-top"><div><div class="item-title">家庭情况</div></div></div><select class="input" data-candidate-edit-family><option value="">请选择</option><option value="未婚">未婚</option><option value="已婚">已婚</option><option value="已婚未育">已婚未育</option><option value="已婚已育">已婚已育</option></select></div></div><div style="font-size:11px;font-weight:600;color:#64748b;text-transform:uppercase;letter-spacing:.06em;margin:16px 0 8px;">职业经历</div><div class="list"><div class="list-item"><div class="item-top"><div><div class="item-title">当前职位</div></div></div><input class="input" data-candidate-edit-title /></div><div class="list-item"><div class="item-top"><div><div class="item-title">最高学历</div></div></div><select class="input" data-candidate-edit-education><option value="高中">高中</option><option value="大专">大专</option><option value="本科" selected>本科</option><option value="硕士">硕士</option><option value="博士">博士</option></select></div><div class="list-item"><div class="item-top"><div><div class="item-title">工作年限</div><div class="item-meta">年（数字）</div></div></div><input class="input" type="number" data-candidate-edit-exp-years /></div><div class="list-item"><div class="item-top"><div><div class="item-title">教育背景</div></div></div><textarea class="input" rows="3" data-candidate-edit-edu-detail></textarea></div><div class="list-item"><div class="item-top"><div><div class="item-title">职业经历</div></div></div><textarea class="input" rows="4" data-candidate-edit-work-history></textarea></div><div class="list-item"><div class="item-top"><div><div class="item-title">项目经历</div></div></div><textarea class="input" rows="3" data-candidate-edit-project-history></textarea></div><div class="list-item"><div class="item-top"><div><div class="item-title">专业证书</div></div></div><textarea class="input" rows="2" data-candidate-edit-certificates></textarea></div></div></div><div class="panel" style="box-shadow:none;border:1px solid rgba(15,23,42,.08);margin:0;"><div style="font-size:11px;font-weight:600;color:#64748b;text-transform:uppercase;letter-spacing:.06em;margin-bottom:8px;">求职意向</div><div class="list"><div class="list-item"><div class="item-top"><div><div class="item-title">期望薪资</div><div class="item-meta">仅限数字，单位（元/月）</div></div></div><input class="input" type="number" data-candidate-edit-salary placeholder="例如：25000" /></div><div class="list-item"><div class="item-top"><div><div class="item-title">薪资结构</div><div class="item-meta">例：12薪+2个月年终</div></div></div><input class="input" data-candidate-edit-salary-structure /></div><div class="list-item"><div class="item-top"><div><div class="item-title">到岗周期</div></div></div><select class="input" data-candidate-edit-onboard><option value="一周">一周</option><option value="两周">两周</option><option value="一个月">一个月</option><option value="两个月">两个月</option><option value="三个月">三个月</option></select></div><div class="list-item"><div class="item-top"><div><div class="item-title">职位状态</div></div></div><select class="input" data-candidate-edit-job-status><option value="在职">在职</option><option value="离职">离职</option><option value="随时到岗">随时到岗</option></select></div><div class="list-item"><div class="item-top"><div><div class="item-title">求职意向</div><div class="item-meta">目标岗位、行业</div></div></div><textarea class="input" rows="3" data-candidate-edit-intention></textarea></div></div><div style="font-size:11px;font-weight:600;color:#64748b;text-transform:uppercase;letter-spacing:.06em;margin:16px 0 8px;">评估</div><div class="list"><div class="list-item"><div class="item-top"><div><div class="item-title">核心价值</div></div></div><textarea class="input" rows="3" data-candidate-edit-core-value></textarea></div><div class="list-item"><div class="item-top"><div><div class="item-title">综合评估</div></div></div><textarea class="input" rows="3" data-candidate-edit-evaluation></textarea></div></div><div style="font-size:11px;font-weight:600;color:#64748b;text-transform:uppercase;letter-spacing:.06em;margin:16px 0 8px;">系统状态</div><div class="list"><div class="list-item"><div class="item-top"><div><div class="item-title">当前状态</div><div class="item-meta">未锁定 / 锁定</div></div></div><select class="input" data-candidate-edit-status><option value="未锁定">未锁定</option><option value="锁定">锁定</option></select></div><div class="list-item"><div class="item-top"><div><div class="item-title">来源</div></div></div><select class="input" data-candidate-edit-source><option value="手工导入">手工导入</option><option value="简历库">简历库</option></select></div><div class="list-item"><div class="item-top"><div><div class="item-title">身份证号</div></div></div><input class="input" data-candidate-edit-idnumber placeholder="例如：110101199001011234" /></div><div class="list-item"><div class="item-top"><div><div class="item-title">标签</div><div class="item-meta">逗号分隔</div></div></div><input class="input" data-candidate-edit-tags /></div></div></div></div></div></div>`;
      document.body.appendChild(div.firstElementChild);
    }
    // id 已在 if 块之前声明，直接使用
    const item = await window.hrApi.candidate(String(id));
    if (!item) throw new Error('候选人不存在');
    const modal = document.querySelector('[data-candidate-edit-modal]');
    const fill = (sel, val) => { const el = document.querySelector(sel); if (el) el.value = val || ''; };
    fill('[data-candidate-edit-name]', item.name);
    fill('[data-candidate-edit-gender]', item.gender);
    fill('[data-candidate-edit-age]', item.age || '');
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
    fill('[data-candidate-edit-status]', item.locked ? '锁定' : (item.status || '未锁定'));
    fill('[data-candidate-edit-source]', item.source);
    fill('[data-candidate-edit-tags]', item.tags);
    if (modal) {
      modal.style.display = 'block';
      modal.dataset.candidateId = String(item.id);
      modal.dataset.target = JSON.stringify({ id: item.id });
    }
    return;
  }
  if (button.dataset.action === "delete-candidate-tree") {
    const recommendationId = Number(button.dataset.recommendationId || 0);
    if (!recommendationId) throw new Error('推荐记录 ID 缺失');
    if (!confirm('确定将该候选人从此岗位移除并解除锁定吗？')) return;
    await window.hrApi.deleteRecommendation(recommendationId);
    showToast('候选人已移除并解除锁定');
    // 保留已展开岗位 ID，clear 缓存后重新拉取候选人再渲染
    const expandedPositionIds = Array.from(treeState.expandedPositions);
    treeState.candidatesByPosition.clear();
    await Promise.all(expandedPositionIds.map(pid => loadPositionCandidates(pid)));
    const page = location.pathname.split("/").pop() || "";
    if (page === "customers.html") await renderCustomerTreeFromState();
    else if (page === "projects.html") await renderProjectTreeFromState();
    else if (page === "positions.html") await renderPositionTreeFromState();
    return;
  }
  if (button.dataset.action === "batch-delete-candidates-tree") {
    const checkboxes = document.querySelectorAll('.tree-candidate-checkbox:checked');
    if (!checkboxes.length) throw new Error('请先选择要移除的候选人');
    const items = Array.from(checkboxes).map(cb => ({
      recommendationId: Number(cb.dataset.recommendationId || 0),
      candidateId: Number(cb.dataset.candidateId || 0),
    })).filter(item => item.recommendationId > 0);
    if (!items.length) throw new Error('没有可移除的推荐记录');
    if (!confirm(`确定批量移除 ${items.length} 名候选人并解除锁定吗？`)) return;
    const ids = items.map(item => item.recommendationId);
    const result = await window.hrApi.batchDeleteRecommendations(ids);
    showToast(`已移除 ${result.deleted} 名候选人`);
    // 保留已展开岗位 ID，clear 缓存后重新拉取候选人再渲染
    const expandedPositionIds = Array.from(treeState.expandedPositions);
    treeState.candidatesByPosition.clear();
    await Promise.all(expandedPositionIds.map(pid => loadPositionCandidates(pid)));
    checkboxes.forEach(cb => cb.checked = false);
    document.querySelectorAll('[data-batch-delete-candidates-btn]').forEach(btn => btn.textContent = '批量移除候选人');
    const page = location.pathname.split("/").pop() || "";
    if (page === "customers.html") await renderCustomerTreeFromState();
    else if (page === "projects.html") await renderProjectTreeFromState();
    else if (page === "positions.html") await renderPositionTreeFromState();
    return;
  }
  if (button.dataset.action === "confirm-recommend") {
    const modal = document.querySelector('[data-recommend-modal]');
    let recordKeys = [];
    try {
      recordKeys = JSON.parse(modal?.dataset.recordKeys || '[]');
    } catch (err) {
      recordKeys = [];
    }
    if (!recordKeys.length) throw new Error('没有待推荐的候选人');
    const positionSelect = document.querySelector('[data-recommend-position-select]');
    const positionId = positionSelect?.value;
    if (!positionId) throw new Error('请选择要推荐的招聘岗位');
    const feedbackTextarea = document.querySelector('[data-recommend-feedback-textarea]');
    const feedback = feedbackTextarea?.value?.trim() || '';
    const result = await window.hrApi.createBatchRecommendations({
      record_keys: recordKeys,
      position_id: Number(positionId),
      recommender: 'admin',
      status: '待推荐',
      feedback: feedback
    });
    const successfulKeys = new Set(result.items.filter((item) => item.result === 'success').map((item) => item.record_key));
    successfulKeys.forEach((recordKey) => window.candidatesPageState?.selectedCandidates?.delete(recordKey));
    window.candidatesPageState?.syncSelectionUI?.();

    const remainingItems = result.items.filter((item) => item.result !== 'success');
    const remainingKeys = remainingItems.map((item) => item.record_key);
    if (modal) modal.dataset.recordKeys = JSON.stringify(remainingKeys);
    if (!remainingItems.length) {
      if (modal) modal.style.display = 'none';
      if (window.candidatesPageState) {
        await window.candidatesPageState.applyFilters();
      }
      showToast(`批量推荐完成：成功 ${result.succeeded} 人`);
      return;
    }

    const selectedSummary = document.querySelector('[data-recommend-selected-summary]');
    const candidateSummary = document.querySelector('[data-recommend-candidate-summary]');
    const resultPanel = document.querySelector('[data-recommend-result]');
    if (selectedSummary) selectedSummary.textContent = `成功 ${result.succeeded} 人，剩余 ${remainingItems.length} 人待处理`;
    if (candidateSummary) {
      candidateSummary.innerHTML = `<div class="item-title">处理汇总</div><div class="item-meta">成功 ${result.succeeded} · 跳过 ${result.skipped} · 失败 ${result.failed}</div>`;
    }
    if (resultPanel) {
      resultPanel.style.display = 'block';
      resultPanel.innerHTML = `<div class="item-title">未完成候选人</div><div class="list" style="margin-top:8px;">${remainingItems.map((item) => `
        <div class="list-item" style="padding:8px 0;border:0;border-top:1px solid rgba(15,23,42,.06);">
          <div class="item-top">
            <div><div class="item-title">${escapeHtml(item.candidate_name || item.record_key)}</div><div class="item-meta">${escapeHtml(item.reason || '处理失败')}</div></div>
            <span class="chip ${item.result === 'skipped' ? 'warning' : 'danger'}">${item.result === 'skipped' ? '已跳过' : '失败'}</span>
          </div>
        </div>`).join('')}</div>`;
    }
    if (window.candidatesPageState) {
      await window.candidatesPageState.applyFilters();
    }
    showToast(`批量推荐：成功 ${result.succeeded}，跳过 ${result.skipped}，失败 ${result.failed}`);
    return;
  }
  if (button.dataset.action === "open-add-note-modal") {
    const candidateId = String(button.dataset.id || document.querySelector('[data-candidate-detail-modal]')?.dataset.candidateId || '');
    if (!candidateId || candidateId === '0') throw new Error('请先打开候选人详情');
    const modal = document.querySelector('[data-add-note-modal]');
    if (modal) {
      modal.dataset.candidateId = candidateId;
      modal.style.display = 'block';
    }
    const txt = document.querySelector('[data-add-note-textarea]');
    if (txt) {
      txt.value = '';
      setTimeout(() => txt.focus(), 50);
    }
    return;
  }
  if (button.dataset.action === "close-add-note-modal") {
    const modal = document.querySelector('[data-add-note-modal]');
    if (modal) modal.style.display = 'none';
    return;
  }
  if (button.dataset.action === "confirm-add-note") {
    const modal = document.querySelector('[data-add-note-modal]');
    const candidateId = modal?.dataset.candidateId || '';
    if (!candidateId || candidateId === '0') throw new Error('没有待添加备注的候选人');
    const txt = document.querySelector('[data-add-note-textarea]');
    const content = txt?.value?.trim() || '';
    if (!content) throw new Error('请输入备注内容');
    const record = await window.hrApi.createCandidateNote({
      candidate_id: Number(candidateId),
      content: content,
      operator: 'admin'
    });
    if (modal) modal.style.display = 'none';
    showToast('备注添加成功！');
    const detailModal = document.querySelector('[data-candidate-detail-modal]');
    if (detailModal && detailModal.dataset.candidateId === candidateId) {
      const fakeBtn = document.createElement("button");
      fakeBtn.dataset.action = "view-detail";
      fakeBtn.dataset.id = candidateId;
      handleGlobalButton(fakeBtn).catch(err => console.warn(err));
    }
    return;
  }
  if (button.dataset.action === "open-add-tracking-modal") {
    const candidateId = String(button.dataset.id || '');
    if (!candidateId || candidateId === '0') throw new Error('没有选中的候选人');
    const modal = document.querySelector('[data-add-tracking-modal]');
    if (modal) {
      modal.dataset.candidateId = candidateId;
      modal.dataset.mode = "add";
      modal.querySelector('h3').textContent = "添加面试记录";
      modal.style.display = 'block';
      
      // 默认面试日期设为今天
      const dateInput = document.getElementById("tracking-interview-date");
      if (dateInput) {
        const today = new Date();
        const yyyy = today.getFullYear();
        const mm = String(today.getMonth() + 1).padStart(2, '0');
        const dd = String(today.getDate()).padStart(2, '0');
        dateInput.value = `${yyyy}-${mm}-${dd}`;
      }
      
      // 清空其它输入框
      document.getElementById("tracking-interview-round").value = "";
      document.getElementById("tracking-screening-result").value = "";
      document.getElementById("tracking-interviewer").value = "";
      document.getElementById("tracking-interview-location").value = "";
      document.getElementById("tracking-interview-requirements").value = "";
      document.getElementById("tracking-interview-contact").value = "";
      document.getElementById("tracking-note").value = "";
    }
    return;
  }
  if (button.dataset.action === "edit-tracking-event") {
    const eventId = Number(button.dataset.id);
    const candidateId = button.dataset.candidateId;
    const modal = document.querySelector('[data-add-tracking-modal]');
    if (!modal) return;
    
    modal.dataset.candidateId = candidateId;
    modal.dataset.eventId = String(eventId);
    modal.dataset.mode = "edit";
    modal.querySelector('h3').textContent = "编辑面试记录";
    modal.style.display = 'block';
    
    try {
      const list = await window.hrApi.candidateTrackingEvents({ candidate_id: Number(candidateId) });
      const evt = list.find(i => i.id === eventId);
      if (!evt) throw new Error("未找到对应记录");
      
      document.getElementById("tracking-interview-round").value = evt.interview_round || "";
      document.getElementById("tracking-screening-result").value = evt.screening_result || "";
      document.getElementById("tracking-interview-date").value = evt.interview_date || "";
      document.getElementById("tracking-interviewer").value = evt.interviewer || "";
      document.getElementById("tracking-interview-location").value = evt.interview_location || "";
      document.getElementById("tracking-interview-requirements").value = evt.interview_requirements || "";
      document.getElementById("tracking-interview-contact").value = evt.interview_contact || "";
      document.getElementById("tracking-note").value = evt.note || "";
    } catch (err) {
      console.error("加载记录失败", err);
      showToast("加载记录详情失败: " + err.message);
      modal.style.display = 'none';
    }
    return;
  }
  if (button.dataset.action === "delete-tracking-event") {
    const eventId = Number(button.dataset.id);
    const candidateId = button.dataset.candidateId;
    if (confirm("确定要删除这条面试记录吗？此操作不可撤销。")) {
      try {
        await window.hrApi.deleteCandidateTrackingEvent(eventId);
        showToast("面试记录已成功删除");
        
        const detailModal = document.querySelector('[data-candidate-detail-modal]');
        if (detailModal && detailModal.dataset.candidateId === candidateId) {
          const fakeBtn = document.createElement("button");
          fakeBtn.dataset.action = "view-detail";
          fakeBtn.dataset.id = candidateId;
          handleGlobalButton(fakeBtn).catch(err => console.warn(err));
        }
      } catch (err) {
        showToast("删除面试记录失败: " + err.message);
      }
    }
    return;
  }
  if (button.dataset.action === "close-add-tracking-modal") {
    const modal = document.querySelector('[data-add-tracking-modal]');
    if (modal) modal.style.display = 'none';
    return;
  }
  if (button.dataset.action === "confirm-add-tracking") {
    const modal = document.querySelector('[data-add-tracking-modal]');
    const candidateId = modal?.dataset.candidateId || '';
    if (!candidateId || candidateId === '0') throw new Error('没有待保存面试记录的候选人');

    const interviewRound = document.getElementById("tracking-interview-round").value.trim();
    const screeningResult = document.getElementById("tracking-screening-result").value.trim();
    const interviewDate = document.getElementById("tracking-interview-date").value.trim();
    const interviewer = document.getElementById("tracking-interviewer").value.trim();
    const interviewLocation = document.getElementById("tracking-interview-location").value.trim();
    const interviewRequirements = document.getElementById("tracking-interview-requirements").value.trim();
    const interviewContact = document.getElementById("tracking-interview-contact").value.trim();
    const note = document.getElementById("tracking-note").value.trim();

    if (!interviewRound) throw new Error("请选择面试轮次");
    if (interviewRound === "初筛" && !screeningResult) throw new Error("初筛轮次下必须选择初筛结果");

    const payload = {
      candidate_id: Number(candidateId),
      event_type: "面试",
      status: "已完成",
      summary: `${interviewRound} - ${screeningResult || '已安排'}`,
      interview_round: interviewRound,
      screening_result: screeningResult,
      interview_date: interviewDate,
      interviewer: interviewer,
      interview_location: interviewLocation,
      interview_requirements: interviewRequirements,
      interview_contact: interviewContact,
      interview_result: "-",
      note: note,
      employment_status: "待设置",
      operator: ""
    };

    const mode = modal.dataset.mode;
    if (mode === "edit") {
      const eventId = Number(modal.dataset.eventId);
      await window.hrApi.updateCandidateTrackingEvent(eventId, payload);
      showToast("面试记录修改成功！");
    } else {
      await window.hrApi.createCandidateTrackingEvent(payload);
      showToast("面试记录添加成功！");
    }
    
    if (modal) modal.style.display = 'none';

    const detailModal = document.querySelector('[data-candidate-detail-modal]');
    if (detailModal && detailModal.dataset.candidateId === candidateId) {
      const fakeBtn = document.createElement("button");
      fakeBtn.dataset.action = "view-detail";
      fakeBtn.dataset.id = candidateId;
      handleGlobalButton(fakeBtn).catch(err => console.warn(err));
    }
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
async function populateSalaryPositionOptions({ positionId = '', positionName = '', companyName = '' } = {}) {
  const positionSelect = document.getElementById('salary-position-id');
  const companyDisplay = document.getElementById('salary-company-name-display');
  if (!positionSelect || !companyDisplay) return { positions: [], projects: [], projectMap: new Map() };

  positionSelect.innerHTML = '<option value="">加载中...</option>';
  companyDisplay.textContent = '所属公司：请选择岗位后自动显示';

  try {
    const [positions, projects] = await Promise.all([window.hrApi.positions(), window.hrApi.projects()]);
    const projectMap = new Map(projects.map((project) => [project.id, project]));
    const fallbackMatch = !positionId
      ? positions.find((position) => {
          const project = projectMap.get(position.project_id);
          return position.name === positionName && (project?.company_name || '') === (companyName || '');
        })
      : null;
    const resolvedPositionId = String(positionId || fallbackMatch?.id || '');

    positionSelect.innerHTML = '<option value="">请选择岗位</option>' + positions.map((position) => `<option value="${position.id}">${position.name}</option>`).join('');
    positionSelect.value = resolvedPositionId;

    const syncCompanyDisplay = () => {
      const selectedPosition = positions.find((position) => String(position.id) === String(positionSelect.value || ''));
      if (selectedPosition) {
        const selectedProject = projectMap.get(selectedPosition.project_id);
        const company = selectedProject?.company_name || '未知公司';
        companyDisplay.textContent = `所属公司：${company}`;
        companyDisplay.title = `${company} · ${selectedPosition.name}`;
        return;
      }
      if (companyName) {
        companyDisplay.textContent = `所属公司：${companyName}（历史记录）`;
        companyDisplay.title = companyName;
        return;
      }
      companyDisplay.textContent = '所属公司：请选择岗位后自动显示';
      companyDisplay.title = '';
    };

    positionSelect.onchange = syncCompanyDisplay;
    syncCompanyDisplay();
    return { positions, projects, projectMap };
  } catch (err) {
    console.warn("Failed to populate salary position select:", err);
    positionSelect.innerHTML = '<option value="">加载失败</option>';
    companyDisplay.textContent = '所属公司：加载岗位失败';
    return { positions: [], projects: [], projectMap: new Map() };
  }
}

  if (button.dataset.action === "open-add-salary-modal") {
    const candidateId = String(button.dataset.id || button.dataset.candidateId || document.querySelector('[data-candidate-detail-modal]')?.dataset.candidateId || '');
    if (!candidateId || candidateId === '0') throw new Error('请先打开候选人详情');
    
    const modal = document.querySelector('[data-salary-tracking-modal]');
    if (!modal) return;
    
    modal.dataset.mode = 'add';
    modal.dataset.candidateId = candidateId;
    delete modal.dataset.recordId;
    
    const titleEl = document.getElementById('salary-modal-title');
    if (titleEl) titleEl.innerHTML = '💰 添加薪资/福利/入职条件记录';
    
    const roundEl = document.getElementById('salary-interview-round');
    const agreedEl = document.getElementById('salary-agreed-salary');
    const welfareEl = document.getElementById('salary-welfare-desc');
    const onboardEl = document.getElementById('salary-onboard-cond');
    const acceptEl = document.getElementById('salary-candidate-accepted');
    const positionSelect = document.getElementById('salary-position-id');
    
    await populateSalaryPositionOptions();
    if (positionSelect) positionSelect.value = '';
    if (agreedEl) agreedEl.value = '';
    if (welfareEl) welfareEl.value = '';
    if (onboardEl) onboardEl.value = '';
    if (acceptEl) acceptEl.value = '接受';
    
    if (roundEl) {
      roundEl.innerHTML = '';
      roundEl.disabled = false;
      
      try {
        const events = await window.hrApi.candidateTrackingEvents({ candidate_id: Number(candidateId) });
        const rounds = [...new Set(events.map(evt => evt.interview_round).filter(Boolean))];
        if (rounds.length > 0) {
          rounds.forEach(r => {
            const opt = document.createElement('option');
            opt.value = r;
            opt.textContent = r;
            roundEl.appendChild(opt);
          });
        } else {
          ['第1轮', '第2轮', '第3轮', '第4轮'].forEach(r => {
            const opt = document.createElement('option');
            opt.value = r;
            opt.textContent = r;
            roundEl.appendChild(opt);
          });
        }
      } catch (err) {
        console.warn("Failed to fetch candidate tracking events for round selection:", err);
        ['第1轮', '第2轮', '第3轮', '第4轮'].forEach(r => {
          const opt = document.createElement('option');
          opt.value = r;
          opt.textContent = r;
          roundEl.appendChild(opt);
        });
      }
    }
    
    modal.style.display = 'block';
    return;
  }
  if (button.dataset.action === "close-salary-tracking-modal") {
    const modal = document.querySelector('[data-salary-tracking-modal]');
    if (modal) modal.style.display = 'none';
    return;
  }
  if (button.dataset.action === "confirm-salary-tracking") {
    const modal = document.querySelector('[data-salary-tracking-modal]');
    if (!modal) return;
    
    const candidateId = modal.dataset.candidateId || '';
    const recordId = modal.dataset.recordId || '';
    const mode = modal.dataset.mode || 'add';
    
    if (!candidateId || candidateId === '0') throw new Error('找不到候选人 ID');
    
    const roundEl = document.getElementById('salary-interview-round');
    const positionSelect = document.getElementById('salary-position-id');
    const agreedEl = document.getElementById('salary-agreed-salary');
    const welfareEl = document.getElementById('salary-welfare-desc');
    const onboardEl = document.getElementById('salary-onboard-cond');
    const acceptEl = document.getElementById('salary-candidate-accepted');
    
    const user = window.currentUser || await window.hrApi.me().catch(() => null);
    const operatorName = user?.full_name || user?.username || '管理员';

    const payload = {
      candidate_id: Number(candidateId),
      position_id: Number(positionSelect?.value || 0) || null,
      interview_round: roundEl?.value || '',
      agreed_salary: agreedEl?.value?.trim() || '',
      welfare_desc: welfareEl?.value?.trim() || '',
      onboard_cond: onboardEl?.value?.trim() || '',
      candidate_accepted: acceptEl?.value || '接受',
      operator: operatorName
    };
    
    if (!payload.interview_round) throw new Error('请选择或指定关联面试轮次');
    if (!payload.position_id) throw new Error('请选择关联岗位');
    
    if (mode === 'add') {
      await window.hrApi.createSalaryRecord(payload);
      showToast('添加薪资记录成功');
    } else if (mode === 'edit') {
      if (!recordId) throw new Error('找不到记录 ID，无法更新');
      await window.hrApi.updateSalaryRecord(Number(recordId), payload);
      showToast('更新薪资记录成功');
    }
    
    modal.style.display = 'none';
    
    const detailModal = document.querySelector('[data-candidate-detail-modal]');
    if (detailModal && detailModal.dataset.candidateId === candidateId) {
      const fakeBtn = document.createElement("button");
      fakeBtn.dataset.action = "view-detail";
      fakeBtn.dataset.id = candidateId;
      handleGlobalButton(fakeBtn).catch(err => console.warn(err));
    }
    return;
  }
  if (button.dataset.action === "edit-salary-record") {
    const recordId = button.dataset.id;
    const candidateId = button.dataset.candidateId;
    if (!recordId || !candidateId) throw new Error('参数缺失');
    
    const modal = document.querySelector('[data-salary-tracking-modal]');
    if (!modal) return;
    
    modal.dataset.mode = 'edit';
    modal.dataset.candidateId = candidateId;
    modal.dataset.recordId = recordId;
    
    const titleEl = document.getElementById('salary-modal-title');
    if (titleEl) titleEl.innerHTML = '📝 编辑薪资/福利/入职条件记录';
    
    const roundEl = document.getElementById('salary-interview-round');
    const agreedEl = document.getElementById('salary-agreed-salary');
    const welfareEl = document.getElementById('salary-welfare-desc');
    const onboardEl = document.getElementById('salary-onboard-cond');
    const acceptEl = document.getElementById('salary-candidate-accepted');
    const positionSelect = document.getElementById('salary-position-id');
    
    const list = await window.hrApi.salaryRecords({ candidate_id: Number(candidateId) });
    const rec = list.find(i => String(i.id) === String(recordId));
    if (!rec) throw new Error('未找到该薪资记录');
    
    await populateSalaryPositionOptions({
      positionId: rec.position_id || '',
      positionName: rec.position_name || '',
      companyName: rec.company_name || '',
    });
    if (positionSelect && rec.position_id) positionSelect.value = String(rec.position_id);
    if (agreedEl) agreedEl.value = rec.agreed_salary || '';
    if (welfareEl) welfareEl.value = rec.welfare_desc || '';
    if (onboardEl) onboardEl.value = rec.onboard_cond || '';
    if (acceptEl) acceptEl.value = rec.candidate_accepted || '接受';
    
    if (roundEl) {
      roundEl.innerHTML = '';
      const opt = document.createElement('option');
      opt.value = rec.interview_round || '第1轮';
      opt.textContent = rec.interview_round || '第1轮';
      roundEl.appendChild(opt);
      roundEl.value = rec.interview_round || '第1轮';
      
      if (rec.interview_round) {
        roundEl.disabled = true;
      } else {
        roundEl.disabled = false;
      }
    }
    
    modal.style.display = 'block';
    return;
  }
  if (button.dataset.action === "delete-salary-record") {
    const recordId = button.dataset.id;
    const candidateId = button.dataset.candidateId;
    if (!recordId || !candidateId) throw new Error('参数缺失');
    
    if (!confirm('您确定要删除这条薪资/福利/入职条件跟踪记录吗？')) {
      return;
    }
    
    await window.hrApi.deleteSalaryRecord(Number(recordId));
    showToast('删除薪资记录成功');
    
    const detailModal = document.querySelector('[data-candidate-detail-modal]');
    if (detailModal && detailModal.dataset.candidateId === candidateId) {
      const fakeBtn = document.createElement("button");
      fakeBtn.dataset.action = "view-detail";
      fakeBtn.dataset.id = candidateId;
      handleGlobalButton(fakeBtn).catch(err => console.warn(err));
    }
    return;
  }
  if (button.dataset.action === "open-candidate-employment-modal") {
    const candidateId = String(button.dataset.candidateId || document.querySelector('[data-candidate-edit-modal]')?.dataset.candidateId || document.querySelector('[data-candidate-detail-modal]')?.dataset.candidateId || '');
    if (!candidateId || candidateId === '0') throw new Error('请先选择候选人');
    
    // 如果编辑弹窗打开了，先关闭编辑弹窗
    const editModal = document.querySelector('[data-candidate-edit-modal]');
    if (editModal) editModal.style.display = 'none';
    
    // 模拟点击打开详情弹窗
    const fakeBtn = document.createElement("button");
    fakeBtn.dataset.action = "view-detail";
    fakeBtn.dataset.id = candidateId;
    await handleGlobalButton(fakeBtn);
    
    // 延时等待详情内容渲染完成，然后平滑滚动定位到底部的入职状态卡片
    setTimeout(() => {
      const panel = document.querySelector('[data-detail-employment-panel]');
      if (panel) {
        panel.scrollIntoView({ behavior: 'smooth', block: 'center' });
      }
    }, 120);
    return;
  }
  if (button.dataset.action === "confirm-not-onboard") {
    const panel = document.querySelector('[data-detail-employment-panel]');
    const candidateId = panel?.dataset.candidateId || '';
    if (!candidateId || candidateId === '0') throw new Error('没有待操作的候选人 ID');
    
    const noteArea = document.getElementById('employment-note-textarea');
    const noteVal = noteArea?.value?.trim() || '';
    if (!noteVal) throw new Error('请先填写未入职备注原因');
    
    const payload = {
      candidate_id: Number(candidateId),
      status: "未入职",
      company_name: "",
      position_name: "",
      onboard_date: null,
      note: noteVal
    };
    
    const record = await window.hrApi.createEmploymentRecord(payload);
    
    // 联动刷新候选人生命周期
    const lifecycle = document.querySelector(`[data-lifecycle-events="${candidateId}"]`);
    if (lifecycle) {
      const container = lifecycle.closest('[id^="details-"]');
      if (container) {
        await window.fetchCandidatePanels(candidateId, container);
      }
    }
    
    showToast(`确认未入职状态成功`);
    
    // 联动刷新详情面板
    const detailModal = document.querySelector('[data-candidate-detail-modal]');
    if (detailModal && detailModal.dataset.candidateId === candidateId) {
      const fakeBtn = document.createElement("button");
      fakeBtn.dataset.action = "view-detail";
      fakeBtn.dataset.id = candidateId;
      handleGlobalButton(fakeBtn).catch(err => console.warn(err));
    }
    return;
  }
  if (button.dataset.action === "confirm-onboard") {
    const panel = document.querySelector('[data-detail-employment-panel]');
    const candidateId = panel?.dataset.candidateId || '';
    if (!candidateId || candidateId === '0') throw new Error('没有待操作的候选人 ID');
    
    const position_name = document.getElementById('employment-display-position').textContent;
    const company_name = document.getElementById('employment-display-company').textContent;
    const onboard_date_str = document.getElementById('employment-display-onboard-date').textContent;
    
    if (position_name === '--' || company_name === '--') {
      throw new Error('当前候选人缺少关联岗位或客户公司，请先在薪资/福利/入职条件跟踪表中录入约定薪资记录！');
    }
    
    const payload = {
      candidate_id: Number(candidateId),
      status: "已入职",
      company_name: company_name,
      position_name: position_name,
      onboard_date: new Date(onboard_date_str).toISOString(),
      note: "确认入职"
    };
    
    const record = await window.hrApi.createEmploymentRecord(payload);
    
    // 联动刷新候选人生命周期
    const lifecycle = document.querySelector(`[data-lifecycle-events="${candidateId}"]`);
    if (lifecycle) {
      const container = lifecycle.closest('[id^="details-"]');
      if (container) {
        await window.fetchCandidatePanels(candidateId, container);
      }
    }
    
    showToast(`确认入职成功：${record.company_name}`);
    
    // 联动刷新详情面板
    const detailModal = document.querySelector('[data-candidate-detail-modal]');
    if (detailModal && detailModal.dataset.candidateId === candidateId) {
      const fakeBtn = document.createElement("button");
      fakeBtn.dataset.action = "view-detail";
      fakeBtn.dataset.id = candidateId;
      handleGlobalButton(fakeBtn).catch(err => console.warn(err));
    }
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
    const lifecycle = document.querySelector(`[data-lifecycle-events="${candidateId}"]`);
    if (lifecycle) {
      const records = await window.hrApi.candidateFollowUpRecords({ candidate_id: candidateId });
      const followHtml = records.map(item => `<div class="list-item"><div class="item-top"><div><div class="item-title">${item.follow_up_time || item.created_at}</div><div class="item-meta">${item.content}</div></div><span class="chip primary">${item.status}</span></div></div>`).join('');
      const block = document.querySelector(`[data-tracking-events="${candidateId}"]`);
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
          const updatedItem = {
            ...window.candidatesPageState.list[itemIndex],
            id: result.id,
            locked: result.locked,
            status: result.status
          };
          window.candidatesPageState.list[itemIndex] = updatedItem;
          
          if (window.candidatesPageState.rawList) {
            const rawIndex = window.candidatesPageState.rawList.findIndex(i =>
              String(i.id) === String(result.id) ||
              (i.candidate_agent_id && String(i.candidate_agent_id) === String(result.candidate_agent_id))
            );
            if (rawIndex > -1) {
              window.candidatesPageState.rawList[rawIndex] = {
                ...window.candidatesPageState.rawList[rawIndex],
                id: result.id,
                locked: result.locked,
                status: result.status
              };
            }
          }
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
    const allowed = [".pdf"];
    const name = (file.name || "").toLowerCase();
    if (!allowed.some(ext => name.endsWith(ext))) throw new Error("目前只支持PDF格式的简历文件，请重新上传");
    const result = await window.hrApi.importSmoke(file);
    await window.hrApi.createNotification({
      user: "admin",
      title: `新简历导入：${result.candidate.name}`,
      type: "导入通知",
      content: `${result.candidate.name} 已进入候选人池，来源：${result.candidate.source || "手工导入"}`,
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
    const allowed = [".pdf"];
    const name = (file.name || "").toLowerCase();
    if (!allowed.some(ext => name.endsWith(ext))) throw new Error("目前只支持PDF格式的简历文件，请重新上传");

    // 立刻关闭弹窗
    const modal = document.querySelector('[data-import-modal]');
    if (modal) modal.style.display = "none";

    // 重置选择
    fileInput.value = "";
    const filenameEl = document.querySelector('[data-import-filename]');
    if (filenameEl) filenameEl.textContent = '未选择任何文件';

    showToast("简历正在后台解析导入中，请稍候...");

    // 异步执行接口请求
    window.hrApi.importSmoke(file).then(async (result) => {
      await window.hrApi.createNotification({
        user: "admin",
        title: `新简历导入：${result.candidate?.name || result.duplicate?.name || '未知'}`,
        type: "导入通知",
        content: `${result.candidate?.name || result.duplicate?.name || '未知'} 已进入候选人池，来源：${result.candidate?.source || "手工导入"}`,
        target_path: "./candidates.html",
        read: false,
      });

      if (result.imported === 0 && result.duplicate) {
        showToast(`检测到同名候选人 ${result.duplicate.name}，已写入待复核历史！`);
      } else {
        showToast(`导入成功：${result.candidate.name}`);
      }

      const preview = document.querySelector('[data-import-preview]');
      if (preview) {
        if (result.imported === 0 && result.duplicate) {
          preview.textContent = `导入完成，检测到同名候选人 ${result.duplicate.name}，已存入导入历史等待复核。`;
        } else {
          preview.textContent = `已导入 ${file.name}，候选人 ${result.candidate.name} 已进入数据池，若有同名记录请在导入历史中复核。`;
        }
      }

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

      const snapshot = document.querySelector("[data-candidate-results]");
      if (snapshot && result.candidate) {
        const item = result.candidate;
        snapshot.prepend(Object.assign(document.createElement("div"), { className: "list-item", innerHTML: `<div class="item-top"><div><div class="item-title">${item.name}</div><div class="item-meta">${item.current_title || ""} · ${item.city || ""} · ${item.status || ""}</div></div><span class="chip success">可操作</span></div>` }));
      }
    }).catch(err => {
      showToast(`简历导入解析失败: ${err.message || err}`);
      window.hrApi.importRecords().then(historyItems => {
        const records = document.querySelector(".import-records .timeline");
        if (records) {
          records.innerHTML = historyItems.slice(0, 5).map(i => `<div class="list-item soft"><div class="item-top"><div><div class="item-title">${i.file_name}</div><div class="item-meta">${i.imported_count} 成功 / ${i.failed_count} 失败 · ${i.note}</div></div><span class="tag ${i.status === '成功' ? 'green' : 'blue'}">${i.status}</span></div></div>`).join('');
        }
      });
    });
    return;
  }
  if (button.dataset.action === "confirm-batch-import-upload") {
    const fileInput = document.querySelector('[data-batch-import-files]');
    const files = Array.from(fileInput?.files || []);
    if (!files.length) throw new Error("请先选择一个或多个简历文件");
    const allowed = [".pdf"];
    for (const file of files) {
      const name = (file.name || "").toLowerCase();
      if (!allowed.some(ext => name.endsWith(ext))) throw new Error("目前只支持PDF格式的简历文件，请重新上传");
    }

    // 立刻关闭弹窗
    const modal = document.querySelector('[data-batch-import-modal]');
    if (modal) modal.style.display = "none";

    // 重置选择
    fileInput.value = "";
    const filenameEl = document.querySelector('[data-batch-import-filenames]');
    if (filenameEl) filenameEl.textContent = '未选择任何文件';

    showToast("多份简历正在后台解析导入中，请稍候...");

    // 异步执行接口请求
    window.hrApi.importBatch(files).then(async (result) => {
      await window.hrApi.createNotification({
        user: "admin",
        title: `批量简历导入：${result.imported} 成功`,
        type: "导入通知",
        content: `批量导入完成，成功 ${result.imported}，重复 ${result.duplicates || 0}`,
        target_path: "./import.html",
        read: false,
      });

      showToast(`批量导入完成：成功 ${result.imported} 条` + (result.duplicates ? `，重复 ${result.duplicates} 条` : ''));

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
    }).catch(err => {
      showToast(`批量简历导入失败: ${err.message || err}`);
      window.hrApi.importRecords().then(historyItems => {
        const records = document.querySelector(".import-records .timeline");
        if (records) {
          records.innerHTML = historyItems.slice(0, 5).map(i => `<div class="list-item soft"><div class="item-top"><div><div class="item-title">${i.file_name}</div><div class="item-meta">${i.imported_count} 成功 / ${i.failed_count} 失败 · ${i.note}</div></div><span class="tag ${i.status === '成功' ? 'green' : 'blue'}">${i.status}</span></div></div>`).join('');
        }
      });
    });
    return;
  }
  if (button.dataset.action === "create-company") {
    const modal = document.querySelector('[data-company-modal]');
    if (modal) modal.style.display = 'block';
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
    if (target.kind === 'delete-company') {
      await window.hrApi.deleteCompany(target.id);
      const list = document.querySelector('[data-company-list]');
      if (list) {
        const companies = await window.hrApi.companies();
        if (window.hrRenderCompanyTree) {
          await refreshCustomerTree();
        } else {
          list.innerHTML = renderCompanyListMarkup(companies);
        }
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
    const currentStatus = project?.status || '招聘中';
    const nextStatus = getProjectNextStatus(currentStatus);
    if (modal) {
      modal.style.display = 'block';
      modal.dataset.target = JSON.stringify({ kind: 'toggle-project', id: Number(button.dataset.id) });
    }
    if (title) title.textContent = `项目 ${project?.name || button.dataset.id} 状态变更`;
    if (desc) desc.textContent = `确认后将项目 ${project?.name || button.dataset.id} 从「${currentStatus}」切换为「${nextStatus}」。`;
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
      const list = document.querySelector('[data-project-list]');
      if (list) {
        const projects = await window.hrApi.projects();
        list.innerHTML = window.hrRenderProjectList ? window.hrRenderProjectList(projects) : renderProjectListMarkup(projects);
      }
      if (window.hrRenderCompanyTree && document.querySelector('[data-company-list]')) {
        await refreshCustomerTree();
      }
      showToast(`项目状态已更新：${project.name}`);
    } else if (target.kind === 'delete-project') {
      await window.hrApi.deleteProject(target.id);
      const list = document.querySelector('[data-project-list]');
      if (list) {
        const projects = await window.hrApi.projects();
        list.innerHTML = window.hrRenderProjectList ? window.hrRenderProjectList(projects) : renderProjectListMarkup(projects);
      }
      if (window.hrRenderCompanyTree && document.querySelector('[data-company-list]')) {
        await refreshCustomerTree();
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
      const [items, candidates, positions] = await Promise.all([window.hrApi.evaluations(), window.hrApi.candidates(), window.hrApi.positions()]);
      list.innerHTML = items.slice(0, 3).map(i => {
        const candidate = candidates.find(c => c.id === i.candidate_id);
        const position = positions.find(p => p.id === i.position_id);
        return `<div class="list-item"><div class="item-top"><div><div class="item-title">${candidate?.name || `候选人 ${i.candidate_id}`}</div><div class="item-meta">${position?.name || `岗位 ${i.position_id || '--'}`} · ${i.round_name}</div></div><span class="chip success">${i.grade} · ${i.score} 分</span></div><div class="item-meta">${i.content || '无备注'}</div></div>`;
      }).join('');
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
    const managerId = Number(document.querySelector('[data-user-manager-id]')?.value || 0) || null;
    const password = document.querySelector('[data-user-password]')?.value || 'dev';
    if (!username || !fullName) throw new Error('请先填写用户名和姓名');
    const user = await window.hrApi.createUser({ username, full_name: fullName, role, password_hash: password, manager_user_id: managerId });
    const modal = document.querySelector('[data-user-modal]');
    if (modal) modal.style.display = 'none';
    const list = document.querySelector('[data-user-list]');
    if (list) {
      const items = await window.hrApi.users();
      list.innerHTML = items.map(u => `<div class="list-item"><div class="item-top"><div><div class="item-title">${u.username}</div><div class="item-meta">${u.full_name} · ${u.role}${u.manager_user_id ? ' · 直属组长ID ' + u.manager_user_id : ''}</div></div><div class="table-actions"><button class="btn-sm" data-action="edit-user" data-id="${u.id}">编辑</button><button class="btn-sm" data-action="toggle-user" data-id="${u.id}">${u.is_active ? '停用' : '启用'}</button><button class="btn-sm" data-action="reset-user-password" data-id="${u.id}">重置密码</button></div><span class="chip ${u.is_active ? 'success' : 'neutral'}">${u.is_active ? '启用' : '停用'}</span></div></div>`).join('');
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
    const managerId = document.querySelector('[data-user-edit-manager-id]');
    const active = document.querySelector('[data-user-edit-active]');
    if (username) username.value = user.username;
    if (fullName) fullName.value = user.full_name || '';
    if (role) role.value = user.role || '';
    if (managerId) managerId.value = user.manager_user_id || '';
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
    const managerId = Number(document.querySelector('[data-user-edit-manager-id]')?.value || 0) || null;
    const isActiveText = document.querySelector('[data-user-edit-active]')?.value?.trim() || '';
    if (!fullName || !role) throw new Error('请先填写姓名和角色');
    const user = await window.hrApi.updateUser(target.id, {
      full_name: fullName,
      role,
      manager_user_id: managerId,
      is_active: isActiveText !== '停用',
    });
    const list = document.querySelector('[data-user-list]');
    if (list) {
      const items = await window.hrApi.users();
      list.innerHTML = items.map(u => `<div class="list-item"><div class="item-top"><div><div class="item-title">${u.username}</div><div class="item-meta">${u.full_name} · ${u.role}${u.manager_user_id ? ' · 直属组长ID ' + u.manager_user_id : ''}</div></div><div class="table-actions"><button class="btn-sm" data-action="edit-user" data-id="${u.id}">编辑</button><button class="btn-sm" data-action="toggle-user" data-id="${u.id}">${u.is_active ? '停用' : '启用'}</button><button class="btn-sm" data-action="reset-user-password" data-id="${u.id}">重置密码</button></div><span class="chip ${u.is_active ? 'success' : 'neutral'}">${u.is_active ? '启用' : '停用'}</span></div></div>`).join('');
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
      list.innerHTML = items.map(u => `<div class="list-item"><div class="item-top"><div><div class="item-title">${u.username}</div><div class="item-meta">${u.full_name} · ${u.role}${u.manager_user_id ? ' · 直属组长ID ' + u.manager_user_id : ''}</div></div><div class="table-actions"><button class="btn-sm" data-action="edit-user" data-id="${u.id}">编辑</button><button class="btn-sm" data-action="toggle-user" data-id="${u.id}">${u.is_active ? '停用' : '启用'}</button><button class="btn-sm" data-action="reset-user-password" data-id="${u.id}">重置密码</button></div><span class="chip ${u.is_active ? 'success' : 'neutral'}">${u.is_active ? '启用' : '停用'}</span></div></div>`).join('');
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
        remark,
      }),
    });
    if (modal) modal.style.display = 'none';
    const list = document.querySelector('[data-company-list]');
    if (list) {
      const companies = await window.hrApi.companies();
      if (window.hrRenderCompanyTree) {
        await refreshCustomerTree();
      } else {
        list.innerHTML = renderCompanyListMarkup(companies);
      }
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
    const remark = document.querySelector('[data-company-remark]')?.value?.trim() || '';
    if (!name) throw new Error('请先填写客户名称');
    const company = await window.hrApi.createCompany({
      name,
      contact_name: contactName,
      contact_phone: contactPhone,
      contact_email: contactEmail,
      address,
      cooperation_period: period,
      remark,
    });
    const modal = document.querySelector('[data-company-modal]');
    if (modal) modal.style.display = 'none';
    const list = document.querySelector('[data-company-list]');
    if (list) {
      const companies = await window.hrApi.companies();
      if (window.hrRenderCompanyTree) {
        await refreshCustomerTree();
      } else {
        list.innerHTML = renderCompanyListMarkup(companies);
      }
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
    const companies = await window.hrApi.companies();
    const company = companies.find(c => c.id === Number(item.company_id));
    const modal = document.querySelector('[data-project-edit-modal]');
    if (modal) modal.style.display = 'block';
    document.querySelector('[data-project-edit-company]').value = String(item.company_id || '');
    const companyDisplay = document.querySelector('[data-project-edit-company-display]');
    if (companyDisplay) {
      companyDisplay.textContent = company
        ? `当前客户：${company.name}`
        : `当前客户：${item.company_name || '未知客户'}`;
    }
    document.querySelector('[data-project-edit-name]').value = item.name || '';
    document.querySelector('[data-project-edit-status]').value = item.status || '招聘中';
    document.querySelector('[data-project-edit-level]').value = item.level || '中';
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
    const level = document.querySelector('[data-project-edit-level]')?.value || '中';
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
        work_location: workLocation,
        project_period: period,
        description,
      }),
    });
    if (modal) modal.style.display = 'none';
    if (document.querySelector('[data-project-list]')) {
      await window.refreshTreePage();
    }
    if (document.querySelector('[data-company-list]')) {
      if (window.hrRenderCompanyTree) await refreshCustomerTree();
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
    const level = document.querySelector('[data-project-level]')?.value || '中';
    const workLocation = document.querySelector('[data-project-location]')?.value?.trim() || '';
    const period = document.querySelector('[data-project-period]')?.value?.trim() || '';
    const description = document.querySelector('[data-project-desc]')?.value?.trim() || '';
    if (!companyId || !name) throw new Error('请先选择客户并填写项目名称');
    const project = await window.hrApi.createProject({
      company_id: companyId,
      name,
      status,
      level,
      work_location: workLocation,
      project_period: period,
      description,
    });
    const modal = document.querySelector('[data-project-modal]');
    if (modal) modal.style.display = 'none';
    if (document.querySelector('[data-project-list]')) {
      await window.refreshTreePage();
    }
    if (document.querySelector('[data-company-list]')) {
      if (window.hrRenderCompanyTree) await refreshCustomerTree();
    }
    await refreshProjectMetrics();
    showToast(`已创建项目：${project.name}`);
    return;
  }
  if (button.dataset.action === "open-position-modal") {
    const modal = document.querySelector('[data-position-modal]');
    if (modal) modal.style.display = 'block';
    return;
  }
  if (button.dataset.action === "close-position-modal") {
    const modal = document.querySelector('[data-position-modal]');
    if (modal) modal.style.display = 'none';
    return;
  }
  if (button.dataset.action === "confirm-position-create") {
    const projectId = Number(document.querySelector('[data-position-project]')?.value || 0);
    const name = document.querySelector('[data-position-name]')?.value?.trim() || '';
    const urgency = document.querySelector('[data-position-urgency]')?.value || '中';
    const hiringCount = Number(document.querySelector('[data-position-count]')?.value || 1);
    const salaryMin = Number(document.querySelector('[data-position-salary-min]')?.value || 0) || null;
    const salaryMax = Number(document.querySelector('[data-position-salary-max]')?.value || 0) || null;
    const location = document.querySelector('[data-position-location]')?.value?.trim() || '';
    if (!projectId || !name) throw new Error('请先选择项目并填写岗位名称');
    const position = await window.hrApi.createPosition({
      project_id: projectId,
      name,
      urgency,
      hiring_count: hiringCount,
      salary_min: salaryMin,
      salary_max: salaryMax,
      location,
    });
    const modal = document.querySelector('[data-position-modal]');
    if (modal) modal.style.display = 'none';
    treeState.positionsByProject.delete(projectId);
    if (document.querySelector('[data-company-list]')) {
      if (window.hrRenderCompanyTree) await refreshCustomerTree();
    } else if (document.querySelector('[data-project-list]')) {
      await window.refreshTreePage();
    }
    showToast(`已创建岗位：${position.name}`);
    return;
  }
  if (button.dataset.action === "edit-position") {
    const positions = await window.hrApi.positions();
    const item = positions.find(p => p.id === Number(button.dataset.id));
    if (!item) throw new Error('未找到岗位');
    const projects = await window.hrApi.projects();
    const companies = await window.hrApi.companies();
    const project = projects.find(p => p.id === Number(item.project_id));
    const company = companies.find(c => c.id === Number(project?.company_id));
    const modal = document.querySelector('[data-position-edit-modal]');
    document.querySelector('[data-position-edit-project]').value = String(item.project_id || '');
    const companyDisplay = document.querySelector('[data-position-edit-company-display]');
    if (companyDisplay) {
      companyDisplay.textContent = company && project
        ? `所属公司：${company.name} · ${project.name}`
        : `所属公司：${project?.company_name || '未知公司'} · ${project?.name || '未知项目'}`;
    }
    document.querySelector('[data-position-edit-name]').value = item.name || '';
    document.querySelector('[data-position-edit-urgency]').value = item.urgency || '中';
    document.querySelector('[data-position-edit-count]').value = String(item.hiring_count || 1);
    document.querySelector('[data-position-edit-salary-min]').value = item.salary_min || '';
    document.querySelector('[data-position-edit-salary-max]').value = item.salary_max || '';
    document.querySelector('[data-position-edit-location]').value = item.location || '';
    if (modal) {
      modal.style.display = 'block';
      modal.dataset.target = JSON.stringify({ id: item.id });
    }
    return;
  }
  if (button.dataset.action === "close-position-edit-modal") {
    const modal = document.querySelector('[data-position-edit-modal]');
    if (modal) modal.style.display = 'none';
    return;
  }
  if (button.dataset.action === "confirm-position-edit") {
    const modal = document.querySelector('[data-position-edit-modal]');
    const target = modal?.dataset.target ? JSON.parse(modal.dataset.target) : null;
    if (!target) throw new Error('没有待编辑的岗位');
    const projectId = Number(document.querySelector('[data-position-edit-project]')?.value || 0);
    const name = document.querySelector('[data-position-edit-name]')?.value?.trim() || '';
    const urgency = document.querySelector('[data-position-edit-urgency]')?.value || '中';
    const hiringCount = Number(document.querySelector('[data-position-edit-count]')?.value || 1);
    const salaryMin = Number(document.querySelector('[data-position-edit-salary-min]')?.value || 0) || null;
    const salaryMax = Number(document.querySelector('[data-position-edit-salary-max]')?.value || 0) || null;
    const location = document.querySelector('[data-position-edit-location]')?.value?.trim() || '';
    if (!projectId || !name) throw new Error('请先选择项目并填写岗位名称');
    const position = await window.hrApi.updatePosition(target.id, {
      project_id: projectId,
      name,
      urgency,
      hiring_count: hiringCount,
      salary_min: salaryMin,
      salary_max: salaryMax,
      location,
    });
    if (modal) modal.style.display = 'none';
    treeState.positionsByProject.delete(projectId);
    if (document.querySelector('[data-company-list]')) {
      if (window.hrRenderCompanyTree) await refreshCustomerTree();
    } else if (document.querySelector('[data-project-list]')) {
      await window.refreshTreePage();
    }
    showToast(`岗位已更新：${position.name}`);
    return;
  }
  if (button.dataset.action === "delete-position") {
    const positions = await window.hrApi.positions();
    const item = positions.find(p => p.id === Number(button.dataset.id));
    if (!item) throw new Error('未找到岗位');
    if (!confirm(`确认删除岗位「${item.name}」？删除后会同步清理关联记录。`)) return;
    await window.hrApi.deletePosition(item.id);
    treeState.positionsByProject.delete(item.project_id);
    if (document.querySelector('[data-company-list]')) {
      if (window.hrRenderCompanyTree) await refreshCustomerTree();
    } else if (document.querySelector('[data-project-list]')) {
      await window.refreshTreePage();
    } else {
      const list = document.querySelector('[data-position-list]');
      if (list) {
        const positions = await window.hrApi.positions();
        list.innerHTML = window.hrRenderPositionList ? window.hrRenderPositionList(positions) : '';
      }
    }
    showToast("岗位已删除");
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
    // Tree nodes are replaced after each toggle, so they use the delegated listener below.
    if (btn.dataset.action === "toggle-tree") return;
    if (btn.dataset.bound === "true") return;
    btn.dataset.bound = "true";
    btn.addEventListener("click", (event) => {
      const explicitAction = btn.dataset.action || "";
      if (explicitAction.includes("recruit") || location.pathname.includes("recruit-")) {
        return; // 放行，不执行 preventDefault 和 handleGlobalButton
      }
      event.preventDefault();
      withButtonBusy(btn, () => handleGlobalButton(btn)).catch((err) => showToast(`操作失败：${err.message || err}`));
    });
  });
}

document.addEventListener("click", (event) => {
  const btn = event.target.closest("button");
  if (!btn) return;

  if (btn.dataset.treeToggle) {
    event.preventDefault();
    const targetId = Number(btn.dataset.treeId || 0);
    if (!targetId) return;
    const toggleByLevel = {
      company: window.hrToggleCompanyTree,
      project: window.hrToggleProjectTree,
      position: window.hrTogglePositionTree,
    };
    const toggle = toggleByLevel[btn.dataset.treeToggle];
    if (!toggle) return;
    
    const closeToast = showLoadingToast("正在加载数据...");
    toggle(targetId)
      .then(() => {
        closeToast();
      })
      .catch((err) => {
        closeToast();
        showToast(`操作失败：${err.message || err}`);
      });
    return;
  }

  const explicitAction = btn.dataset.action || "";
  if (explicitAction.includes("recruit") || location.pathname.includes("recruit-")) {
    return;
  }

  const explicitActionCheck = btn.dataset.action;
  if (!explicitActionCheck && !/^(详情|搜索|导入简历|导出选中|选择文件|查看项目进度|进入求职者数据池|查看待办)/.test((btn.textContent || "").trim())) return;
  if (btn.dataset.bound === "true") return;
  event.preventDefault();
  withButtonBusy(btn, () => handleGlobalButton(btn)).catch((err) => showToast(`操作失败：${err.message || err}`));
});

// Sync batch delete button visibility when tree checkboxes change
document.addEventListener("change", (event) => {
  const target = event.target;
  if (target.classList.contains("tree-candidate-checkbox")) {
    // 找到该 checkbox 所属的岗位节点，更新岗位级的批量移除按钮状态
    const positionNode = target.closest('[data-tree-node="position"]');
    if (positionNode) {
      const positionId = positionNode.dataset.id;
      const batchBtn = positionNode.querySelector(`[data-position-batch-delete="${positionId}"]`);
      const checkedInPosition = positionNode.querySelectorAll('.tree-candidate-checkbox:checked').length;
      if (batchBtn) {
        if (checkedInPosition > 0) {
          batchBtn.disabled = false;
          batchBtn.style.opacity = '1';
          batchBtn.style.cursor = 'pointer';
          batchBtn.textContent = `批量移除（${checkedInPosition}）`;
        } else {
          batchBtn.disabled = true;
          batchBtn.style.opacity = '0.4';
          batchBtn.style.cursor = 'not-allowed';
          batchBtn.textContent = '批量移除';
        }
      }
    }
  }
});

document.addEventListener("focusout", (event) => {
  const target = event.target;
  if (!target) return;
  
  if (target.hasAttribute("data-candidate-edit-phone")) {
    const val = target.value.trim();
    if (val && !/^1[3-9]\d{9}$/.test(val)) {
      showToast("手机号格式不正确，请修改");
      target.style.borderColor = "red";
    } else {
      target.style.borderColor = "";
    }
  }
  
  if (target.hasAttribute("data-candidate-edit-idnumber")) {
    const val = target.value.trim();
    if (val && !/(^\d{15}$)|(^\d{18}$)|(^\d{17}(\d|X|x)$)/.test(val)) {
      showToast("身份证格式不正确，请修改");
      target.style.borderColor = "red";
    } else {
      target.style.borderColor = "";
    }
  }
  
  if (target.hasAttribute("data-candidate-edit-email")) {
    const val = target.value.trim();
    if (val && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(val)) {
      showToast("邮箱格式不正确，请修改");
      target.style.borderColor = "red";
    } else {
      target.style.borderColor = "";
    }
  }
});

window.renderApp = render;

window.fetchCandidatePanels = async function(candidateId, container) {
  try {
    const interview = await window.hrApi.interviewRecords({ candidate_id: candidateId });
    const salary = await window.hrApi.salaryRecords({ candidate_id: candidateId });
    const employment = await window.hrApi.employmentRecords({ candidate_id: candidateId });
    const followUps = await window.hrApi.candidateFollowUpRecords({ candidate_id: candidateId });
    
    const trackingList = container.querySelector('[data-tracking-events]');
    const lifecycleList = container.querySelector('[data-lifecycle-events]');
    
    if (lifecycleList) {
      const items = [];
      if (interview[0]) items.push(`<div class="list-item"><div class="item-top"><div><div class="item-title">${interview[0].round_name}</div><div class="item-meta">${interview[0].result} · ${interview[0].interviewer}</div></div><span class="chip success">面试</span></div></div>`);
      if (salary[0]) items.push(`<div class="list-item"><div class="item-top"><div><div class="item-title">薪资</div><div class="item-meta">${salary[0].expected_salary} / ${salary[0].offered_salary}</div></div><span class="chip warning">${salary[0].service_status}</span></div></div>`);
      if (employment[0]) {
        if (employment[0].status === '已入职') {
          items.push(`<div class="list-item"><div class="item-top"><div><div class="item-title">${employment[0].company_name}</div><div class="item-meta">${employment[0].position_name} · 已入职</div></div><span class="chip success">入职</span></div></div>`);
        } else {
          items.push(`<div class="list-item"><div class="item-top"><div><div class="item-title">未入职</div><div class="item-meta">原因：${employment[0].note || '无备注原因'}</div></div><span class="chip neutral">入职</span></div></div>`);
        }
      }
      if (followUps[0]) items.push(`<div class="list-item"><div class="item-top"><div><div class="item-title">随访</div><div class="item-meta">${followUps[0].follow_up_time || followUps[0].created_at} · ${followUps[0].content}</div></div><span class="chip primary">已录用</span></div></div>`);
      lifecycleList.innerHTML = items.join('') || '<div class="list-item"><div class="item-meta">暂无面试、入职等生命周期记录</div></div>';
    }
    
    if (trackingList) {
      trackingList.innerHTML = followUps.map(item => `
        <div class="list-item">
          <div class="item-top">
            <div>
              <div class="item-title">${item.follow_up_time || item.created_at}</div>
              <div class="item-meta">${item.content}</div>
            </div>
            <span class="chip primary">${item.status}</span>
          </div>
        </div>
      `).join('') || '<div class="list-item"><div class="item-meta">暂无跟踪事件记录</div></div>';
    }
  } catch (err) {
    console.warn('Failed to fetch candidate panels:', err);
  }
};

// ----------------------------------------------------
// 推荐岗位弹窗级联选择器监听处理
// ----------------------------------------------------
document.addEventListener("change", async (event) => {
  const target = event.target;
  if (!target) return;
  
  if (target.matches('[data-recommend-company-select]')) {
    const companyId = target.value;
    const projectSelect = document.querySelector('[data-recommend-project-select]');
    const positionSelect = document.querySelector('[data-recommend-position-select]');
    if (!companyId) {
      if (projectSelect) projectSelect.innerHTML = '<option value="">-- 请先选择客户公司 --</option>';
      if (positionSelect) positionSelect.innerHTML = '<option value="">-- 请先选择猎头项目 --</option>';
      return;
    }
    if (projectSelect) projectSelect.innerHTML = '<option value="">加载中...</option>';
    try {
      const projects = await window.hrApi.projects({ company_id: Number(companyId) });
      if (projectSelect) {
        projectSelect.innerHTML = '<option value="">-- 请选择猎头项目 --</option>' +
          projects.map(p => `<option value="${p.id}">${p.name}</option>`).join('');
      }
    } catch (err) {
      if (projectSelect) projectSelect.innerHTML = '<option value="">加载失败</option>';
    }
    if (positionSelect) positionSelect.innerHTML = '<option value="">-- 请先选择猎头项目 --</option>';
  }

  if (target.matches('[data-recommend-project-select]')) {
    const projectId = target.value;
    const positionSelect = document.querySelector('[data-recommend-position-select]');
    if (!projectId) {
      if (positionSelect) positionSelect.innerHTML = '<option value="">-- 请先选择猎头项目 --</option>';
      return;
    }
    if (positionSelect) positionSelect.innerHTML = '<option value="">加载中...</option>';
    try {
      const positions = await window.hrApi.positions({ project_id: Number(projectId) });
      if (positionSelect) {
        positionSelect.innerHTML = '<option value="">-- 请选择招聘岗位 --</option>' +
          positions.map(p => `<option value="${p.id}">${p.name}</option>`).join('');
      }
    } catch (err) {
      if (positionSelect) positionSelect.innerHTML = '<option value="">加载失败</option>';
    }
  }
});
