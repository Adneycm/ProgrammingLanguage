/* A Bison parser, made by GNU Bison 3.8.2.  */

/* Bison interface for Yacc-like parsers in C

   Copyright (C) 1984, 1989-1990, 2000-2015, 2018-2021 Free Software Foundation,
   Inc.

   This program is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program.  If not, see <https://www.gnu.org/licenses/>.  */

/* As a special exception, you may create a larger work that contains
   part or all of the Bison parser skeleton and distribute that work
   under terms of your choice, so long as that work isn't itself a
   parser generator using the skeleton or a modified version thereof
   as a parser skeleton.  Alternatively, if you modify or redistribute
   the parser skeleton itself, you may (at your option) remove this
   special exception, which will cause the skeleton and the resulting
   Bison output files to be licensed under the GNU General Public
   License without this special exception.

   This special exception was added by the Free Software Foundation in
   version 2.2 of Bison.  */

/* DO NOT RELY ON FEATURES THAT ARE NOT DOCUMENTED in the manual,
   especially those whose name start with YY_ or yy_.  They are
   private implementation details that can be changed or removed.  */

#ifndef YY_YY_PARSER_TAB_H_INCLUDED
# define YY_YY_PARSER_TAB_H_INCLUDED
/* Debug traces.  */
#ifndef YYDEBUG
# define YYDEBUG 0
#endif
#if YYDEBUG
extern int yydebug;
#endif

/* Token kinds.  */
#ifndef YYTOKENTYPE
# define YYTOKENTYPE
  enum yytokentype
  {
    YYEMPTY = -2,
    YYEOF = 0,                     /* "end of file"  */
    YYerror = 256,                 /* error  */
    YYUNDEF = 257,                 /* "invalid token"  */
    ASSIGNMENT = 258,              /* ASSIGNMENT  */
    LPAREN = 259,                  /* LPAREN  */
    RPAREN = 260,                  /* RPAREN  */
    LBRACKET = 261,                /* LBRACKET  */
    RBRACKET = 262,                /* RBRACKET  */
    PIPE = 263,                    /* PIPE  */
    COMMA = 264,                   /* COMMA  */
    ROUTINE = 265,                 /* ROUTINE  */
    AVAILABILITY = 266,            /* AVAILABILITY  */
    WHILE = 267,                   /* WHILE  */
    DO = 268,                      /* DO  */
    IF = 269,                      /* IF  */
    THEN = 270,                    /* THEN  */
    ELSE = 271,                    /* ELSE  */
    END = 272,                     /* END  */
    DISPLAY = 273,                 /* DISPLAY  */
    READ = 274,                    /* READ  */
    OR = 275,                      /* OR  */
    AND = 276,                     /* AND  */
    EQ = 277,                      /* EQ  */
    GT = 278,                      /* GT  */
    LT = 279,                      /* LT  */
    PLUS = 280,                    /* PLUS  */
    MINUS = 281,                   /* MINUS  */
    TIMES = 282,                   /* TIMES  */
    DIV = 283,                     /* DIV  */
    NOT = 284,                     /* NOT  */
    IDENTIFIER = 285,              /* IDENTIFIER  */
    INT_LITERAL = 286,             /* INT_LITERAL  */
    STRING_LITERAL = 287,          /* STRING_LITERAL  */
    NEWLINE = 288                  /* NEWLINE  */
  };
  typedef enum yytokentype yytoken_kind_t;
#endif

/* Value type.  */
#if ! defined YYSTYPE && ! defined YYSTYPE_IS_DECLARED
typedef int YYSTYPE;
# define YYSTYPE_IS_TRIVIAL 1
# define YYSTYPE_IS_DECLARED 1
#endif


extern YYSTYPE yylval;


int yyparse (void);


#endif /* !YY_YY_PARSER_TAB_H_INCLUDED  */
