import re

from zmei_generator.config.domain.collection_set_def import CollectionSetDef
from zmei_generator.config.extras import PageExtra
from zmei_generator.parser.errors import ReactAndChannelsRequiredValidationError
from zmei_generator.parser.gen.ZmeiLangParser import ZmeiLangParser
from zmei_generator.parser.utils import BaseListener


class StreamModel(object):

    def __init__(self, page) -> None:
        self.page = page
        self.target = None
        self.filter_expr = None
        self.fields = None

    @property
    def class_name(self):
        return self.target

    @property
    def stream_name(self):
        return re.sub('[^a-z0-9]+', '_', self.target.lower())


class StreamPageExtra(PageExtra):
    # stream

    def __init__(self, page) -> None:
        super().__init__(page)

        self.models = []


class StreamPageExtraParserListener(BaseListener):


    def __init__(self, collection_set: CollectionSetDef) -> None:
        super().__init__(collection_set)

        self.stream_model = None

    def enterAn_stream(self, ctx: ZmeiLangParser.An_streamContext):
        stream = StreamPageExtra(self.page)
        self.collection_set.extras.append(
            stream
        )

        if not self.page.collection_set.channels or \
                not self.page.react:
            raise ReactAndChannelsRequiredValidationError(token=ctx.start)

        self.page.stream = stream

    def enterAn_stream_target_model(self, ctx: ZmeiLangParser.An_stream_target_modelContext):
        super().enterAn_stream_target_model(ctx)

        model = StreamModel(self.page)
        model.target = ctx.getText()

        self.page.stream.models.append(
            model
        )

        self.stream_model = model

    def enterAn_stream_target_filter(self, ctx: ZmeiLangParser.An_stream_target_filterContext):
        self.stream_model.filter_expr = self._get_code(ctx)

    def enterAn_stream_field_name(self, ctx: ZmeiLangParser.An_stream_field_nameContext):
        field_name = ctx.getText()

        if not self.stream_model.fields:
            self.stream_model.fields = [field_name]
        else:
            self.stream_model.fields.append(field_name)




