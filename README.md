# ProgrammingLanguage


```python
PROGRAM         = { BLOCK };
BLOCK           = { STATEMENT };
STATEMENT       = (λ | ASSIGNMENT | PRINT | WHILE | IF), "\n";
ASSIGNMENT      = IDENTIFIER, "=", BOOLEXPRESSION;
PRINT           = "print", "(", BOOLEXPRESSION, ")";
IF              = "while", BOOLEXPRESSION, "do", "\n", {STATEMENT}, "end", "\n";
IF              = "if", BOOLEXPRESSION, "then", "\n", {STATEMENT}, {"else", "\n", STATEMENT}, "end", "\n";
BOOLEXPRESSION  = BOOLTERM, {"or" BOOLTERM};
BOOLTERM        = RELEXPRESSION, {"and", RELEXPRESSION};
RELEXPRESSION   = EXPRESSION, {("==" | ">" | "<"), EXPRESSION};
EXPRESSION      = TERM, { ("+" | "-"), TERM};
TERM            = FACTOR, {("*" | "/"), FACTOR};
FACTOR          = INT | STRING | IDENTIFIER | (("+" | "-" | "!"), FACTOR) | "(", BOOLEXPRESSION, ")" | READ;
READ            = "read", "(", ")";
IDENTIFIER      = LETTER, {LETTER | DIGIT | "_"};
INT             = DIGIT, {DIGIT};
STRING          = ( " | ' ), { λ | LETTER | DIGIT }, ( " | ' );
LETTER          = ( a | ... | z | A | ... | Z );
DIGIT           = ( 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 0 );
```
