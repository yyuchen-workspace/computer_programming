%{
#include <stdio.h>
%}

%token NAME NUMBER

%%
statement:
      NAME '=' expression
    {
        printf("Yacc: reduce rule 'statement -> NAME = expression'\n");
    }
    | expression
    {
        printf("Yacc: reduce rule 'statement -> expression'\n");
        printf("= %d\n", $1);
    }
    ;

expression:
      expression '+' NUMBER
    {
        printf("Yacc: reduce rule 'expression -> expression + NUMBER'\n");
        $$ = $1 + $3;
    }
    | expression '-' NUMBER
    {
        printf("Yacc: reduce rule 'expression -> expression - NUMBER'\n");
        $$ = $1 - $3;
    }
    | NUMBER
    {
        printf("Yacc: reduce rule 'expression -> NUMBER'\n");
        $$ = $1;
    }
    ;
%%
int main(void) {
    return yyparse();
}
int yyerror(const char *s) {
    fprintf(stderr, "Error: %s\n", s);
    return 0;
}
