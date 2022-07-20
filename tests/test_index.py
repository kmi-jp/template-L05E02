import pytest

from data.index import Index


@pytest.fixture
def keys():
    return ["key 1", "key 2", "key 3", "key 4", "key 5"]


def test_index(keys):
    test_labels = keys

    idx = Index(labels=test_labels)
    values = [0, 1, 2, 3, 4]

    assert idx.labels == test_labels
    assert isinstance(idx.labels, list)
    assert values[idx.get_loc("key 2")] == 1
    assert idx.name == ""


def test_empty_labels():
    with pytest.raises(ValueError):
        Index([])


def test_nonempty_name(keys):
    idx = Index(labels=keys, name="index")

    assert idx.name == "index"


def test_invalid_key():
    with pytest.raises(KeyError):
        Index(["key 1"]).get_loc("key 2")


def test_label_duplicity():
    with pytest.raises(ValueError):
        Index(["key 1", "key 1", "key 3", "key 4", "key 5"])


def test_docstrings():
    assert Index.__doc__ is not None
    assert Index.get_loc.__doc__ is not None
