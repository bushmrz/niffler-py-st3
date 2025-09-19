from playwright.sync_api import Page

class PageActions:
    def __init__(self, page: Page):
        self.page = page

    def navigate_to_login(self):
        self.page.goto("http://frontend.niffler.dc/login")

    def navigate_to_register(self):
        self.page.goto("http://frontend.niffler.dc/login")
        self.page.locator(".form__register").click()


    def login(self, username: str, password: str):
        self.page.locator("[name='username']").fill(username)
        self.page.locator("[name='password']").fill(password)
        self.page.get_by_role("button", name="Log in").click()

    def logout(self):
        self.page.get_by_test_id("PersonIcon").click()
        self.page.get_by_text("Sign out").click()
        self.page.get_by_text("Log out").click()

    def registration(self, username: str, password: str, submit_password: str):
        self.page.locator("[name='username']").fill(username)
        self.page.locator("[name='password']").fill(password)
        self.page.locator("[name='passwordSubmit']").fill(submit_password)

        self.page.get_by_role("button", name="Sign up").click()

    def create_spending(self, amount: str, category: str, description: str):
        self.page.get_by_text("New spending").click()
        self.page.locator("#amount").fill(amount)
        self.page.locator("#category").fill(category)
        self.page.locator("#description").fill(description)
        self.page.locator("#save").click()