

grammar another;


file: (row '\n')*;
row: field (',' field)*;
field: INT;

INT: [0-9]+;