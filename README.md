# Automatyzacja testów UI — Playwright / Python

![CI](https://github.com/Drejkson/playwright-tests/actions/workflows/tests.yml/badge.svg)

Projekt testów end-to-end dla aplikacji [TodoMVC](https://demo.playwright.dev/todomvc). Pokrywa 12 krytycznych ścieżek użytkownika.

📊 **[Raport z ostatniego uruchomienia](https://drejkson.github.io/playwright-tests/report.html)**

## Pokryte ścieżki

| Test | Ścieżka |
|------|---------|
| `test_dodaj_nowe_zadanie` | Dodanie zadania → weryfikacja na liście |
| `test_oznacz_jako_wykonane` | Oznaczenie zadania jako done → weryfikacja licznika |
| `test_usun_zadanie` | Usunięcie zadania → weryfikacja pustej listy |
| `test_dodaj_wiele_zadan` | Dodanie 3 zadań → weryfikacja licznika |
| `test_filtruj_aktywne` | Filtr Active → widoczne tylko nieukończone |
| `test_filtruj_ukonczone` | Filtr Completed → widoczne tylko ukończone |
| `test_wyczysc_ukonczone` | Clear completed → lista pusta |
| `test_oznacz_wszystkie_jako_ukonczone` | Toggle All → wszystkie oznaczone, licznik = 0 |
| `test_edytuj_zadanie` | Edycja nazwy zadania przez double-click |
| `test_licznik_zadan` | Licznik aktywnych zadań aktualizuje się po zmianie statusu |
| `test_nie_dodaj_pustego_zadania` | Enter bez tekstu → brak nowego elementu |
| `test_filtr_all_pokazuje_wszystkie` | Powrót do filtru All → widoczne wszystkie zadania |

Łączny czas regresji manualnej: ~15 min → po automatyzacji: **12 sec** (czas CI).

## Jak uruchomić lokalnie

```bash
pip install -r requirements.txt
playwright install chromium
pytest test_todo.py -v
```

## CI/CD

Testy uruchamiają się automatycznie przy każdym `push` do brancha `main` przez GitHub Actions.

Po każdym uruchomieniu generowany jest raport HTML dostępny pod adresem:
**https://drejkson.github.io/playwright-tests/report.html**
