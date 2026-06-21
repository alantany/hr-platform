import asyncio
from playwright.async_api import async_playwright

async def main():
    try:
        async with async_playwright() as p:
            print("Launching browser...")
            browser = await p.chromium.launch(headless=True)
            print("Browser launched. Opening page...")
            page = await browser.new_page()
            # Just test if the browser works, we don't need a real server for the headless test
            await page.goto('https://example.com', timeout=10000)
            print("Title:", await page.title())
            await browser.close()
            print("Browser closed successfully.")
    except Exception as e:
        print(f"Error: {e}")

asyncio.run(main())
