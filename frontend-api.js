window.hrApi = {
  baseUrl: (location.protocol === "file:" || location.port !== "8000") ? "http://127.0.0.1:8000/api" : "/api",
  token: localStorage.getItem("hr_token") || "",
  async request(path, options = {}) {
    const headers = { "Content-Type": "application/json", ...(options.headers || {}) };
    if (this.token) headers.Authorization = `Bearer ${this.token}`;
    const res = await fetch(`${this.baseUrl}${path}`, { ...options, headers });
    if (res.status === 401 && !location.pathname.endsWith("/login.html")) {
      localStorage.removeItem("hr_token");
      location.href = `./login.html?next=${encodeURIComponent(location.pathname.split("/").pop() || "dashboard.html")}`;
      throw new Error("请先登录");
    }
    if (!res.ok) {
      const text = await res.text();
      throw new Error(text || `HTTP ${res.status}`);
    }
    return res.json();
  },
  login(username, password) {
    return this.request("/auth/login", { method: "POST", body: JSON.stringify({ username, password }) });
  },
  logout() {
    return this.request("/auth/logout", { method: "POST" });
  },
  me() {
    return this.request("/me");
  },
  dashboardSummary() {
    return this.request("/dashboard/summary");
  },
  dashboardTodos() {
    return this.request("/dashboard/todos");
  },
  auditLogs(params = {}) {
    const qs = new URLSearchParams(params).toString();
    return this.request(`/audit-logs${qs ? `?${qs}` : ""}`);
  },
  users() {
    return this.request("/users");
  },
  createUser(payload) {
    return this.request("/users", { method: "POST", body: JSON.stringify(payload) });
  },
  updateUser(id, payload) {
    return this.request(`/users/${id}`, { method: "PATCH", body: JSON.stringify(payload) });
  },
  toggleUser(id) {
    return this.request(`/users/${id}/toggle`, { method: "POST" });
  },
  resetUserPassword(id, payload) {
    return this.request(`/users/${id}/reset-password`, { method: "POST", body: JSON.stringify(payload) });
  },
  roles() {
    return this.request("/roles");
  },
  createRole(payload) {
    return this.request("/roles", { method: "POST", body: JSON.stringify(payload) });
  },
  updateRole(id, payload) {
    return this.request(`/roles/${id}`, { method: "PATCH", body: JSON.stringify(payload) });
  },
  toggleRole(id) {
    return this.request(`/roles/${id}/toggle`, { method: "POST" });
  },
  deleteRole(id) {
    return this.request(`/roles/${id}`, { method: "DELETE" });
  },
  companies() {
    return this.request("/companies");
  },
  createCompany(payload) {
    return this.request("/companies", { method: "POST", body: JSON.stringify(payload) });
  },
  updateCompany(id, payload) {
    return this.request(`/companies/${id}`, { method: "PATCH", body: JSON.stringify(payload) });
  },
  deleteCompany(id) {
    return this.request(`/companies/${id}`, { method: "DELETE" });
  },
  projects(params = {}) {
    const qs = new URLSearchParams(params).toString();
    return this.request(`/projects${qs ? `?${qs}` : ""}`);
  },
  createProject(payload) {
    return this.request("/projects", { method: "POST", body: JSON.stringify(payload) });
  },
  updateProject(id, payload) {
    return this.request(`/projects/${id}`, { method: "PATCH", body: JSON.stringify(payload) });
  },
  toggleProject(id) {
    return this.request(`/projects/${id}/toggle`, { method: "POST" });
  },
  deleteProject(id) {
    return this.request(`/projects/${id}`, { method: "DELETE" });
  },
  positions(params = {}) {
    const qs = new URLSearchParams(params).toString();
    return this.request(`/positions${qs ? `?${qs}` : ""}`);
  },
  createPosition(payload) {
    return this.request("/positions", { method: "POST", body: JSON.stringify(payload) });
  },
  updatePosition(id, payload) {
    return this.request(`/positions/${id}`, { method: "PATCH", body: JSON.stringify(payload) });
  },
  deletePosition(id) {
    return this.request(`/positions/${id}`, { method: "DELETE" });
  },
  candidates(params = {}) {
    const qs = new URLSearchParams(params).toString();
    return this.request(`/candidates${qs ? `?${qs}` : ""}`);
  },
  candidate(id) {
    return this.request(`/candidates/${encodeURIComponent(id)}`);
  },
  candidateAiSearch(payload) {
    return this.request("/candidates/ai-search", { method: "POST", body: JSON.stringify(payload) });
  },
  searchPresets() {
    return this.request("/search-presets");
  },
  createSearchPreset(payload) {
    return this.request("/search-presets", { method: "POST", body: JSON.stringify(payload) });
  },
  createCandidate(payload) {
    return this.request("/candidates", { method: "POST", body: JSON.stringify(payload) });
  },
  updateCandidate(id, payload) {
    return this.request(`/candidates/${id}`, { method: "PATCH", body: JSON.stringify(payload) });
  },
  lockCandidate(id) {
    return this.request(`/candidates/${id}/lock`, { method: "POST" });
  },
  releaseCandidate(id) {
    return this.request(`/candidates/${id}/release`, { method: "POST" });
  },
  candidateTrackingEvents(params = {}) {
    const qs = new URLSearchParams(params).toString();
    return this.request(`/candidate-tracking-events${qs ? `?${qs}` : ""}`);
  },
  createCandidateTrackingEvent(payload) {
    return this.request("/candidate-tracking-events", { method: "POST", body: JSON.stringify(payload) });
  },
  updateCandidateTrackingEvent(eventId, payload) {
    return this.request(`/candidate-tracking-events/${eventId}`, { method: "PUT", body: JSON.stringify(payload) });
  },
  deleteCandidateTrackingEvent(eventId) {
    return this.request(`/candidate-tracking-events/${eventId}`, { method: "DELETE" });
  },
  interviewRecords(params = {}) {
    const qs = new URLSearchParams(params).toString();
    return this.request(`/interview-records${qs ? `?${qs}` : ""}`);
  },
  createInterviewRecord(payload) {
    return this.request("/interview-records", { method: "POST", body: JSON.stringify(payload) });
  },
  salaryRecords(params = {}) {
    const qs = new URLSearchParams(params).toString();
    return this.request(`/salary-records${qs ? `?${qs}` : ""}`);
  },
  createSalaryRecord(payload) {
    return this.request("/salary-records", { method: "POST", body: JSON.stringify(payload) });
  },
  updateSalaryRecord(recordId, payload) {
    return this.request(`/salary-records/${recordId}`, { method: "PATCH", body: JSON.stringify(payload) });
  },
  deleteSalaryRecord(recordId) {
    return this.request(`/salary-records/${recordId}`, { method: "DELETE" });
  },
  employmentRecords(params = {}) {
    const qs = new URLSearchParams(params).toString();
    return this.request(`/employment-records${qs ? `?${qs}` : ""}`);
  },
  createEmploymentRecord(payload) {
    return this.request("/employment-records", { method: "POST", body: JSON.stringify(payload) });
  },
  candidateFollowUpRecords(params = {}) {
    const qs = new URLSearchParams(params).toString();
    return this.request(`/candidate-follow-up-records${qs ? `?${qs}` : ""}`);
  },
  createCandidateFollowUpRecord(payload) {
    return this.request("/candidate-follow-up-records", { method: "POST", body: JSON.stringify(payload) });
  },
  candidateMailRecords(params = {}) {
    const qs = new URLSearchParams(params).toString();
    return this.request(`/candidate-mail-records${qs ? `?${qs}` : ""}`);
  },
  createCandidateMailRecord(payload) {
    return this.request("/candidate-mail-records", { method: "POST", body: JSON.stringify(payload) });
  },
  exportRecords(params = {}) {
    const qs = new URLSearchParams(params).toString();
    return this.request(`/export-records${qs ? `?${qs}` : ""}`);
  },
  createExportRecord(payload) {
    return this.request("/export-records", { method: "POST", body: JSON.stringify(payload) });
  },
  importRecords() {
    return this.request("/import-records");
  },
  importBatch(files) {
    const form = new FormData();
    files.forEach((file) => form.append("files", file));
    return fetch(`${this.baseUrl}/imports/batch`, {
      method: "POST",
      headers: { Authorization: `Bearer ${this.token}` },
      body: form,
    }).then(async (res) => {
      if (!res.ok) throw new Error(await res.text());
      return res.json();
    });
  },
  createCandidateNote(payload) {
    return this.request("/candidate-notes", { method: "POST", body: JSON.stringify(payload) });
  },
  candidateNotes(params = {}) {
    const qs = new URLSearchParams(params).toString();
    return this.request(`/candidate-notes${qs ? `?${qs}` : ""}`);
  },
  createRecommendation(payload) {
    return this.request("/recommendations", { method: "POST", body: JSON.stringify(payload) });
  },
  createBatchRecommendations(payload) {
    return this.request("/recommendations/batch", { method: "POST", body: JSON.stringify(payload) });
  },
  deleteRecommendation(id) {
    return this.request(`/recommendations/${id}`, { method: "DELETE" });
  },
  recommendations(params = {}) {
    const qs = new URLSearchParams(params).toString();
    return this.request(`/recommendations${qs ? `?${qs}` : ""}`);
  },
  updateRecommendation(id, payload) {
    return this.request(`/recommendations/${id}`, { method: "PUT", body: JSON.stringify(payload) });
  },
  recommendationFeedbacks(params = {}) {
    const qs = new URLSearchParams(params).toString();
    return this.request(`/recommendation-feedbacks${qs ? `?${qs}` : ""}`);
  },
  createRecommendationFeedback(payload) {
    return this.request("/recommendation-feedbacks", { method: "POST", body: JSON.stringify(payload) });
  },
  createDelivery(payload) {
    return this.request("/deliveries", { method: "POST", body: JSON.stringify(payload) });
  },
  deliveries(params = {}) {
    const qs = new URLSearchParams(params).toString();
    return this.request(`/deliveries${qs ? `?${qs}` : ""}`);
  },
  evaluations(params = {}) {
    const qs = new URLSearchParams(params).toString();
    return this.request(`/evaluations${qs ? `?${qs}` : ""}`);
  },
  createEvaluation(payload) {
    return this.request("/evaluations", { method: "POST", body: JSON.stringify(payload) });
  },
  evaluationLevels() {
    return this.request("/evaluation-levels");
  },
  createEvaluationLevel(payload) {
    return this.request("/evaluation-levels", { method: "POST", body: JSON.stringify(payload) });
  },
  updateEvaluationLevel(id, payload) {
    return this.request(`/evaluation-levels/${id}`, { method: "PUT", body: JSON.stringify(payload) });
  },
  deleteEvaluationLevel(id) {
    return this.request(`/evaluation-levels/${id}`, { method: "DELETE" });
  },
  tags() {
    return this.request("/tags");
  },
  createTag(payload) {
    return this.request("/tags", { method: "POST", body: JSON.stringify(payload) });
  },
  updateTag(id, payload) {
    return this.request(`/tags/${id}`, { method: "PATCH", body: JSON.stringify(payload) });
  },
  deleteTag(id) {
    return this.request(`/tags/${id}`, { method: "DELETE" });
  },
  notifications(params = {}) {
    const qs = new URLSearchParams(params).toString();
    return this.request(`/notifications${qs ? `?${qs}` : ""}`);
  },
  createNotification(payload) {
    return this.request("/notifications", { method: "POST", body: JSON.stringify(payload) });
  },
  readNotification(id) {
    return this.request(`/notifications/${id}/read`, { method: "POST" });
  },
  batchReadNotifications(ids) {
    return this.request("/notifications/batch-read", { method: "PATCH", body: JSON.stringify(ids) });
  },
  warrantyRules() {
    return this.request("/warranty-rules");
  },
  createWarrantyRule(payload) {
    return this.request("/warranty-rules", { method: "POST", body: JSON.stringify(payload) });
  },
  updateWarrantyRule(id, payload) {
    return this.request(`/warranty-rules/${id}`, { method: "PUT", body: JSON.stringify(payload) });
  },
  deleteWarrantyRule(id) {
    return this.request(`/warranty-rules/${id}`, { method: "DELETE" });
  },
  analyticsSummary() {
    return this.request("/analytics/summary");
  },
  systemConfigs() {
    return this.request("/system-configs");
  },
  saveSystemConfig(payload) {
    return this.request("/system-configs", { method: "POST", body: JSON.stringify(payload) });
  },
  emailConfig() {
    return this.request("/email-config");
  },
  saveEmailConfig(payload) {
    return this.request("/email-config", { method: "POST", body: JSON.stringify(payload) });
  },
  testEmailConfig(payload) {
    return this.request("/email-config/test", { method: "POST", body: JSON.stringify(payload) });
  },
  aiTasks() {
    return this.request("/ai/tasks");
  },
  createAiTask(payload) {
    return this.request("/ai/tasks", { method: "POST", body: JSON.stringify(payload) });
  },
  rolePermissions(params = {}) {
    const qs = new URLSearchParams(params).toString();
    return this.request(`/role-permissions${qs ? `?${qs}` : ""}`);
  },
  saveRolePermission(payload) {
    return this.request("/role-permissions", { method: "POST", body: JSON.stringify(payload) });
  },
  dataPermissions(params = {}) {
    const qs = new URLSearchParams(params).toString();
    return this.request(`/data-permissions${qs ? `?${qs}` : ""}`);
  },
  saveDataPermission(payload) {
    return this.request("/data-permissions", { method: "POST", body: JSON.stringify(payload) });
  },
  candidateOwnershipTransfers(params = {}) {
    const qs = new URLSearchParams(params).toString();
    return this.request(`/candidate-ownership-transfers${qs ? `?${qs}` : ""}`);
  },
  createCandidateOwnershipTransfer(payload) {
    return this.request("/candidate-ownership-transfers", { method: "POST", body: JSON.stringify(payload) });
  },
  approveCandidateOwnershipTransfer(id, payload = {}) {
    return this.request(`/candidate-ownership-transfers/${id}/approve`, { method: "POST", body: JSON.stringify(payload) });
  },
  importSmoke(file) {
    const form = new FormData();
    form.append("file", file);
    return fetch(`${this.baseUrl}/imports/smoke`, {
      method: "POST",
      headers: { Authorization: `Bearer ${this.token}` },
      body: form,
    }).then(async (res) => {
      if (!res.ok) throw new Error(await res.text());
      return res.json();
    });
  },
  recruitCandidates(params = {}) {
    const qs = new URLSearchParams(params).toString();
    return this.request(`/recruit/candidates${qs ? `?${qs}` : ""}`);
  },
  recruitEmployees() {
    return this.request("/recruit/employees");
  },
  recruitJobPostings(params = {}) {
    const qs = new URLSearchParams(params).toString();
    return this.request(`/recruit/job-postings${qs ? `?${qs}` : ""}`);
  },
  createRecruitJobPosting(payload) {
    return this.request("/recruit/job-postings", { method: "POST", body: JSON.stringify(payload) });
  },
  updateRecruitJobPosting(id, payload) {
    return this.request(`/recruit/job-postings/${id}`, { method: "PATCH", body: JSON.stringify(payload) });
  },
  deleteRecruitJobPosting(id) {
    return this.request(`/recruit/job-postings/${id}`, { method: "DELETE" });
  },
  recruitDailyTaskStats(params = {}) {
    const qs = new URLSearchParams(params).toString();
    return this.request(`/recruit/daily-task-stats${qs ? `?${qs}` : ""}`);
  },
  downloadRecruitResume(agentId) {
    return fetch(`${this.baseUrl}/recruit/resumes/${agentId}/download`, {
      headers: { Authorization: `Bearer ${this.token}` }
    }).then(async (res) => {
      if (!res.ok) throw new Error(await res.text());
      return res.blob();
    });
  },
  dbTables() {
    return this.request("/db-tables");
  },
  dbTableData(tableName, params = {}) {
    const limit = params.limit || 100;
    return this.request(`/db-tables?table_name=${tableName}&limit=${limit}`);
  },
};
