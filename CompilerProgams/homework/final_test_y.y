%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void generate_code(const char *instr, const char *arg1, const char *arg2, const char *result);
int temp_count = 0;
char temp_var[10];

char *new_temp() {
    sprintf(temp_var, "t%d", temp_count++);
    return strdup(temp_var);
}
%}

%union {
    double dval;
    char *str;
}

%token <str> NAME
%token <dval> NUMBER
%token PROGRAM BEGINP END DECLARE AS INTEGER FLOAT
%token FOR TO DOWNTO ENDFOR IF THEN ELSE ENDIF PRINT
%token LE GE EQ NE

%type <str> expression var_list
%type <str> statement_list statement

%%
Program:
    PROGRAM NAME BEGINP statement_list END {
        printf("Compilation successful.\n");
    }
    ;

statement_list:
    statement
    | statement_list statement
    ;

statement:
    var_declare
    | for_loop
    | if_statement
    | assign
    | print_statement
    ;

var_declare:
    DECLARE var_list AS type ';' {
        printf("Variables declared.\n");
    }
    ;

type:
    INTEGER | FLOAT
    ;

var_list:
    NAME
    | var_list ',' NAME
    ;

assign:
    NAME '=' expression ';' {
        generate_code("I_STORE", $3, "-", $1);
    }
    ;

expression:
    expression '+' expression {
        char *t = new_temp();
        generate_code("I_ADD", $1, $3, t);
        $$ = t;
    }
    | expression '-' expression {
        char *t = new_temp();
        generate_code("I_SUB", $1, $3, t);
        $$ = t;
    }
    | expression '*' expression {
        char *t = new_temp();
        generate_code("I_MUL", $1, $3, t);
        $$ = t;
    }
    | expression '/' expression {
        char *t = new_temp();
        generate_code("I_DIV", $1, $3, t);
        $$ = t;
    }
    | NAME { $$ = $1; }
    | NUMBER { $$ = $1; }
    ;

print_statement:
    PRINT '(' var_list ')' ';' {
        printf("Print command\n");
    }
    ;

for_loop:
    FOR '(' NAME '=' expression TO expression ')' statement_list ENDFOR {
        printf("FOR loop parsed.\n");
    }
    | FOR '(' NAME '=' expression DOWNTO expression ')' statement_list ENDFOR {
        printf("FOR loop parsed (DOWNTO).\n");
    }
    ;

if_statement:
    IF '(' expression ')' THEN statement_list ELSE statement_list ENDIF {
        printf("IF-ELSE statement parsed.\n");
    }
    | IF '(' expression ')' THEN statement_list ENDIF {
        printf("IF statement parsed.\n");
    }
    ;

%%
void generate_code(const char *instr, const char *arg1, const char *arg2, const char *result) {
    printf("%s %s, %s, %s\n", instr, arg1, arg2, result);
}

int main() {
    yyparse();
    return 0;
}
