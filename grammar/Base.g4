parser grammar Base;

options { tokenVocab=ZmeiLangSimpleLexer; }

/**
 * Allow keywords to be used as ID
 */
id_or_kw: ID
   |BOOL
   |WRITE_MODE
   |KW_THEME
   |KW_INSTALL
   |KW_HEADER
   |KW_SERVICES
   |KW_SELENIUM_PYTEST
   |KW_CHILD
   |KW_FILTER_OUT
   |KW_FILTER_IN
   |KW_PAGE
   |KW_LINK_SUFFIX
   |KW_URL_PREFIX
   |KW_CAN_EDIT
   |KW_OBJECT_EXPR
   |KW_BLOCK
   |KW_ITEM_NAME
   |KW_PK_PARAM
   |KW_LIST_FIELDS
   |KW_DELETE
   |KW_EDIT
   |KW_CREATE
   |KW_DETAIL
   |KW_SKIP
   |KW_FROM
   |KW_POLY_LIST
   |KW_CSS
   |KW_JS
   |KW_INLINE_TYPE
   |KW_AUTH_TYPE
   |KW_INLINE
   |KW_TYPE
   |KW_USER_FIELD
   |KW_ANNOTATE
   |KW_ON_CREATE
   |KW_QUERY
   |KW_AUTH
   |KW_COUNT
   |KW_I18N
   |KW_EXTRA
   |KW_TABS
   |KW_LIST
   |KW_READ_ONLY
   |KW_LIST_EDITABLE
   |KW_LIST_FILTER
   |KW_LIST_SEARCH
   |KW_FIELDS
   |KW_IMPORT
   |KW_AS
   |COL_FIELD_TYPE_LONGTEXT
   |COL_FIELD_TYPE_HTML
   |COL_FIELD_TYPE_HTML_MEDIA
   |COL_FIELD_TYPE_FLOAT
   |COL_FIELD_TYPE_DECIMAL
   |COL_FIELD_TYPE_DATE
   |COL_FIELD_TYPE_DATETIME
   |COL_FIELD_TYPE_CREATE_TIME
   |COL_FIELD_TYPE_UPDATE_TIME
   |COL_FIELD_TYPE_IMAGE
   |COL_FIELD_TYPE_FILE
   |COL_FIELD_TYPE_FILER_IMAGE
   |COL_FIELD_TYPE_FILER_FILE
   |COL_FIELD_TYPE_FILER_FOLDER
   |COL_FIELD_TYPE_FILER_IMAGE_FOLDER
   |COL_FIELD_TYPE_TEXT
   |COL_FIELD_TYPE_INT
   |COL_FIELD_TYPE_SLUG
   |COL_FIELD_TYPE_BOOL
   |COL_FIELD_TYPE_ONE
   |COL_FIELD_TYPE_ONE2ONE
   |COL_FIELD_TYPE_MANY
   |COL_FIELD_CHOICES
   ;

classname: id_or_kw (DOT id_or_kw)*;
model_ref: HASH (id_or_kw DOT)? id_or_kw;

field_list_expr:
    DOT? STAR (COMA EXCLUDE field_list_expr_field)*
    | id_or_kw (COMA EXCLUDE? field_list_expr_field)*
    ;

field_list_expr_field : STAR? id_or_kw STAR? ;


write_mode_expr : SQ_BRACE_OPEN WRITE_MODE SQ_BRACE_CLOSE;

python_code:
     code_block
    |code_line
    ;

code_line:
    ASSIGN
    PYTHON_CODE
    NL;

code_block:
    CODE_BLOCK
    ;
