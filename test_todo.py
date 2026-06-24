"""
Projekt: Automatyzacja testów UI — Playwright / Python
Autor: Maksymilian Tarczyński
Strona testowana: https://demo.playwright.dev/todomvc
Cel: pokrycie 3 krytycznych ścieżek użytkownika testami end-to-end
"""

import pytest
from playwright.sync_api import Page, expect


# ─────────────────────────────────────────────
# ŚCIEŻKA 1: Dodawanie nowego zadania
# ─────────────────────────────────────────────
def test_dodaj_nowe_zadanie(page: Page):
    """
    Użytkownik wchodzi na stronę i dodaje nowe zadanie.
    Sprawdzamy czy zadanie pojawia się na liście.
    """
    # Otwieramy aplikację
    page.goto("https://demo.playwright.dev/todomvc")

    # Wpisujemy nazwę zadania w pole tekstowe
    page.locator(".new-todo").fill("Nauczyć się Playwright")

    # Zatwierdzamy klawiszem Enter
    page.locator(".new-todo").press("Enter")

    # Sprawdzamy czy zadanie pojawiło się na liście
    todo_item = page.locator(".todo-list li")
    expect(todo_item).to_have_count(1)
    expect(todo_item).to_contain_text("Nauczyć się Playwright")


# ─────────────────────────────────────────────
# ŚCIEŻKA 2: Oznaczanie zadania jako wykonane
# ─────────────────────────────────────────────
def test_oznacz_zadanie_jako_wykonane(page: Page):
    """
    Użytkownik dodaje zadanie, a następnie oznacza je jako ukończone.
    Sprawdzamy czy zadanie otrzymuje status 'completed'.
    """
    page.goto("https://demo.playwright.dev/todomvc")

    # Dodajemy zadanie
    page.locator(".new-todo").fill("Napisać raport z testów")
    page.locator(".new-todo").press("Enter")

    # Klikamy checkbox przy zadaniu (oznaczamy jako done)
    page.locator(".todo-list li .toggle").click()

    # Sprawdzamy czy zadanie ma klasę 'completed'
    completed_item = page.locator(".todo-list li.completed")
    expect(completed_item).to_have_count(1)

    # Sprawdzamy licznik w stopce — powinien pokazywać "0 items left"
    expect(page.locator(".todo-count")).to_contain_text("0")


# ─────────────────────────────────────────────
# ŚCIEŻKA 3: Usuwanie zadania
# ─────────────────────────────────────────────
def test_usun_zadanie(page: Page):
    """
    Użytkownik dodaje zadanie, a następnie je usuwa.
    Sprawdzamy czy lista jest pusta po usunięciu.
    """
    page.goto("https://demo.playwright.dev/todomvc")

    # Dodajemy zadanie które zaraz usuniemy
    page.locator(".new-todo").fill("Zadanie do usunięcia")
    page.locator(".new-todo").press("Enter")

    # Najeżdżamy myszką na zadanie żeby pojawił się przycisk usuń (X)
    page.locator(".todo-list li").hover()

    # Klikamy przycisk usuń
    page.locator(".todo-list li .destroy").click()

    # Sprawdzamy czy lista jest teraz pusta
    expect(page.locator(".todo-list li")).to_have_count(0)
