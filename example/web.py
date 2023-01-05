import PyVutils as vu
# from mechanize import Request

url = "https://cold-dream-9470.bss.design"

# open url in web browser
browser = vu.WebBrowser(headers={"test": "test"})
browser.open(url) # browser.open(Request(url, headers={"test":"test"}))

# print title and forms
print(browser.title())
for form in browser.forms(): print(form)

# register an account
browser.select_form(nr=0)
browser["form-register-user"] = "PyVutils"
browser["form-register-pass"] = "PyVutils@123456"
response = browser.submit()
print("status code =", response.code)
