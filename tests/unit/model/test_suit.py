from textwrap import dedent

import pytest

from zmei_generator.extras.collection_set.suit import SuitCsExtra
from zmei_generator.extras.model.admin import AdminExtra, AdminInlineConfig
from zmei_generator.parser.errors import TabsSuitRequiredValidationError
from zmei_generator.parser.parser import parse_string
from zmei_generator.parser.populate import populate_collection_set


def _(code):
    tree = parse_string(dedent(code))

    return populate_collection_set(tree, 'example')


def test_suit():
    cs = _("""
        @suit
    """)

    assert 'django-suit' in cs.get_required_deps()
    assert 'suit' in cs.get_required_apps()
    assert isinstance(cs.suit, SuitCsExtra)


def test_app_name():
    cs = _("""
        @suit("hoho!")
    """)

    assert cs.suit.app_name == 'hoho!'


def test_admin_tabs_no_suit():

    with pytest.raises(TabsSuitRequiredValidationError):
        _("""
            #boo
            -----
            a
    
            @admin(tabs: lala(a))
        """)