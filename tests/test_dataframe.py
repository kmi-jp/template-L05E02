import pytest

from data.index import Index
from data.series import Series
from data.dataframe import DataFrame


@pytest.fixture
def users_data():
    return ["user 1", "user 2", "user 3", "user 4"]


@pytest.fixture
def salaries_data():
    return [20000, 300000, 20000, 50000]


@pytest.fixture
def cash_flow_data():
    return [-100, 10000, -2000, 1100]


@pytest.fixture
def names_data():
    return ["Lukas Novak", "Petr Pavel", "Pavel Petr", "Ludek Skocil"]


def test_dataframe(users_data, salaries_data, names_data, cash_flow_data):
    users = Index(users_data, name="names")

    salaries = Series(salaries_data, index=users)
    names = Series(names_data, index=users)
    cash_flow = Series(cash_flow_data, index=users)

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


def test_empty_columns(users_data, salaries_data, names_data, cash_flow_data):
    users = Index(users_data, name="names")

    salaries = Series(salaries_data, index=users)
    names = Series(names_data, index=users)
    cash_flow = Series(cash_flow_data, index=users)

    data = DataFrame([names, salaries, cash_flow])

    assert data.columns.labels == Index(range(3)).labels
    assert data.values == [names, salaries, cash_flow]
    assert data.get(1) == salaries
    assert data.get(2).max() == 10000


def test_docstrings():
    assert DataFrame.__doc__ is not None
    assert DataFrame.get.__doc__ is not None
