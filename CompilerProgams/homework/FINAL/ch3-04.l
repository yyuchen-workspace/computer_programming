%{
#include "y.tab.h"
#include "ch3hdr.h"
#include <math.h>
%}

%%
([0-9]+|([0-9]*\.[0-9]+)([eE][-+]?[0-9]+)?) {
		yylval.dval = atof(yytext);
		printf("[LEX] Got Token = %f\n", yylval.dval);
		return NUMBER;
	}

[ \t]	;		 /* ignore white space */

[A-Za-z][A-Za-z0-9]*	{	/* return symbol pointer */
		yylval.symp = symlook(yytext);
		printf("[LEX] Got Token = %s\n", yytext);
		return NAME;
	}

"$"	{ return 0; }

\n	|
.	return yytext[0];
