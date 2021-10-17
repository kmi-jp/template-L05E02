import pytest

from data.index import Index
from data.series import Series
from data.dataframe import DataFrame


def test_dataframe():
    users = Index(["user 1", "user 2", "user 3", "user 4"], name="names")

    salaries = Series([20000, 300000, 20000, 50000], index=users)
    names = Series(["Lukas Novak", "Petr Pavel", "Pavel Petr", "Ludek Skocil"], index=users)
    cash_flow = Series([-100, 10000, -2000, 1100], index=users)

    columns = Index(["names", "salary", "cash flow"])
    data = DataFrame([names, salaries, cash_flow], columns=columns)

    assert data.columns == columns
    assert data.values == [names, salaries, cash_flow]
    assert isinstance(data.values, list)
    assert data.get("salary") == salaries
    assert data.get("cash flow").max() == 10000
    assert data.get("wrong key") == None


def test_empty_dataframe():
    with pytest.raises(ValueError):
        DataFrame([])


def test_empty_columns():
    users = Index(["user 1", "user 2", "user 3", "user 4"], name="names")

    salaries = Series([20000, 300000, 20000, 50000], index=users)
    names = Series(["Lukas Novak", "Petr Pavel", "Pavel Petr", "Ludek Skocil"], index=users)
    cash_flow = Series([-100, 10000, -2000, 1100], index=users)

    data = DataFrame([names, salaries, cash_flow])

    assert data.columns.labels == Index(range(3)).labels
    assert data.values == [names, salaries, cash_flow]
    assert data.get(1) == salaries
    assert data.get(2).max() == 10000
