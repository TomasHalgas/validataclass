"""
validataclass
Copyright (c) 2021, binary butterfly GmbH and contributors
Use of this source code is governed by an MIT-style license that can be found in the LICENSE file.
"""

import pytest
from pytest import raises
from validataclass.exceptions import InvalidDecimalError
from validataclass.validators import DecimalValidator, IntegerValidator, Validator
from validataclass.dataclasses import validataclass
from unittest.mock import MagicMock
from validataclass.helpers import BaseDateTimeRange
import unittest.mock
import sys


class MockedPattern:

    def fullmatch(self):
        return True


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
