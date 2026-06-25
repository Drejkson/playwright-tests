# Automatyzacja testów UI — Playwright / Python

Projekt testów end-to-end dla aplikacji TodoMVC. Pokrywa 3 krytyczne ścieżki użytkownika.

## Pokryte ścieżki

| Test | Ścieżka | Czas bez automatyzacji |
|------|---------|------------------------|
| `test_dodaj_nowe_zadanie` | Dodanie zadania → weryfikacja na liście | ~5 min |
| `test_oznacz_zadanie_jako_wykonane` | Oznaczenie zadania jako done → weryfikacja licznika | ~10 min |
| `test_usun_zadanie` | Usunięcie zadania → weryfikacja pustej listy | ~15 min |

Łączny czas regresji manualnej: ~30 min → po automatyzacji: **~4 min** (czas CI).

## Jak uruchomić lokalnie

```bash
pip install -r requirements.txt
playwright install chromium
pytest tests/ -v
```

## CI/CD

Testy uruchamiają się automatycznie przy każdym `push` do brancha `main` przez GitHub Actions.

#aktualizacja
