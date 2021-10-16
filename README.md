 # L05E01: Data
Vytvořte balíček `data`, který obsahuje moduly `index.py`, `series.py` a `dataframe.py`.

---

## Třída `Index`
Modul `index.py` obsahuje třídu `Index`, která slouží k překladu názvu na jejich index. Třída `Index` obsahuje vlastnosti `.labels` (reprezentujeme seznamem) a `.name`. Vlastnost `.labels` je povinná a její interní reprezentace je seznam. Seznam `.labels` nesmí obsahovat duplicitní řetězec, pokud se tak stane, vyvoláme `ValueError`. Vlastnost `.name` je volitelná, v případě, že ji uživatel neuvede je rovna `""`.

```python
from data.index import Index


idx = Index(["user 1", "user 2", "user 3", "user 4", "user 5"])

assert idx.name == ""
assert idx.labels == ["user 1", "user 2", "user 3", "user 4", "user 5"]

idx = Index(["user 1", "user 2", "user 3", "user 4", "user 5"], name="users")

assert idx.name == "users"
assert idx.labels == ["user 1", "user 2", "user 3", "user 4", "user 5"]
```

Dále třída `Index` obsahuje metodu `.get_loc(self, key)`, která vrací index zadaného klíče `key` uloženého v seznamu `.labels`. Pokud není klíč přítomen vyvoláme výjimku `ValueError`.

```python
idx = Index(["user 1", "user 2", "user 3", "user 4", "user 5"])

assert idx.get_loc("user 1") == 1
```

---

## Třída `Series`
Modul `series.py` obsahuje třídu `Series`, která slouží k reprezentaci serie hodnot (má alespoň jednu hodnotu) s odpovídajícím indexem. Například tedy platy uživatelů. Třída `Series` obsahuje povinnou vlastnost `.values` ve které uložíme jednotlivé hodnoty a vlastnost `.index` reprezentovaný objektem třídy `Index` sloužící k indexování hodnot uložených ve `.values`. Pokud `.index` není uveden, vytvoří se index s hodnotami 0 až n, kde n je délka `.values`.

```python
from data.series import Series
from data.index import Index


users = Index(["user 1", "user 2", "user 3", "user 4", "user 5"], name="names")

names = Series(["Lukas Novak", "Petr Pavel", "Pavel Petr", "Ludek Skocil", "Josef Nebyl"], index=users)
cash_flow = Series([-100, 10000, -2000, 1100, 100], index=users)
salaries = Series([20000, 300000, 20000, 50000, 10000], index=users)

assert salaries.values == [20000, 300000, 20000, 50000, 10000]
assert salaries.index.labels == ['user 1', 'user 2', 'user 3', 'user 4', 'user 5']

# situace kdy nebude předán index
no_index = Series(["Lukas Novak", "Petr Pavel", "Pavel Petr", "Ludek Skocil", "Josef Nebyl"])
assert no_index.index.labels == [0, 1, 2, 3, 4]
```

### Metoda `.get(self, key)`
Slouží k přístupu k hodnota uložené pod klíčem `key`. V případě, že klíč není přítomen, výsledná hodnota je `None`.

```python
from data.series import Series
from data.index import Index


users = Index(["user 1", "user 2", "user 3", "user 4", "user 5"], name="names")

cash_flow = Series([-100, 10000, -2000, 1100, 100], index=users)

assert cash_flow.get("user 1") == -100
assert cash_flow.get("user 1000") is None
```

Dále bude možné provádět jednoduché operace na datech uložených v `Series`. Konkrétně:

### Metoda `.max(self)`
Maximální hodnota v `Series`.

```python
from data.series import Series
from data.index import Index


users = Index(["user 1", "user 2", "user 3", "user 4", "user 5"], name="names")
cash_flow = Series([-100, 10000, -2000, 1100, 100], index=users)

assert cash_flow.max() == 10000
```

### Metoda `.sum(self)`
Součet hodnot v `Series`.

```python
from data.series import Series
from data.index import Index


users = Index(["user 1", "user 2", "user 3", "user 4", "user 5"], name="names")
cash_flow = Series([-100, 10000, -2000, 1100, 100], index=users)

assert cash_flow.sum() == 9100
```

### Metoda `.mean(self)`
Aritmetický průměr hodnot v `Series`.

```python
from data.series import Series
from data.index import Index


users = Index(["user 1", "user 2", "user 3", "user 4", "user 5"], name="names")
cash_flow = Series([-100, 10000, -2000, 1100, 100], index=users)

assert cash_flow.mean() == 1820.0
```

### Metoda `.apply(self, func)`
Která aplikuje funkci `func` na všechny prvky `Series` a vrátí `Series` novou (s vypočítanými hodnotami). Původní `Series` nemodifikuje!

```python
from data.series import Series
from data.index import Index


def squared(a):
    """Returns squared number"""
    return a ** 2


users = Index(["user 1", "user 2", "user 3", "user 4", "user 5"], name="names")
cash_flow = Series([-100, 10000, -2000, 1100, 100], index=users)

result = cash_flow.apply(squared)

assert cash_flow != result
assert result.values == [10000, 100000000, 4000000, 1210000, 10000]
```

### Metoda `.abs(self)`
Která aplikuje funkci `abs` na všechny prvky `Series` a vrátí `Series` novou. Původní `Series` nemodifikuje!

```python
from data.series import Series
from data.index import Index


users = Index(["user 1", "user 2", "user 3", "user 4", "user 5"], name="names")
cash_flow = Series([-100, 10000, -2000, 1100, 100], index=users)

result = cash_flow.abs(squared)

assert cash_flow != result
assert result.values == [100, 10000, 2000, 1100, 100
```

---

## Třída `DataFrame`
Modul `dataframe.py` obsahuje třídu `DataFrame`, která slouží k reprezentaci tabulky dat. Tabulka je složena ze sloupců (má alespoň jeden sloupec), každý sloupec je tvořen instancí třídy `Series`. Sloupce jsou indexované pomocí instance `Index`. Třída `DataFrame` tedy obsahuje dvě vlastnosti `.values` (seznam `Series` instancí) a `.columns` (instance třídy `Index`).

Třída `DataFrame` obsahuje jednu metodu `.get(self, key)`, které vrací sloupec odpovídající klíči `key`. Pokud klíč `key` není obsažen v indexu `.columns` vrací `None`.

```python
from data.series import Series
from data.index import Index


users = Index(["user 1", "user 2", "user 3", "user 4", "user 5"], name="names")

salaries = Series([20000, 300000, 20000, 50000, 10000], index=users)
names = Series(["Lukas Novak", "Petr Pavel", "Pavel Petr", "Ludek Skocil", "Josef Nebyl"], index=users)
cash_flow = Series([-100, 10000, -2000, 1100, 100], index=users)

data = DataFrame([names, salaries, cash_flow], columns=Index(["names", "salary", "cash flow"]))

data.get("salary") == salaries
data.get("cash flow").max() == 10000
```


