# WSB_Python_INLS5-SI_M.Madej

**Wypożyczalnia samochodów** — konsolowa aplikacja w Pythonie z bazą danych SQLite.

Autor: Magdalena Madej

## Opis

Program pozwala prowadzić prostą ewidencję samochodów i ich wypożyczeń. Dane są zapisywane w pliku `mini_loans.db`, więc nie znikają po zamknięciu programu.

## Wymagania i uruchomienie

- Python 3
- Tylko biblioteka standardowa (`sqlite3`, `datetime`) — nie trzeba nic instalować

```
python main.py
```

Przy pierwszym uruchomieniu program sam tworzy plik bazy i tabele. Plik `mini_loans.db` w repozytorium zawiera przykładowe dane.

## Funkcje (menu)

| Opcja | Działanie |
|-------|-----------|
| 1 | Dodanie samochodu do bazy |
| 2 | Lista wszystkich samochodów z informacją o dostępności (TAK / NIE) |
| 3 | Wypożyczenie samochodu — wyświetla tylko dostępne auta, pyta o ID i imię i nazwisko wypożyczającego |
| 4 | Zwrot samochodu — wyświetla tylko wypożyczone auta i pyta o ID |
| 5 | Lista aktualnych wypożyczeń (samochód, osoba, data), od najnowszych |
| 0 | Wyjście z programu |

## Struktura bazy danych

**`items`** — samochody

| Kolumna | Typ | Opis |
|---------|-----|------|
| `id` | INTEGER, PK | ID samochodu |
| `name` | TEXT | Nazwa / model |
| `is_available` | INTEGER | `1` — dostępny, `0` — wypożyczony |

**`loans`** — aktywne wypożyczenia

| Kolumna | Typ | Opis |
|---------|-----|------|
| `id` | INTEGER, PK | ID wypożyczenia |
| `item_id` | INTEGER, FK → `items.id`, UNIQUE | Wypożyczony samochód |
| `borrower` | TEXT | Imię i nazwisko wypożyczającego |
| `loan_date` | TEXT | Data wypożyczenia w formacie `RRRR-MM-DD` |

Relacja: jeden samochód może mieć najwyżej jedno aktywne wypożyczenie (`UNIQUE` na `item_id`). Przy zwrocie rekord z `loans` jest usuwany, a samochód znowu staje się dostępny.

## Najważniejsze rozwiązania

- **Zapytania parametryzowane** (`?`) — dane od użytkownika nigdy nie są wklejane bezpośrednio do SQL, co chroni przed SQL injection.
- **Transakcje** (`with conn:`) — przy wypożyczeniu i zwrocie dwie operacje (zmiana `items` i zmiana `loans`) wykonują się razem albo wcale, więc baza nie zostanie w niespójnym stanie.
- **Klucz obcy** z `ON DELETE CASCADE` i włączonym `PRAGMA foreign_keys = ON` — usunięcie samochodu usuwa też jego wypożyczenie.
- **`sqlite3.Row`** — wyniki zapytań są dostępne po nazwie kolumny, np. `row["name"]`.
- **`INNER JOIN`** w liście wypożyczeń — łączy dane z obu tabel, żeby pokazać nazwę samochodu razem z osobą i datą.
- **Funkcja pomocnicza `get_items()`** — jedno zapytanie o listę samochodów używane w kilku miejscach zamiast powtarzania tego samego kodu.
- **Walidacja danych wejściowych** — puste nazwy, puste dane wypożyczającego, ID niebędące liczbą, nieistniejący samochód i próba wypożyczenia już wypożyczonego auta są obsługiwane komunikatem, bez przerywania programu.

## Struktura kodu (`main.py`)

| Funkcja | Rola |
|---------|------|
| `connect()` | Połączenie z bazą, ustawienie `Row` i kluczy obcych |
| `init_db()` | Utworzenie tabel, jeśli nie istnieją |
| `get_items()` | Pobranie listy samochodów |
| `add_item()` | Opcja 1 |
| `list_items()` | Opcja 2 |
| `loan_item()` | Opcja 3 |
| `return_items()` | Opcja 4 |
| `list_loans()` | Opcja 5 |
| `menu()` | Wyświetlenie menu |
| `main()` | Główna pętla programu |
