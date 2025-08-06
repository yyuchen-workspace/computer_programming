%{
#include "y.tab.h"
#include <stdio.h>
#include <stdlib.h>

extern int yylval;
%}

%%
[0-9]+  {
            yylval = atoi(yytext);
            printf("Lex: recognized NUMBER (%s)\n", yytext);
            return NUMBER;
        }
[ \t]   ;   /* ignore white space */
\n      return 0;    /* logical EOF */
.       {
            printf("Lex: recognized character '%s'\n", yytext);
            return yytext[0];
        }
%%
