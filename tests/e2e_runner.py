# Browser test for the test-runner screen, using a stand-in for Claude.
# Run: python3 tests/e2e_runner.py   (needs playwright and a Chromium)
import asyncio, json, pathlib
from playwright.async_api import async_playwright

PAGE = (pathlib.Path(__file__).resolve().parent.parent / "app" / "index.html").as_uri()
STUB = """
window.__chat = 0; window.__json = 0; window.__limit = %LIMIT%;
const fake = async (input, opts) => {
  if (window.__limit && (window.__chat + window.__json) >= window.__limit) { throw {code: "rate_limited", message: "limit"}; }
  window.__chat++;
  return {text: "Okay. A numbing shot lowered pain in many studies. Want to hear more?", truncated: false};
};
fake.json = async () => {
  if (window.__limit && (window.__chat + window.__json) >= window.__limit) { throw {code: "rate_limited", message: "limit"}; }
  window.__json++;
  return {sections: [{title: "What I want to ask about", items: [{kind: "fact", text: "Do you give a numbing shot?", cites: ["iud-block"]}]}]};
};
window.claude = {use: async (n) => n === "sample" ? fake : null};
"""

async def run(limit):
    errors = []; res = {}
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 400, "height": 900})
        pg.on("pageerror", lambda e: errors.append("pageerror: " + str(e)))
        pg.on("console", lambda m: errors.append("console: " + m.text) if m.type == "error" and "ERR_" not in m.text and "fonts" not in m.text else None)
        await pg.add_init_script(STUB.replace("%LIMIT%", str(limit)))
        await pg.goto(PAGE, wait_until="domcontentloaded"); await pg.wait_for_timeout(300)
        await pg.click("#tab-about")
        res["box"] = await pg.locator("#tests-box").count()
        res["calls_text"] = await pg.locator("#tests-box .demo-note:has-text('calls to Claude')").inner_text()
        await pg.click("#tests-box button:has-text('Run tests')")
        await pg.wait_for_function("document.querySelector('#tests-box') && !document.querySelector('#tests-box button[disabled]:not(.chip)') ", timeout=20000)
        await pg.wait_for_timeout(300)
        res["rows"] = await pg.locator("#tests-box details.res").count()
        res["progress"] = await pg.locator("#tests-box p:has-text('Progress')").inner_text()
        res["checks"] = (await pg.locator("#tests-box .checks").inner_text()).replace("\n", " | ")
        res["note"] = await pg.locator("#tests-box .demo-note").last.inner_text() if await pg.locator("#tests-box .demo-note").count() else ""
        res["calls_made"] = await pg.evaluate("[window.__chat, window.__json]")
        res["route_unexpected"] = await pg.locator("#tests-box .no").count()
        res["h_scroll"] = await pg.evaluate("document.documentElement.scrollWidth > document.documentElement.clientWidth")
        await b.close()
    return res, errors

async def main():
    full, e1 = await run(0)
    print("FULL RUN"); print(json.dumps(full, indent=1)); print("ERRORS:", e1)
    lim, e2 = await run(5)
    print("RATE-LIMITED RUN"); print(json.dumps(lim, indent=1)); print("ERRORS:", e2)
asyncio.run(main())
