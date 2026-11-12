# Browser test for the page. Needs: pip install playwright (and a Chromium). Run: python3 tests/e2e.py
# It checks the click-through demo mode and the live mode (with a stand-in for Claude), and prints results to read by eye.
import asyncio, json
from playwright.async_api import async_playwright
import pathlib
PAGE = (pathlib.Path(__file__).resolve().parent.parent / "app" / "index.html").as_uri()
LIVE = """
const fake = async (input, opts) => { const r = "Okay. A numbing shot lowered pain in many studies. Want to hear more?"; if (opts && opts.onText) opts.onText({text: r, delta: r}); return {text: r, truncated: false}; };
fake.json = async () => ({sections: [{title: "What I want to ask about", items: [{kind: "fact", text: "Do you give a numbing shot?", cites: ["iud-block"]}]}]});
window.claude = {use: async (n) => n === "sample" ? fake : null};
"""
async def main():
    errors = []; res = {}
    async with async_playwright() as p:
        b = await p.chromium.launch()
        def watch(pg):
            pg.on("pageerror", lambda e: errors.append("pageerror: " + str(e)))
            pg.on("console", lambda m: errors.append("console: " + m.text) if m.type == "error" and "ERR_" not in m.text and "fonts" not in m.text else None)
        # ---- demo mode (no claude)
        pg = await b.new_page(viewport={"width": 400, "height": 900}); watch(pg)
        await pg.goto(PAGE, wait_until="domcontentloaded"); await pg.wait_for_timeout(300)
        res["tag"] = await pg.locator("#tag").inner_text()
        res["learn_banner"] = await pg.locator("#panel-learn .note:has-text('Click-through demo')").count()
        await pg.click("#tab-chat")
        res["demo_banner"] = await pg.locator("#panel-chat .note:has-text('Demo mode')").count()
        res["plan_disabled_at_start"] = await pg.locator("button:has-text('Make my plan')").is_disabled()
        res["textarea_hidden"] = await pg.locator("#msg-box").count() == 0
        for msg in ["I am worried about the pain", "Can I be asleep for it?", "I want to be able to stop if I need to"]:
            await pg.click(f"button.chip:has-text('{msg}')")
            await pg.wait_for_selector(f".bubble.bot:not(.wait)", timeout=3000)
            await pg.wait_for_function("!document.querySelector('.bubble.wait')")
        res["bubbles"] = await pg.locator(".bubble").count()
        res["plan_enabled_after"] = not await pg.locator("button:has-text('Make my plan')").is_disabled()
        await pg.click("button:has-text('Make my plan')")
        await pg.wait_for_selector(".sheet")
        res["good_checks"] = (await pg.locator(".checks").inner_text()).replace("\n", " | ")
        await pg.click("button:has-text('Show what the checks catch')")
        await pg.wait_for_selector(".note:has-text('Test example')")
        res["trap_checks"] = (await pg.locator(".checks").inner_text()).replace("\n", " | ")
        res["trap_sheet_has_800"] = "800" in await pg.locator(".sheet").inner_text()
        res["flag"] = await pg.locator(".flag").count()
        await pg.click("button:has-text('Back to the example plan')")
        # guardrails
        await pg.click("button.chip:has-text('How much medicine should I take?')")
        await pg.wait_for_function("!document.querySelector('.bubble.wait')")
        res["decline"] = await pg.locator(".bubble.bot:has-text('does not give medicine amounts')").count()
        await pg.click("button.chip:has-text('I have heavy bleeding')")
        res["urgent"] = await pg.locator(".bubble.sys:has-text('911')").count()
        # cervical
        await pg.click("button.mod:has-text('Cervical')")
        for msg in ["How often do I need this?", "Can I do the test myself?", "What if my result is not normal?"]:
            await pg.click(f"button.chip:has-text('{msg}')")
            await pg.wait_for_function("!document.querySelector('.bubble.wait')")
        await pg.click("button:has-text('Make my plan')"); await pg.wait_for_selector(".sheet")
        res["cx_checks"] = (await pg.locator(".checks").inner_text()).replace("\n", " | ")
        await pg.click("#tab-about")
        res["about_demo_note"] = await pg.locator("#panel-about .note:has-text('demo version')").count()
        res["h_scroll"] = await pg.evaluate("document.documentElement.scrollWidth > document.documentElement.clientWidth")
        # ---- live mode (stub) regression
        pg2 = await b.new_page(viewport={"width": 400, "height": 900}); watch(pg2)
        await pg2.add_init_script(LIVE)
        await pg2.goto(PAGE, wait_until="domcontentloaded"); await pg2.wait_for_timeout(300)
        res["live_tag"] = await pg2.locator("#tag").inner_text()
        await pg2.click("#tab-chat")
        res["live_textarea"] = await pg2.locator("#msg-box").count()
        res["live_no_demo_banner"] = await pg2.locator(".note:has-text('Demo mode')").count()
        await pg2.click("button.chip:has-text('I am worried about the pain')")
        await pg2.wait_for_selector(".bubble.bot:has-text('numbing shot')")
        await pg2.click("button:has-text('Make my plan')"); await pg2.wait_for_selector(".sheet")
        res["live_plan"] = (await pg2.locator(".checks").inner_text()).replace("\n", " | ")
        await b.close()
    print(json.dumps(res, indent=1)); print("ERRORS:", errors)
asyncio.run(main())
