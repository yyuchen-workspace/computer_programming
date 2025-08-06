%{
#include "ch3hdr.h"
#include <string.h>
%}

%union {
	double dval;
	struct symtab *symp;
}
%token <symp> NAME
%token <dval> NUMBER
%left '-' '+'
%left '*' '/'
%nonassoc UMINUS

%type <dval> expression
%%
statement_list:	statement '\n'
	|	statement_list statement '\n'
	;

statement:	NAME '=' expression	{ $1->value = $3; }
	|	expression		{ printf("[YACC] R1 reduce: <STMT> -> <E> = (result = %g)\n", $1); }
	;

expression:	expression '+' expression { 
					    	$$ = $1 + $3;
					    	printf("[YACC] R2 reduce: <E> -> <E> + <E> = (%g + %g = %g)\n", $1, $3, $$); 		
					  }
	|	expression '-' expression { 
					    	$$ = $1 - $3;
					    	printf("[YACC] R3 reduce: <E> -> <E> - <E> = (%g - %g = %g)\n", $1, $3, $$); 				  
					  }
	|	expression '*' expression { 
        				    	$$ = $1 * $3; 
					   	 printf("[YACC] R4 reduce: <E> -> <E> * <E> = (%g * %g = %g)\n", $1, $3, $$); 
					  }
	|	expression '/' expression
				{	if($3 == 0.0)
						yyerror("divide by zero");
					else
					    	printf("[YACC] R5 reduce: <E> -> <E> / <E> = (%g / %g = %g)\n", $1, $3, $$); 
						$$ = $1 / $3;
				}
	|	'-' expression %prec UMINUS	{ 
							  $$ = -$2;
					    	  	printf("[YACC] R6 reduce: <E> -> -<E> = %g\n", $$); 
						}
	|	'(' expression ')'	{ 
						$$ = $2;
					    	printf("[YACC] R7 reduce: <E> -> (<E>) = %g\n", $$); 
					}
	|	NUMBER			{
						printf("[YACC] R8 reduce: <E> -> NUMBER = %g\n", $1);
					} 			
	|	NAME			{ 
						$$ = $1->value;
					    	  	printf("[YACC] R9 reduce: <E> -> NAME = (%g = %s -> value)\n", $$, $1->name); 
					}
	;
%%
/* look up a symbol table entry, add if not present */
struct symtab *
symlook(s)
char *s;
{
	char *p;
	struct symtab *sp;
	
	for(sp = symtab; sp < &symtab[NSYMS]; sp++) {
		/* is it already here? */
		if(sp->name && !strcmp(sp->name, s))
			return sp;
		
		/* is it free */
		if(!sp->name) {
			sp->name = strdup(s);
			return sp;
		}
		/* otherwise continue to next */
	}
	yyerror("Too many symbols");
	exit(1);	/* cannot continue */
} /* symlook */
