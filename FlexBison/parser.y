%{
#include <stdio.h>
int yylex();
void yyerror(const char *s);
%}

%token IF
%token ELSE
%token DOTS
%token WHILE
%token END
%token DISPLAY
%token ROUTINE
%token AVAILABILITY
%token LOCAL
%token READ
%token LPAREN
%token RPAREN
%token LBRACK
%token RBRACK
%token PIPE
%token COMMA
%token EQ
%token GT
%token LT
%token AND
%token OR
%token PLUS
%token MINUS
%token TIMES
%token DIVIDE
%token ASSIGN
%token NOT
%token INT
%token STRING
%token IDENTIFIER
%token NEWLINE

%%

program: statement
        | program statement;

block: NEWLINE statements;

statements: statement
          | statements statement
          ;

statement : assignment
          | display
          | while
          | if
          | routine 
          | availability
          | NEWLINE
          ;

assignment : IDENTIFIER ASSIGN bexpression NEWLINE
           | LOCAL IDENTIFIER ASSIGN bexpression NEWLINE
           | LOCAL IDENTIFIER NEWLINE
           ;

display : DISPLAY LPAREN bexpression RPAREN NEWLINE;

while : WHILE bexpression DOTS block END NEWLINE;


if : IF bexpression DOTS block END NEWLINE
   | IF bexpression DOTS block ELSE DOTS block END NEWLINE
   ;

routine : ROUTINE IDENTIFIER NEWLINE
        | ROUTINE IDENTIFIER ASSIGN LPAREN LBRACK routine_param_list RBRACK PIPE LBRACK routine_restriction_param_list RBRACK RPAREN NEWLINE


routine_param_list : routine_param COMMA routine_param_list
                   | routine_param
                   ;

routine_param : LPAREN bexpression COMMA INT RPAREN
              | /* empty */
              ;


routine_restriction_param_list : routine_restriction_param COMMA routine_restriction_param_list
                               | routine_restriction_param
                               ;

routine_restriction_param : LPAREN INT COMMA INT RPAREN
                          | /* empty */
                          ;


availability : AVAILABILITY LPAREN IDENTIFIER COMMA INT RPAREN NEWLINE;

bexpression : bexpression OR bterm
            | bterm
            ;

bterm : bterm AND rexpression
      | rexpression
      ;

rexpression : rexpression EQ expression
            | rexpression GT expression
            | rexpression LT expression
            | expression 
            ;

expression : expression PLUS term
           | expression MINUS term
           | term
           ;

term : term TIMES factor
     | term DIVIDE factor
     | factor
     ;

factor : PLUS factor
       | MINUS factor
       | NOT factor
       | INT 
       | STRING 
       | LPAREN bexpression RPAREN
       | IDENTIFIER 
       | READ LPAREN RPAREN
      ;

%%

void yyerror(const char *s) {
    extern int yylineno;
    extern char *yytext;

    /* mensagem de erro exibe o símbolo que causou erro e o número da linha */
    printf("\nErro (%s): símbolo \"%s\" (linha %d)\n", s, yytext, yylineno);
}

int main() {
    yyparse();
    return 0;
}
