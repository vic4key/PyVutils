import PyVutils as vu

browser = vu.web_browser(headers={"test": "test"})
browser.open("https://cold-dream-9470.bss.design")
print(browser.title())
for form in browser.forms(): print(form)