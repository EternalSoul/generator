from textwrap import dedent

from zmei_generator.fields.text import SlugFieldDef
from zmei_generator.parser.parser import parse_string
from zmei_generator.parser.populate import populate_collection_set


def _(code):
    tree = parse_string(dedent(code))

    return populate_collection_set(tree, 'example')


def test_slug_field():
    cs = _("""
    
        #boo
        ----------
        a: text(15)
        b: text(10)
        c: slug(a,b)
    """)

    c = cs.collections['boo'].fields['c']

    assert isinstance(c, SlugFieldDef)
    assert c.field_names == ['a', 'b']
