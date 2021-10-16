 # L05E01: Data
Vytvořte balíček `data`, který obsahuje moduly `index.py`, `series.py` a `dataframe.py`.

---

## Třída `Index`
Modul `index.py` obsahuje třídu `Index` sloužící k indexaci libovolné sekvence hodnot.

```python
from data.index import Index

idx = Index(["key 1", "key 2", "key 3", "key 4", "key 5"])
values = [0, 1, 2, 3, 4]

assert values[idx.get_loc("key 2")] == 1
```

Třída obsahuje následující vlastnosti:
* `Index.labels` - seznam klíču (labelů) - nesmí obsahovat duplicity (vyvolá vyjimku `ValueError`).
* `Index.name` - volitelná vlastnost obsahující název indexu, výchozí hodnota na `""`.

Třída obsahuje následující metody:
* `Index.get_loc(self, key)` - přeloží klíč `key` z `Index.labels` na odpovídající index. Pokud není klíč přítomen vyvoláme výjimku `KeyError`.

```python
from data.index import Index


idx = Index(["user 1", "user 2", "user 3", "user 4", "user 5"])

assert idx.name == ""
assert idx.labels == ["user 1", "user 2", "user 3", "user 4", "user 5"]

idx = Index(["user 1", "user 2", "user 3", "user 4", "user 5"], name="users")

assert idx.name == "users"
assert idx.labels == ["user 1", "user 2", "user 3", "user 4", "user 5"]
```

```python
idx = Index(["user 1", "user 2", "user 3", "user 4", "user 5"])

assert idx.get_loc("user 2") == 1
```

---

## Třída `Series`
Modul `series.py` obsahuje třídu `Series`, která uchovává serii hodnot indexovaných dle objektu třídy `Index`.

```python
from data.series import Series
from data.index import Index

# index
users = Index(["user 1", "user 2", "user 3", "user 4", "user 5"], name="names")

# series indexovaná dle indexu users
salaries = Series([20000, 300000, 20000, 50000, 10000], index=users)

assert salaries.values == [20000, 300000, 20000, 50000, 10000]
assert salaries.index.labels == ['user 1', 'user 2', 'user 3', 'user 4', 'user 5']
```

Třída obsahuje následující vlastnosti:
* `Series.values` - seznam hodnot uložený v serii, musí obsahovat alespoň jeden prvek jinak vyvolá `ValueError`.
* `Series.index` - index sloužící k indexaci `Series.values`, musi být stejné délky jako `Series.values` jinak vyvolá `ValueError`. Pokud byla počáteční hodnota `None` vytvoříme index nový, `Index.labels` nastavíme na hodnoty `0` až `n` kde `n` je délka `Series.values`.

Třída obsahuje následující metody:
* `Series.get(self, key)` - pokud `Series.index` obsahuje `key`, vrátí odpovídající hodnotu z `Series.values`, jinak vrací `None`.
* `Series.sum(self)` - sečtě všechny hodnoty v serii, detailní popis níže
* `Series.max(self)` - nalezne maximální hodnotu ze serie, detailní popis níže
* `Series.mean(self)` - vypočítá aritmetický průměr, detailní popis níže
* `Series.apply(self, func)` - aplikuje libovolnou funkci na prvky serie, detailní popis níže
* `Series.abs(self)` - vytvoří novou serii, kde všechny hodnotu budou výsledky aplikace funkce `abs()`, detailní popis níže


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
Maximální hodnota v `Series`. Nemusíte ošetřovat datový typ hodnot v serii.

```python
from data.series import Series
from data.index import Index


users = Index(["user 1", "user 2", "user 3", "user 4", "user 5"], name="names")
cash_flow = Series([-100, 10000, -2000, 1100, 100], index=users)

assert cash_flow.max() == 10000
```

### Metoda `.sum(self)`
Součet hodnot v `Series`. Nemusíte ošetřovat datový typ hodnot v serii.

```python
from data.series import Series
from data.index import Index


users = Index(["user 1", "user 2", "user 3", "user 4", "user 5"], name="names")
cash_flow = Series([-100, 10000, -2000, 1100, 100], index=users)

assert cash_flow.sum() == 9100
```

### Metoda `.mean(self)`
Aritmetický průměr hodnot v `Series`. Nemusíte ošetřovat datový typ hodnot v serii.

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
Která aplikuje funkci `abs` na všechny prvky `Series` a vrátí `Series` novou. Původní `Series` nemodifikuje! Nemusíte ošetřovat datový typ hodnot v serii.

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


