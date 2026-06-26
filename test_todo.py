"""
Projekt: Automatyzacja testów UI — Playwright / Python
Autor: Maksymilian Tarczyński
Strona testowana: https://demo.playwright.dev/todomvc
Cel: pokrycie 12 krytycznych ścieżek użytkownika testami end-to-end
"""

import pytest
from playwright.sync_api import Page, expect

URL = "https://demo.playwright.dev/todomvc"

@pytest.fixture(autouse=True)
def goto(page: Page):
    page.goto(URL)

def add(page: Page, *texts):
    for text in texts:
        page.locator(".new-todo").fill(text)
        page.locator(".new-todo").press("Enter")


def test_dodaj_nowe_zadanie(page: Page):
    add(page, "Nauczyć się Playwright")
    expect(page.locator(".todo-list li")).to_have_count(1)
    expect(page.locator(".todo-list li")).to_contain_text("Nauczyć się Playwright")

def test_oznacz_jako_wykonane(page: Page):
    add(page, "Napisać raport z testów")
    page.locator(".todo-list li .toggle").click()
    expect(page.locator(".todo-list li.completed")).to_have_count(1)
    expect(page.locator(".todo-count")).to_contain_text("0")

def test_usun_zadanie(page: Page):
    add(page, "Zadanie do usunięcia")
    page.locator(".todo-list li").hover()
    page.locator(".todo-list li .destroy").click()
    expect(page.locator(".todo-list li")).to_have_count(0)

def test_dodaj_wiele_zadan(page: Page):
    add(page, "Zadanie pierwsze", "Zadanie drugie", "Zadanie trzecie")
    expect(page.locator(".todo-list li")).to_have_count(3)
    expect(page.locator(".todo-count")).to_contain_text("3")

def test_filtruj_aktywne(page: Page):
    add(page, "Zadanie aktywne", "Zadanie ukonczone")
    page.locator(".todo-list li").nth(1).locator(".toggle").click()
    page.locator("a", has_text="Active").click()
    expect(page.locator(".todo-list li")).to_have_count(1)
    expect(page.locator(".todo-list li")).to_contain_text("Zadanie aktywne")

def test_filtruj_ukonczone(page: Page):
    add(page, "Zadanie aktywne", "Zadanie ukonczone")
    page.locator(".todo-list li").nth(1).locator(".toggle").click()
    page.locator("a", has_text="Completed").click()
    expect(page.locator(".todo-list li")).to_have_count(1)
    expect(page.locator(".todo-list li")).to_contain_text("Zadanie ukonczone")

def test_wyczysc_ukonczone(page: Page):
    add(page, "Zadanie do wyczyszczenia")
    page.locator(".todo-list li .toggle").click()
    page.locator(".clear-completed").click()
    expect(page.locator(".todo-list li")).to_have_count(0)

def test_oznacz_wszystkie_jako_ukonczone(page: Page):
    add(page, "Zadanie 1", "Zadanie 2", "Zadanie 3")
    page.locator(".toggle-all").click()
    expect(page.locator(".todo-list li.completed")).to_have_count(3)
    expect(page.locator(".todo-count")).to_contain_text("0")

def test_edytuj_zadanie(page: Page):
    add(page, "Stara nazwa zadania")
    page.locator(".todo-list li label").dblclick()
    edit = page.locator(".todo-list li .edit")
    edit.fill("Nowa nazwa zadania")
    edit.press("Enter")
    expect(page.locator(".todo-list li")).to_contain_text("Nowa nazwa zadania")

def test_licznik_zadan(page: Page):
    add(page, "Zadanie A", "Zadanie B", "Zadanie C")
    expect(page.locator(".todo-count")).to_contain_text("3")
    page.locator(".todo-list li").first.locator(".toggle").click()
    expect(page.locator(".todo-count")).to_contain_text("2")

def test_nie_dodaj_pustego_zadania(page: Page):
    page.locator(".new-todo").press("Enter")
    expect(page.locator(".todo-list li")).to_have_count(0)

def test_filtr_all_pokazuje_wszystkie(page: Page):
    add(page, "Aktywne", "Ukonczone")
    page.locator(".todo-list li").nth(1).locator(".toggle").click()
    page.locator("a", has_text="Completed").click()
    page.locator("a", has_text="All").click()
    expect(page.locator(".todo-list li")).to_have_count(2)
