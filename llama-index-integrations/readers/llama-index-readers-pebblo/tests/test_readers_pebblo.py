from llama_index.core.readers.base import BaseReader
from llama_index.readers.pebblo import PebbloSafeReader
from pathlib import Path
from typing import Dict
from pytest_mock import MockerFixture
from llama_index.readers.file import CSVReader
from llama_index.core import Document


class MockResponse:
    def __init__(self, json_data: Dict, status_code: int):
        self.json_data = json_data
        self.status_code = status_code

    def json(self) -> Dict:
        return self.json_data


def test_class():
    names_of_base_classes = [b.__name__ for b in PebbloSafeReader.__mro__]
    assert BaseReader.__name__ in names_of_base_classes


def test_empty_filebased_loader(mocker: MockerFixture) -> None:
    """Test basic file based csv loader."""
    mocker.patch.multiple(
        "requests",
        get=MockResponse(json_data={"data": ""}, status_code=200),
        post=MockResponse(json_data={"data": ""}, status_code=200),
    )

    file_path = f"{Path().resolve()}/test_empty.csv"
    expected_docs: list = []

    # Exercise
    loader = PebbloSafeReader(
        CSVReader(),
        "dummy_app_name",
        "dummy_owner",
        "dummy_description",
    )
    result = loader.load_data(file=Path(file_path))

    # Assert
    assert result[0].text == ""
    assert result[0].metadata == {"filename": "test_empty.csv", "extension": ".csv"}


def test_csv_loader_load_valid_data(mocker: MockerFixture) -> None:
    mocker.patch.multiple(
        "requests",
        get=MockResponse(json_data={"data": ""}, status_code=200),
        post=MockResponse(json_data={"data": ""}, status_code=200),
    )
    file_path = f"{Path().resolve()}/test_nominal.csv"
    expected_docs = [
        Document(
            page_content="column1: value1\ncolumn2: value2\ncolumn3: value3",
            metadata={"source": "test_nominal.csv", "row": 0},
        ),
        Document(
            page_content="column1: value4\ncolumn2: value5\ncolumn3: value6",
            metadata={"source": "test_nominal.csv", "row": 1},
        ),
    ]

    # Exercise
    loader = PebbloSafeReader(
        CSVReader(),
        "dummy_app_name",
        "dummy_owner",
        "dummy_description",
    )
    result = loader.load_data(file=Path(file_path))

    # Assert
    assert (
        result[0].text
        == "column1, column2, column3\nvalue1, value2, value3\nvalue4, value5, value6"
    )
    assert result[0].metadata == {"filename": "test_nominal.csv", "extension": ".csv"}
