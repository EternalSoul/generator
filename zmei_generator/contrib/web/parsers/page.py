from zmei_generator.domain.collection_set_def import CollectionSetDef
from zmei_generator.domain.page_def import PageDef, PageFunction
from zmei_generator.domain.page_expression import PageExpression
from zmei_generator.parser.errors import LangsRequiredValidationError
from zmei_generator.parser.gen.ZmeiLangParser import ZmeiLangParser
from zmei_generator.parser.utils import BaseListener


class PageParserListener(BaseListener):
    def __init__(self, collection_set: CollectionSetDef) -> None:
        super().__init__(collection_set)

        self.page = None  # type: PageDef

    ############################################
    # Page
    ############################################

    def enterPage(self, ctx: ZmeiLangParser.PageContext):
        self.page = PageDef(self.collection_set)
        self.page.page_items = {}
        self.page.name = ctx.page_header().page_name().getText()

        base_name = ctx.page_header().page_base()
        if base_name:
            base_name = base_name.getText()
            self.page.extend_name = base_name[-2] == '~'
            self.page.parent_name = base_name[:-2]

        if self.page.parent_name and self.page.extend_name:
            self.page.name = f'{self.page.parent_name}_{self.page.name}'

        self.collection_set.pages[self.page.name] = self.page

    def enterPage_alias_name(self, ctx: ZmeiLangParser.Page_alias_nameContext):
        self.page.defined_url_alias = ctx.getText()

    def enterPage_url(self, ctx: ZmeiLangParser.Page_urlContext):
        url = ctx.getText().strip()
        if url[0] == '$':
            if not self.collection_set.langs:
                raise LangsRequiredValidationError(ctx.start)
        self.page.set_uri(url)

    def enterPage_template(self, ctx: ZmeiLangParser.Page_templateContext):
        tpl = ctx.getText().strip()

        if '{' in tpl:
            self.page.parsed_template_expr = tpl.strip('{}')
        else:
            self.page.parsed_template_name = tpl

    def enterPage_field(self, ctx: ZmeiLangParser.Page_fieldContext):
        field = ctx.page_field_name().getText()
        val = ctx.page_field_code().getText()

        expr = PageExpression(field, val, self.page)

        if field == 'sitemap':
            self.page.sitemap_expr = expr
        else:
            self.page.page_items[field] = expr

    def enterPage_function(self, ctx: ZmeiLangParser.Page_functionContext):
        super().enterPage_function(ctx)

        func = PageFunction()
        func.name = ctx.page_function_name().getText()
        if ctx.page_function_args():
            func.out_args = [x.strip() for x in ctx.page_function_args().getText().split(',')]
            func.args = [x for x in func.out_args if x not in ('url', 'request')]
        else:
            func.args = []

        if ctx.code_block():
            func.body = self._get_code(ctx)

        self.page.functions[func.name] = func

    def enterPage_code(self, ctx: ZmeiLangParser.Page_codeContext):
        self.page.page_code = self._get_code(ctx.python_code()) + '\n'

    def exitPage(self, ctx: ZmeiLangParser.PageContext):
        self.page = None
