import asyncio
import time
from playwright.async_api import async_playwright

pages_to_test = [
    "dashboard.html",
    "candidates.html",
    "import.html",
    "customers.html",
    "projects.html",
    "positions.html",
    "evaluations.html",
    "warranty.html",
    "notifications.html",
    "statistics.html",
    "users.html",
    "roles.html",
    "permissions.html",
    "data-permissions.html",
    "dictionary.html",
    "ai-center.html",
    "system-config.html",
    "logs.html"
]

async def run_test():
    async with async_playwright() as p:
        print(">> Launching browser for ALL PAGES E2E test...")
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        errors_found = []

        # Catch console logs to see what's happening
        def handle_console(msg):
            text = msg.text
            if msg.type == 'error':
                # Ignore 404s for API endpoints that might just be missing in MVP, focus on JS crashes
                if "404 (Not Found)" not in text and "detail\":\"Not Found" not in text:
                    print(f"[PAGE ERROR] {text}")
                    errors_found.append(text)

        page.on("console", handle_console)
        page.on("pageerror", lambda err: errors_found.append(f"Uncaught exception: {err}"))

        base_url = "http://127.0.0.1:8000/src/pages"

        try:
            for p_name in pages_to_test:
                print(f"--- Visiting {p_name} ---")
                await page.goto(f"{base_url}/{p_name}")
                
                # Wait for the main app shell to load
                await page.wait_for_selector(".app-shell", state="visible", timeout=10000)
                
                # Wait for a bit to let any async JS execute
                await page.wait_for_timeout(1000)

                # Special interaction for a few key pages to ensure forms work
                if p_name == "system-config.html":
                    await page.click("button[data-action='open-system-config-modal']")
                    await page.wait_for_selector("[data-system-config-modal]", state="visible")
                    await page.fill("[data-system-name-input]", "Test HR System")
                    await page.fill("[data-system-watermark-input]", "Test Watermark")
                    await page.fill("[data-system-logs-input]", "30")
                    await page.click("button[data-action='confirm-system-config-upload']")
                    await page.wait_for_timeout(500)
                elif p_name == "projects.html":
                    await page.click("button[data-action='open-project-modal']")
                    await page.wait_for_selector("[data-project-modal]", state="visible")
                    await page.fill("[data-project-name]", "Auto Project")
                    await page.select_option("[data-project-level]", "A")
                    await page.click("button[data-action='confirm-project-upload']")
                    await page.wait_for_timeout(500)

                if errors_found:
                    print(f"!!! CRASH DETECTED ON {p_name} !!!")
                    break

            if not errors_found:
                print("\n>>> ALL 18 PAGES PASSED SUCCESSFULLY! NO JS CRASHES DETECTED. <<<")
            else:
                print("\n>>> TEST FAILED WITH THE FOLLOWING ERRORS:")
                for e in errors_found:
                    print(e)
                import sys
                sys.exit(1)

        except Exception as e:
            print(f"\n[!] TEST HALTED DUE TO EXCEPTION: {str(e)}")
            await page.screenshot(path="all_pages_error.png")
            print("Saved error screenshot to all_pages_error.png")
            import sys
            sys.exit(1)
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(run_test())
