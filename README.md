# Routin

Routin is a programming language designed to help users create habits and build a solid routine.

<p align="center">
  <img src="Images/Routin.png" alt="Routin" width="240"/>
</p>

* #### [About](#About)
* #### [EBNF](#EBNF)
* #### [Code Example](#Code-Example)
* #### [Flex & Bison](#Flex-&-Bison)

#### <a name="About">About</a> 
Routin is a programming language designed to help users create habits and build a solid routine. It helps you easily check for free time in your schedule and match free time hours with friends and family. Some key features are:

* **Interpreted language:** Easy to run and test.
* **Productivity focus:** Native methods to help you have a more productive day.
* **Syntax inspiration:** Inspired by Lua and Python.
* **Time management:** Represents hours of the day as integers (0 to 24) and measures task duration in hours.

#### <a name="EBNF">EBNF</a> 
```python
PROGRAM   = { BLOCK };
BLOCK     = { STATEMENT };
STATEMENT = (ASSIGNMENT | VARIABLE_DECLARATION | DISPLAY | WHILE | IF | ROUTINE | AVAILABILITY), "\n";

ASSIGNMENT           = IDENTIFIER, "=", BOOLEXPRESSION;
VARIABLE_DECLARATION = "local", IDENTIFIER, [ "=", BOOLEXPRESSION ] ;
DISPLAY              = "display", "(", BOOLEXPRESSION, ")";
WHILE                = "while", BOOLEXPRESSION, "do", "\n", {STATEMENT}, "end", "\n";
IF                   = "if", BOOLEXPRESSION, "then", "\n", {STATEMENT}, ["else", "\n", {STATEMENT}], "end", "\n;
ROUTINE              = "routine", IDENTIFIER, ["=", "(", "[", { ")",BOOLEXPRESSION, ",", INT, "("},"]", "|", "[", { ")",INT, "-", INT, "("}, "]", ")"], "\n;
AVAILABILITY         = "availability", "(",IDENTIFIER, ",",INT, ")";

BOOLEXPRESSION = BOOLTERM, {"or", BOOLTERM};
BOOLTERM       = RELEXPRESSION, {"and", RELEXPRESSION};
RELEXPRESSION  = EXPRESSION, {("==" | ">" | "<"), EXPRESSION};
EXPRESSION     = TERM, { ("+" | "-"), TERM};
TERM           = FACTOR, {("*" | "/"), FACTOR};
FACTOR         = INT | STRING | IDENTIFIER | (("+" | "-" | "!"), FACTOR) | "(", BOOLEXPRESSION, ")" | READ;
READ           = "read", "(", ")";
IDENTIFIER     = LETTER, {LETTER | DIGIT | "_"};
INT            = DIGIT, {DIGIT};
STRING         = {LETTER | DIGIT };

```

![EBNF](Images/EBNF2.png)


#### <a name="Code-Example">Code Example</a> 

Some key points worth noting are:
* The hours of the day are represented as integers, ranging from 0 to 24, where 0 corresponds to the beginning of the day and 24 to the end (midnight).
* The time required to complete a task is also measured in hours. For example, specifying 1 would indicate a duration of 1 hour.
Here's an example of how to use it:


```python
local my_routine
routine my_routine = (
  [("read book", 1), ("gym", 2), ("study", 4)],
  [(0,6), (13,16), (21,24)])


local i = 0
while i < 25 {
  if availability(my_routine, i) {
    print(i)
  }
  i = i + 1
}

print(my_routine)

my_routine.add_task("meeting", 2)
my_routine.del_task("study")

local j = 0
while j < 25 {
  if availability(my_routine, j) {
    print(j)
  }
  j = j + 1
}

print(my_routine)


-------------------------------------------
16
17
18
19
20
Free time: [16, 17, 18, 19, 20]
Tasks time: [('study', 6, 10), ('gym', 10, 12), ('read book', 12, 13)]


6
7
8
9
18
19
20
Free time: [6, 7, 8, 9, 18, 19, 20]
Tasks time: [('gym', 10, 12), ('read book', 12, 13), ('meeting', 16, 18)]
```

#### <a name="Flex-&-Bison">Flex & Bison</a> 

To test the Flex & Bison you can do:
```sh
flex scanner.l
bison -d parser.y
```

```sh
gcc lex.yy.c parser.tab.c -o parser -lfl
```

```sh
./parser < test_input.txt
```
