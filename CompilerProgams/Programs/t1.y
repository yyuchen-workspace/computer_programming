%token NAME NUMBER
%%

statement:	NAME '=' expression
	|	expression		{ printf("= %d\n", $1); }
	;

expression:	expression '+' expression { $$ = $1 + $3; printf("Rule +\n"); }
	|	expression '-' expression { $$ = $1 - $3; printf("Rule -\n");}
	|	expression '*' expression { $$ = $1 * $3; printf("Rule *\n");}
	|	expression '/' expression
				{		$$ = $1 / $3;
                                                printf("Rule /\n");
				}
	|	'-' expression { $$ = -$2; printf("Rule Uni -\n");}
	|	'(' expression ')'	{ $$ = $2; }
	|	NUMBER			{ $$ = $1; }
	;
%%
