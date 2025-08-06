%{
double vbltable[26];
%}

%union {
	double dval;
	int vblno;
}

%token <vblno> NAME
%token <dval> NUMBER
%left '-' '+'
%left '*' '/'
%nonassoc UMINUS

%type <dval> expression
%%
statement_list:	statement '\n'
	|	statement_list statement '\n'
	;

statement:	NAME '=' expression	{ vbltable[$1] = $3;
                                          printf("statement type 1\n"); 
                                           printf("Do assignment\n");}
	|	expression		{  printf("statement type 2\n"); 
                                           printf("= %g\n", $1); }
	;

expression:	expression '+' expression { $$ = $1 + $3; }
	|	expression '-' expression { $$ = $1 - $3; }
	|	expression '*' expression { $$ = $1 * $3; }
	|	expression '/' expression
				{	if($3 == 0.0)
						yyerror("divide by zero");
					else
						$$ = $1 / $3;
				}
	|	'-' expression %prec UMINUS	{ $$ = -$2; }
	|	'(' expression ')'	{ $$ = $2; }
	|	NUMBER
	|	NAME			{ $$ = vbltable[$1]; }
	;
%%
