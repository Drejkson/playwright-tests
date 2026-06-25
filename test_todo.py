"""
Projekt: Automatyzacja testów UI — Playwright / Python
Autor: Maksymilian Tarczyński
Strona testowana: https://demo.playwright.dev/todomvc
Cel: pokrycie 12 krytycznych ścieżek użytkownika testami end-to-end
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


# ─────────────────────────────────────────────
# ŚCIEŻKA 4: Dodawanie wielu zadań
# ─────────────────────────────────────────────
def test_dodaj_wiele_zadan(page: Page):
    """
    Użytkownik dodaje 3 zadania jedno po drugim.
    Sprawdzamy czy wszystkie pojawiają się na liście i licznik jest poprawny.
    """
    page.goto("https://demo.playwright.dev/todomvc")

    zadania = ["Zadanie pierwsze", "Zadanie drugie", "Zadanie trzecie"]
    for zadanie in zadania:
        page.locator(".new-todo").fill(zadanie)
        page.locator(".new-todo").press("Enter")

    # Na liście powinny być 3 elementy
    expect(page.locator(".todo-list li")).to_have_count(3)

    # Licznik pokazuje "3 items left"
    expect(page.locator(".todo-count")).to_contain_text("3")


# ─────────────────────────────────────────────
# ŚCIEŻKA 5: Filtrowanie — tylko aktywne zadania
# ─────────────────────────────────────────────
def test_filtruj_aktywne(page: Page):
    """
    Użytkownik dodaje 2 zadania, jedno oznacza jako done,
    a następnie filtruje listę by widzieć tylko aktywne.
    """
    page.goto("https://demo.playwright.dev/todomvc")

    # Dodajemy 2 zadania
    page.locator(".new-todo").fill("Zadanie aktywne")
    page.locator(".new-todo").press("Enter")
    page.locator(".new-todo").fill("Zadanie ukonczone")
    page.locator(".new-todo").press("Enter")

    # Drugie zadanie oznaczamy jako done
    page.locator(".todo-list li").nth(1).locator(".toggle").click()

    # Klikamy filtr "Active"
    page.locator("a", has_text="Active").click()

    # Powinno być widoczne tylko 1 aktywne zadanie
    expect(page.locator(".todo-list li")).to_have_count(1)
    expect(page.locator(".todo-list li")).to_contain_text("Zadanie aktywne")


# ─────────────────────────────────────────────
# ŚCIEŻKA 6: Filtrowanie — tylko ukończone zadania
# ─────────────────────────────────────────────
def test_filtruj_ukonczone(page: Page):
    """
    Użytkownik filtruje listę by widzieć tylko ukończone zadania.
    """
    page.goto("https://demo.playwright.dev/todomvc")

    page.locator(".new-todo").fill("Zadanie aktywne")
    page.locator(".new-todo").press("Enter")
    page.locator(".new-todo").fill("Zadanie ukonczone")
    page.locator(".new-todo").press("Enter")

    # Oznaczamy drugie zadanie jako done
    page.locator(".todo-list li").nth(1).locator(".toggle").click()

    # Klikamy filtr "Completed"
    page.locator("a", has_text="Completed").click()

    # Powinno być widoczne tylko 1 ukończone zadanie
    expect(page.locator(".todo-list li")).to_have_count(1)
    expect(page.locator(".todo-list li")).to_contain_text("Zadanie ukonczone")


# ─────────────────────────────────────────────
# ŚCIEŻKA 7: Czyszczenie ukończonych zadań
# ─────────────────────────────────────────────
def test_wyczysc_ukonczone(page: Page):
    """
    Użytkownik oznacza zadanie jako done i klika 'Clear completed'.
    Sprawdzamy czy ukończone zadania znikają z listy.
    """
    page.goto("https://demo.playwright.dev/todomvc")

    page.locator(".new-todo").fill("Zadanie do wyczyszczenia")
    page.locator(".new-todo").press("Enter")

    # Oznaczamy jako done
    page.locator(".todo-list li .toggle").click()

    # Klikamy "Clear completed"
    page.locator(".clear-completed").click()

    # Lista powinna być pusta
    expect(page.locator(".todo-list li")).to_have_count(0)


# ─────────────────────────────────────────────
# ŚCIEŻKA 8: Oznacz wszystkie jako ukończone
# ─────────────────────────────────────────────
def test_oznacz_wszystkie_jako_ukonczone(page: Page):
    """
    Użytkownik klika 'toggle all' żeby oznaczyć wszystkie zadania naraz.
    """
    page.goto("https://demo.playwright.dev/todomvc")

    # Dodajemy 3 zadania
    for tekst in ["Zadanie 1", "Zadanie 2", "Zadanie 3"]:
        page.locator(".new-todo").fill(tekst)
        page.locator(".new-todo").press("Enter")

    # Klikamy toggle-all (strzałka w dół przy polu tekstowym)
    page.locator(".toggle-all").click()

    # Wszystkie 3 powinny mieć status completed
    expect(page.locator(".todo-list li.completed")).to_have_count(3)

    # Licznik powinien pokazywać 0
    expect(page.locator(".todo-count")).to_contain_text("0")


# ─────────────────────────────────────────────
# ŚCIEŻKA 9: Edytowanie istniejącego zadania
# ─────────────────────────────────────────────
def test_edytuj_zadanie(page: Page):
    """
    Użytkownik dwukrotnie klika zadanie, zmienia jego treść i zatwierdza.
    """
    page.goto("https://demo.playwright.dev/todomvc")

    page.locator(".new-todo").fill("Stara nazwa zadania")
    page.locator(".new-todo").press("Enter")

    # Dwuklik uruchamia tryb edycji
    page.locator(".todo-list li label").dblclick()

    # Czyścimy pole i wpisujemy nową nazwę
    edit_field = page.locator(".todo-list li .edit")
    edit_field.fill("Nowa nazwa zadania")
    edit_field.press("Enter")

    # Sprawdzamy że zadanie ma nową nazwę
    expect(page.locator(".todo-list li")).to_contain_text("Nowa nazwa zadania")


# ─────────────────────────────────────────────
# ŚCIEŻKA 10: Licznik zadań aktualizuje się poprawnie
# ─────────────────────────────────────────────
def test_licznik_zadan(page: Page):
    """
    Sprawdzamy czy licznik 'X items left' poprawnie się aktualizuje
    po dodaniu i ukończeniu zadań.
    """
    page.goto("https://demo.playwright.dev/todomvc")

    # Dodajemy 3 zadania — licznik powinien pokazać 3
    for tekst in ["Zadanie A", "Zadanie B", "Zadanie C"]:
        page.locator(".new-todo").fill(tekst)
        page.locator(".new-todo").press("Enter")

    expect(page.locator(".todo-count")).to_contain_text("3")

    # Oznaczamy jedno jako done — licznik powinien pokazać 2
    page.locator(".todo-list li").first.locator(".toggle").click()
    expect(page.locator(".todo-count")).to_contain_text("2")


# ─────────────────────────────────────────────
# ŚCIEŻKA 11: Nie można dodać pustego zadania
# ─────────────────────────────────────────────
def test_nie_dodaj_pustego_zadania(page: Page):
    """
    Użytkownik próbuje dodać zadanie z pustą nazwą.
    Aplikacja nie powinna dodać niczego do listy.
    """
    page.goto("https://demo.playwright.dev/todomvc")

    # Wciskamy Enter bez wpisywania tekstu
    page.locator(".new-todo").press("Enter")

    # Lista powinna być pusta — puste zadanie nie może zostać dodane
    expect(page.locator(".todo-list li")).to_have_count(0)


# ─────────────────────────────────────────────
# ŚCIEŻKA 12: Filtr "All" pokazuje wszystkie zadania
# ─────────────────────────────────────────────
def test_filtr_all_pokazuje_wszystkie(page: Page):
    """
    Po przełączeniu na filtr 'Completed' a potem 'All',
    wszystkie zadania (ukończone i aktywne) są widoczne.
    """
    page.goto("https://demo.playwright.dev/todomvc")

    page.locator(".new-todo").fill("Aktywne")
    page.locator(".new-todo").press("Enter")
    page.locator(".new-todo").fill("Ukonczone")
    page.locator(".new-todo").press("Enter")

    # Oznaczamy drugie jako done
    page.locator(".todo-list li").nth(1).locator(".toggle").click()

    # Przechodzimy na filtr Completed
    page.locator("a", has_text="Completed").click()

    # Wracamy na filtr All
    page.locator("a", has_text="All").click()

    # Powinny być widoczne oba zadania
    expect(page.locator(".todo-list li")).to_have_count(2)
