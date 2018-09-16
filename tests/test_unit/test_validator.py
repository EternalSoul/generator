
from textwrap import dedent

import pytest

from zmei_generator.parser.errors import PageParentValidationError
from zmei_generator.parser.parser import parse_string
from zmei_generator.parser.symbols import SymbolTable
from zmei_generator.parser.validator import validate


def _(code):
    tree = parse_string(dedent(code))

    symbols = SymbolTable()
    symbols.update_from_tree(tree)

    return validate(tree, symbols)


def test_validate_page_base_name_ok():
    errors = _("""

        [base]
        [base->index]

    """)

    assert errors == []


def test_validate_page_base_name_fail():
    errors = _("""

        [base]
        [foo->index]

    """)

    assert len(errors) == 1
    assert isinstance(errors[0], PageParentValidationError)
    assert errors[0].parent_page_name == 'foo'
