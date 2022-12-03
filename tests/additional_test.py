"""
validataclass
Copyright (c) 2021, binary butterfly GmbH and contributors
Use of this source code is governed by an MIT-style license that can be found in the LICENSE file.
"""

import pytest
from pytest import raises
from validataclass.exceptions import InvalidDecimalError
from validataclass.validators import DecimalValidator, IntegerValidator, Validator, BooleanValidator, StringValidator, \
    AnythingValidator, ListValidator, UrlValidator, Noneable, RejectValidator, DataclassValidator
from validataclass.dataclasses import validataclass, ValidataclassMixin
from unittest.mock import MagicMock
from validataclass.helpers import BaseDateTimeRange
import unittest.mock
import sys


class MockedPattern:
    def fullmatch(self):
        return True


@validataclass
class AdditionalTestDataclass(ValidataclassMixin):
    url: str = UrlValidator()
    boolean: bool = (Noneable(RejectValidator(), default=True))


class AdditionalTest:
    """
    Additional unit tests for excluded statements.
    """

    @staticmethod
    @pytest.mark.parametrize('input_data', ['', 'bananana', '1234x', '$123', '1,234', '.'])
    def test_decimal_validator_mock(input_data):
        """ Test DecimalValidator with malformed strings. """

        with unittest.mock.patch.object(DecimalValidator, 'decimal_regex', MockedPattern):
            validator = DecimalValidator()
            with pytest.raises(InvalidDecimalError) as exception_info:
                validator.validate(input_data)
            assert exception_info.value.to_dict() == {'code': 'invalid_decimal'}

    @staticmethod
    def test_validataclass_version():
        """ Create a dataclass using @validataclass with mocked python version 3.10 -> kw_only should be set. """

        with unittest.mock.patch.object(sys, 'version_info', (3, 10)) as v_info:
            print(v_info)

            with pytest.raises(TypeError) as exception_info:
                @validataclass
                class FooDataclass:
                    foo: int = IntegerValidator()

            assert str(exception_info.value) == "dataclass() got an unexpected keyword argument 'kw_only'"

    @staticmethod
    def test_abstract_methods_not_implemented():
        with pytest.raises(NotImplementedError):
            BaseDateTimeRange.to_dict(None, None)
        with pytest.raises(NotImplementedError):
            BaseDateTimeRange.contains_datetime(None, None)
        with pytest.raises(NotImplementedError):
            Validator.validate(None, "test")

    """
    Additional integration tests.
    """

    @staticmethod
    def test_integration_string_boolean():
        # check workflow of StringValidator(min_length=3, max_length=5) + BooleanValidator(allow_strings=True)
        # if it accepts string value "true"
        validator_string = StringValidator(min_length=3, max_length=5)
        string_result = validator_string.validate("true")
        validator_boolean = BooleanValidator(allow_strings=True)
        boolean_result = validator_boolean.validate(string_result)
        assert boolean_result is True

    @staticmethod
    def test_integration_anything_list():
        # check workflow: if combination of AnythingValidator + ListValidator accepts anything
        validator_anything = AnythingValidator(allowed_types=[int, float, str, list, tuple, range, bool, dict, complex],
                                               allow_none=True)
        input_list = [
            42,
            4.2,
            '1.234',
            'banana',
            [8, 4],
            [8, 4.2],
            [8, 'banana'],
            ("apple", "banana", "cherry"),
            range(1, 80, 10),
            True,
            False,
            {
                "a": 4,
                "b": 5
            },
            complex(2, -3),
            None,
        ]

        validator_list = ListValidator(validator_anything)
        list_result = validator_list.validate(input_list)

        assert list_result == input_list

    @staticmethod
    def test_dataclass_url_noneable_reject_validators():
        # check workflow of DataclassValidator with custom scheme (UrlValidator + Noneable wrapper with RejectValidator)
        validator = DataclassValidator(AdditionalTestDataclass)
        obj: AdditionalTestDataclass = validator.validate({'url': "https://moodle.fei.tuke.sk", 'boolean': None})
        assert obj.to_dict() == {
            'url': "https://moodle.fei.tuke.sk",
            'boolean': True
        }
