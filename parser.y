%{
#include <stdio.h>
#include "parser.tab.h"
%}

%token ASSIGNMENT LPAREN RPAREN LBRACKET RBRACKET PIPE COMMA ROUTINE AVAILABILITY
%token WHILE DO IF THEN ELSE END DISPLAY READ OR AND EQ GT LT PLUS MINUS TIMES DIV NOT
%token IDENTIFIER INT_LITERAL STRING_LITERAL NEWLINE

%%

program : blocks
        | /* empty */
        ;

blocks : blocks block
       | block
       ;

block : statements
      ;

statements : statements statement NEWLINE
           | statement NEWLINE
           ;

statement : ASSIGNMENT
          | DISPLAY LPAREN expression RPAREN
          | WHILE expression DO NEWLINE statements END
          | IF expression THEN NEWLINE statements else_block END
          | ROUTINE ASSIGNMENT LPAREN routine_params RBRACKET PIPE LBRACKET routine_params RBRACKET RPAREN
          | AVAILABILITY LPAREN IDENTIFIER COMMA INT_LITERAL RPAREN
          ;

else_block : ELSE NEWLINE statements
           | /* empty */
           ;

routine_params : routine_param COMMA routine_params
               | routine_param
               | /* empty */
               ;

routine_param : RPAREN expression COMMA INT_LITERAL LPAREN
              ;

expression : bool_expression
           ;

bool_expression : bool_term
                | bool_term OR bool_expression
                ;

bool_term : rel_expression
          | rel_expression AND bool_term
          ;

rel_expression : expression EQ expression
               | expression GT expression
               | expression LT expression
               ;

expression : term
           | term PLUS expression
           | term MINUS expression
           ;

term : factor
     | factor TIMES term
     | factor DIV term
     ;

factor : INT_LITERAL
       | STRING_LITERAL
       | IDENTIFIER
       | PLUS factor
       | MINUS factor
       | NOT factor
       | LPAREN bool_expression RPAREN
       | READ LPAREN RPAREN
       ;

%%

int main() {
    yyparse();
    return 0;
}

int yyerror(char *msg) {
    fprintf(stderr, "Error: %s\n", msg);
    return 0;
}
