import re

from cratis_generator.config.domain.collection_set_def import FieldDeclaration
from cratis_generator.config.domain.field_def import FieldDef
from cratis_generator.config.grammar import choices
from cratis_generator.generator.utils import gen_args, handle_parse_exception
from cPyparsing import *


class IntegerFieldDef(FieldDef):

    choices = None

    def parse_options(self):

        field_opts = Optional(Suppress('choices') + Suppress(':') + choices) + stringEnd

        if isinstance(self.options, str) and self.options.strip() != '':
            try:
                opts = field_opts.parseString(self.options)

                if opts.choices:
                    choice_list = []
                    for x in opts.choices:
                        value = int(x.value)
                        label = x.label or x.value
                        choice_list.append((value, label))
                    self.choices = tuple(choice_list)

            except ParseException as e:
                handle_parse_exception(e, self.options,
                                       'Can not parse options for field "{}" for collection "{}"'.format(self.name, self.collection.ref))

    def get_model_field(self, collection):
        args = self.prepare_field_arguemnts()

        if self.choices:
            args['choices'] = self.choices

        return FieldDeclaration(
            [('django.db', 'models')],
            'models.IntegerField({})'.format(gen_args(args))
        )


class FloatFieldDef(FieldDef):
    def get_model_field(self, collection):
        args = self.prepare_field_arguemnts()

        return FieldDeclaration(
            [('django.db', 'models')],
            'models.FloatField({})'.format(gen_args(args))
        )


class DecimalFieldDef(FieldDef):

    positive = False

    def parse_options(self):
        if isinstance(self.options, str) and self.options.strip() != '':
            self.positive = self.options.strip() == '+'

    def get_model_field(self, collection):
        imports = [('django.db', 'models')]

        own_args = {'max_digits': 15, 'decimal_places': 2, }

        if self.positive:
            imports.append(
                ('django.core.validators', 'MinValueValidator')
            )
            imports.append(
                ('decimal', 'Decimal')
            )
            own_args['validators'] = '[MinValueValidator(Decimal("0.00"))]'

        args = self.prepare_field_arguemnts(own_args)

        return FieldDeclaration(
            imports,
            'models.DecimalField({})'.format(gen_args(args, raw_args=['validators']))
        )
