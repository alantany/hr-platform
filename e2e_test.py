import asyncio
import time
from playwright.async_api import async_playwright

async def run_test():
    async with async_playwright() as p:
        print(">> Launching browser...")
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        # Catch console logs to see what's happening
        page.on("console", lambda msg: print(f"Browser Console: {msg.text}"))

        base_url = "http://127.0.0.1:8000/src/pages"

        try:
            # ----------------------------------------------------
            # Scenario A: Customers & Projects
            # ----------------------------------------------------
            print("\n[A] Testing Customer Creation")
            await page.goto(f"{base_url}/customers.html")
            await page.wait_for_selector("button[data-action='open-company-modal']")
            
            # Open create modal
            await page.click("button[data-action='open-company-modal']")
            await page.wait_for_selector("[data-company-modal]", state="visible")
            
            # Fill form
            test_company_name = f"Playwright Test Corp {int(time.time())}"
            await page.fill("[data-company-name]", test_company_name)
            await page.fill("[data-company-contact]", "Auto Tester")
            await page.fill("[data-company-phone]", "13800138000")
            
            # Submit
            await page.click("button[data-action='confirm-company-upload']")
            
            # Wait for list to update (the modal should hide and the name should appear in the list)
            print(">> Waiting for UI to refresh with new company...")
            await page.wait_for_selector(f"text='{test_company_name}'", timeout=5000)
            print(">> Customer Creation OK")

            # ----------------------------------------------------
            # Scenario B: Candidates Creation and Detail
            # ----------------------------------------------------
            print("\n[B] Testing Candidate Creation")
            await page.goto(f"{base_url}/candidates.html")
            await page.wait_for_selector("button[data-action='open-candidate-create-modal']")
            
            await page.click("button[data-action='open-candidate-create-modal']")
            await page.wait_for_selector("[data-candidate-create-modal]", state="visible")
            
            test_candidate_name = f"Auto Candidate {int(time.time())}"
            await page.fill("[data-candidate-name]", test_candidate_name)
            await page.fill("[data-candidate-phone]", "13900139000")
            await page.fill("[data-candidate-title]", "Software Engineer")
            
            await page.click("button[data-action='confirm-candidate-create']")
            
            print(">> Waiting for Candidate List to update...")
            await page.wait_for_selector(f"text='{test_candidate_name}'", timeout=5000)
            print(">> Candidate Creation OK")
            
            # ----------------------------------------------------
            # Details Test
            # ----------------------------------------------------
            print("\n[C] Testing Candidate Detail View")
            # We just created the candidate, its detail button should be available
            # Find the view-detail button for the newly created candidate
            # `data-title` is used in the button
            await page.click(f"button[data-action='view-detail'][data-title='{test_candidate_name}']")
            
            print(">> Waiting for Detail Modal...")
            await page.wait_for_selector("[data-candidate-detail-modal]", state="visible")
            
            # Check if name is rendered
            detail_name = await page.locator("[data-candidate-detail-name]").inner_text()
            assert detail_name == test_candidate_name, f"Detail name mismatch: {detail_name}"
            print(">> Candidate Detail Render OK")

            print("\n>>> ALL TESTS PASSED SUCCESSFULLY! <<<")

        except Exception as e:
            print(f"\n[!] TEST FAILED: {str(e)}")
            await page.screenshot(path="error_screenshot.png")
            print("Saved error screenshot to error_screenshot.png")
            import sys
            sys.exit(1)
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(run_test())
