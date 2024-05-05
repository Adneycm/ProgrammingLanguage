%{
#include <stdio.h>
#include "parser.tab.h"
%}

%option noyywrap

/* Regular expressions for tokens */
DIGIT           [0-9]
LETTER          [a-zA-Z]
ID              {LETTER}({LETTER}|{DIGIT}|"_")*
INT             {DIGIT}+
STRING          {LETTER}|{DIGIT}+

%%
"="             { return ASSIGNMENT; }
"("             { return LPAREN; }
")"             { return RPAREN; }
"["             { return LBRACKET; }
"]"             { return RBRACKET; }
"|"             { return PIPE; }
","             { return COMMA; }
"routine"       { return ROUTINE; }
"availability"  { return AVAILABILITY; }
"while"         { return WHILE; }
"do"            { return DO; }
"if"            { return IF; }
"then"          { return THEN; }
"else"          { return ELSE; }
"end"           { return END; }
"display"       { return DISPLAY; }
"read"          { return READ; }
"or"            { return OR; }
"and"           { return AND; }
"=="            { return EQ; }
">"             { return GT; }
"<"             { return LT; }
"+"             { return PLUS; }
"-"             { return MINUS; }
"*"             { return TIMES; }
"/"             { return DIV; }
"!"             { return NOT; }
\n              { return NEWLINE; }
{INT}           { return INT_LITERAL; }
{STRING}        { return STRING_LITERAL; }
{ID}            { return IDENTIFIER; }
.               { /* Ignore other characters */ }

%%

int main() {
    yylex();
    return 0;
}
