%{
#include<stdio.h>
#include<stdlib.h>
#include "ch3hdr.h"
#include"y.tab.h"
#include<math.h>
#include <string.h>
extern FILE *yyin;
		/*nothing*/
char varchar[100][100];
int count;
double is_arr[100];

void print_var_list()
{
	int i;
	printf("(<var_list> = ");
	for(i = 0 ; i < count ; i++)
	{
		printf("%s", varchar[i]);
		if(is_arr[i] != 0)
		{
			printf("[%.0f]", is_arr[i]);
		}
		if(i != count-1)
		{
			printf(", ");
		}
	}
	printf(")");
}

%}

%union
{
	double dval;
	struct symtab *symp;
	char *str;
}
%token<symp>NAME
%token<dval>NUMBER
%token<str>TYPE
%token PROGRAM
%token IF FOR THEN ELSE TO
%token KW_BEGIN END DECLARE AS 
%token READ WRITE PRINT ENDIF ENDFOR WHILE ENDWHILE
%token ASSIGN EQ NE GE LE GT LT
%left '-' '+'
%left '*' '/'
%nonassoc UMINUS


%type<dval>expression
%%
Prog:	PROGRAM NAME KW_BEGIN statement_list END
	{
		printf("[YACC] reduce: <Prog> -> PROGRAM NAME BEGIN <statement_list> END\n");
		printf("Compilation stops\n");
	}; 
statement_list:	
	statement
	{
		printf("[YACC] reduce: <statement_list> -> <statement>\n");
	}
	|statement_list statement
	{	
		printf("[YACC] reduce: <statement_list> -> <statement_list> <statement>\n");
	}
statement:	
	var_declaration
	{
		printf("[YACC] reduce: <statement> -> <var_delaration>\n");
	}
	|assign	
	{
		printf("[YACC] reduce: <statement> -> <assign>\n");
	}
	|if_statement
	{	
		printf("[YACC] reduce: <statement> -> <if_statement>\n");
	}
	|for_statement
	{
		printf("[YACC] reduce: <statement> -> <for_statement>\n");
	}
	|print_
	{
		printf("[YACC] reduce: <statement -> ,<print>");
	}
var_declaration:	 
	DECLARE var_list AS TYPE';'
	{		
		printf("[YACC] reduce: <var_declaration> -> DECLARE <var_list> AS  TYPE = (DECLARE <var_list>");
		print_var_list();
		printf(" AS %s)\n", $4);
		count = 0;				
	}

assign:
	NAME ASSIGN expression';'
	{
		$1->value = $3;
		printf("[YACC] reduce: NAME := <E> = (%s = %g)\n", $1->name, $3);
	}
	;
if_statement:
	/*nothing*/
	;
for_statement:
	FOR'('assign TO expression')'for_inform ENDFOR
	{
		printf("[YACC] reduce: FOR(assign TO <E>) <for_inform> ENDFOR\n");
	}
	;
for_inform:
	statementlist	
	{
		printf("[YACC] reduce: <for_inform> -> <statementlist>\n");
	}
	;
print_:
	PRINT'('expression')'';'
	{
		printf("%g", $3);
	}

var_list:	
	var_list','NAME'['NUMBER']'
	{
		strcpy(varchar[count], $3->name);
		printf("[YACC] reduce: <var_list> -> <var_list>, NAME[NUMBER](NAME[NUMBER] = %s[%.0f])\n",varchar[count], $5);
		is_arr[count] = $5;
		count++;
		print_var_list();
		printf("\n");
	}
	|var_list','NAME
	{
		strcpy(varchar[count], $3->name);
		printf("[YACC] reduce: <var_list> -> <var_list>, NAME(NAME = %s)\n", varchar[count]);
		count++;
		print_var_list();
		printf("\n");
	}
	|NAME
	{
		strcpy(varchar[count], $1->name);
		printf("[YACC] reduce: <var_list> -> NAME(NAME = %s)\n", varchar[count]);
		count++;
		print_var_list();
		printf("\n");
	}
expression:	expression '+' expression { 
					    	$$ = $1 + $3;
					    	printf("[YACC] reduce: <E> -> <E> + <E> = (%g + %g = %g)\n", $1, $3, $$); 		
					  }
	|	expression '-' expression { 
					    	$$ = $1 - $3;
					    	printf("[YACC] reduce: <E> -> <E> - <E> = (%g - %g = %g)\n", $1, $3, $$); 				  
					  }
	|	expression '*' expression { 
        				    	$$ = $1 * $3; 
					   	 printf("[YACC] reduce: <E> -> <E> * <E> = (%g * %g = %g)\n", $1, $3, $$); 
					  }
	|	expression '/' expression
				{	if($3 == 0.0)
						yyerror("divide by zero");
					else
					    	printf("[YACC] reduce: <E> -> <E> / <E> = (%g / %g = %g)\n", $1, $3, $$); 
						$$ = $1 / $3;
				}
	|	'-' expression %prec UMINUS	{ 
							  $$ = -$2;
					    	  	printf("[YACC] reduce: <E> -> -<E> = %g\n", $$); 
						}
	|	'(' expression ')'	{ 
						$$ = $2;
					    	printf("[YACC] reduce: <E> -> (<E>) = %g\n", $$); 
					}
	|	NUMBER			{
						printf("[YACC] reduce: <E> -> NUMBER = %g\n", $1);
					} 			
	|	NAME			{ 
						$$ = $1->value;
					    	  	printf("[YACC] reduce: <E> -> NAME = %s\n", $1->name); 
					}
	;	
%%

struct symtab *
symlook(s)
char *s;
{
	char *p;
	struct symtab *sp;

	for(sp = symtab; sp < &symtab[NSYMS]; sp++)
	{
		if(sp->name && !strcmp(sp->name, s))
			return sp;

		if(!sp->name)
		{
			sp->name = strdup(s);
			return sp;
		}
	}
	yyerror("Too many symbols");
	exit(1);
}


main(argc, argv)
int argc;
char **argv;
{
	if(argc > 1)
	{
		FILE *file;
		file = fopen(argv[1], "r");
		if(!file)
		{
			fprintf(stderr, "could not open %s\n", argv[1]);
			exit(1);
		}
		yyin = file;
	}
	yyparse();	
	return 0;

}

