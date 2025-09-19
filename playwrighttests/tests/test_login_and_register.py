import random
import pytest
from faker import Faker
from playwright.sync_api import Page, expect
from pages.page_actions import PageActions


BASE_URL = "http://frontend.niffler.dc"
username = "username1"
password = "password1"

@pytest.fixture()
def page_actions(page: Page):
    return PageActions(page)

def test_login_with_empty_login(page: Page):
    actions = PageActions(page)
    actions.navigate_to_login()
    actions.login("", "password")
    expect(page).not_to_have_url(BASE_URL + "/main")
    assert page.locator("[name='username']").evaluate("el => el.validity.valueMissing")

def test_login_with_empty_password(page: Page):
    actions = PageActions(page)
    actions.navigate_to_login()
    actions.login("username", "")
    expect(page).not_to_have_url(BASE_URL + "/main")
    assert page.locator("[name='password']").evaluate("el => el.validity.valueMissing")

def test_login_correct(page_actions):
    page_actions.navigate_to_login()
    page_actions.login(username, password)
    expect(page_actions.page).to_have_url(BASE_URL + "/main")

def test_registration_correct(page_actions):
    fake = Faker()
    username = fake.user_name()
    password = fake.password(length=10)
    page_actions.navigate_to_register()
    page_actions.registration(username=username, password=password, submit_password=password)
    expect(page_actions.page.locator(".form")).to_contain_text("Congratulations! You've registered!")

def test_registration_with_wrong_password(page_actions):
    page_actions.navigate_to_register()
    page_actions.navigate_to_register()
    page_actions.registration(username="user123", password="password", submit_password="password123")
    expect(page_actions.page.locator(".form__error")).to_have_text("Passwords should be equal")

def test_logout(page_actions):
    page_actions.navigate_to_login()
    page_actions.login(username, password)
    page_actions.logout()
    expect(page_actions.page.get_by_text("Niffler")).to_be_visible()
    expect(page_actions.page.get_by_role("button", name="Log in")).to_be_visible()

def test_create_new_spending(page_actions):
    amount = str(random.randint(1, 1000000))
    desc = f"autotest_{amount}"

    page_actions.navigate_to_login()
    page_actions.login(username, password)
    page_actions.create_spending(amount, "techno", desc)

    row = page_actions.page.locator("tbody tr", has_text=desc)
    expect(row).to_be_visible()
    expect(row).to_contain_text(amount)

