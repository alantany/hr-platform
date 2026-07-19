import { chromium } from "playwright";
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, "..");
const OUT = path.join(ROOT, "outputs/manual-screenshots");
const BASE = "http://127.0.0.1:8000";

const pages = [
  { file: "06-01-login.png", path: "/src/pages/login.html", skipAuth: true },
  { file: "06-02-dashboard.png", path: "/src/pages/dashboard.html" },
  { file: "06-03-customers.png", path: "/src/pages/customers.html" },
  { file: "06-04-projects.png", path: "/src/pages/projects.html" },
  {
    file: "06-04-positions.png",
    path: "/src/pages/projects.html",
    after: async (page) => {
      const tab = page.locator('button, a, [role="tab"]').filter({ hasText: "岗位列表" }).first();
      if (await tab.count()) {
        await tab.click();
        await page.waitForTimeout(800);
      }
    },
  },
  { file: "06-05-position-candidates.png", path: "/src/pages/position-candidates.html?position_id=1207" },
  { file: "06-06-candidates.png", path: "/src/pages/candidates.html" },
  { file: "06-07-import.png", path: "/src/pages/import.html" },
  { file: "06-08-evaluations.png", path: "/src/pages/evaluations.html" },
  { file: "06-09-warranty.png", path: "/src/pages/warranty.html" },
  { file: "06-10-statistics.png", path: "/src/pages/statistics.html" },
  { file: "06-11-position-tasks.png", path: "/src/pages/notifications.html?tab=position-tasks" },
  {
    file: "06-11-notifications.png",
    path: "/src/pages/notifications.html",
    after: async (page) => {
      const tab = page.locator('button, a, [role="tab"]').filter({ hasText: /通知|消息/ }).first();
      if (await tab.count()) {
        await tab.click();
        await page.waitForTimeout(600);
      }
    },
  },
  { file: "06-12-recruit-publish.png", path: "/src/pages/recruit-job-publish.html" },
  { file: "06-12-recruit-list.png", path: "/src/pages/recruit-job-list.html" },
  { file: "06-12-recruit-daily.png", path: "/src/pages/recruit-daily-tasks.html" },
  { file: "06-13-users.png", path: "/src/pages/users.html" },
  { file: "06-14-roles.png", path: "/src/pages/roles.html" },
  { file: "06-15-permissions.png", path: "/src/pages/permissions.html" },
  { file: "06-16-data-permissions.png", path: "/src/pages/data-permissions.html" },
  { file: "06-17-dictionary.png", path: "/src/pages/dictionary.html" },
  { file: "06-18-logs.png", path: "/src/pages/logs.html" },
  { file: "06-19-ai-center.png", path: "/src/pages/ai-center.html" },
  { file: "06-20-system-config.png", path: "/src/pages/system-config.html" },
  { file: "06-21-settings.png", path: "/src/pages/settings.html" },
  { file: "06-22-db-explorer.png", path: "/src/pages/db-explorer.html" },
  { file: "06-22-ui-kit.png", path: "/src/pages/ui-kit.html" },
];

fs.mkdirSync(OUT, { recursive: true });

const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({
  viewport: { width: 1440, height: 900 },
  deviceScaleFactor: 1,
});
const page = await context.newPage();

async function login() {
  const res = await page.request.post(`${BASE}/api/auth/login`, {
    data: { username: "admin", password: "admin123" },
  });
  const json = await res.json();
  if (!json.access_token) throw new Error(`login failed: ${JSON.stringify(json)}`);
  await page.goto(`${BASE}/src/pages/login.html`, { waitUntil: "domcontentloaded" });
  await page.evaluate((token) => localStorage.setItem("hr_token", token), json.access_token);
  return json.access_token;
}

await login();

const results = [];
for (const item of pages) {
  const outPath = path.join(OUT, item.file);
  try {
    if (!item.skipAuth) {
      const token = await page.evaluate(() => localStorage.getItem("hr_token"));
      if (!token) await login();
    }
    await page.goto(`${BASE}${item.path}`, { waitUntil: "networkidle", timeout: 60000 });
    await page.waitForTimeout(1200);
    if (page.url().includes("login.html") && !item.skipAuth) {
      await login();
      await page.goto(`${BASE}${item.path}`, { waitUntil: "networkidle", timeout: 60000 });
      await page.waitForTimeout(1200);
    }
    if (item.after) await item.after(page);
    await page.screenshot({ path: outPath, fullPage: true });
    const size = fs.statSync(outPath).size;
    results.push({ file: item.file, ok: true, size });
    console.log(`OK ${item.file} (${size} bytes)`);
  } catch (err) {
    results.push({ file: item.file, ok: false, error: String(err) });
    console.error(`FAIL ${item.file}: ${err}`);
  }
}

await browser.close();
const ok = results.filter((r) => r.ok).length;
const fail = results.filter((r) => !r.ok);
console.log(JSON.stringify({ ok, failCount: fail.length, fail }, null, 2));
process.exit(fail.length ? 1 : 0);
