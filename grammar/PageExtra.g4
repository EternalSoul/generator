parser grammar PageExtra;

options { tokenVocab=ZmeiLangSimpleLexer; }

import
    PageExtraReact,
    PageExtraMarkdown,
    PageExtraAuth,
    PageExtraError,
    PageExtraPost,
    PageExtraCrudCreate,
    PageExtraCrudEdit,
    PageExtraCrudDelete,
    PageExtraCrudDetail,
    PageExtraCrudList,
    PageExtraCrud,
    PageExtraMenu,
    PageExtraGet,
    PageExtraStream,
    PageExtraFlutter,
    PageExtraHtml
    ;

page_annotation:
     an_html
    |an_react
    |an_flutter
    |an_stream
    |an_get
    |an_menu
    |an_crud
    |an_crud_detail
    |an_crud_delete
    |an_crud_edit
    |an_crud_create
    |an_crud_list
    |an_post
    |an_error
    |an_auth
    |an_markdown
    |page_priority_marker
    |NL;

page_priority_marker:
    AN_PRIORITY
    ;