%{
#include<stdio.h>
#include<stdlib.h>
#include "ch3hdr.h"
#include"y.tab.h"
#include<math.h>
#include <string.h>
#include <stdarg.h> 
extern FILE *yyin;
char varchar[100][100];
int count;
extern int countline;

int ForLabel;
int ForIL1;
int ForIL2;
struct symtab *ForVAR;

int labelCount = 0;
int newLabel()
{
    return labelCount++;
}

void generate(const char *fmt, ...)
{
    va_list args;
    va_start(args, fmt);
    printf("GEN: ");
    vprintf(fmt, args);
    printf("\n");
    va_end(args);
}

%}

%union
{
	double dval;
	struct symtab *symp;
}
%token<symp>NAME
%token<dval>NUMBER
%token PROGRAM
%token IF FOR THEN ELSE TO
%token KW_BEGIN END DECLARE AS 
%token READ WRITE PRINT ENDIF ENDFOR WHILE ENDWHILE
%token REAL INTEGER FLOAT
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
	;

statement:	
	var_declaration
	{
		printf("[YACC] reduce: <statement> -> <var_declaration>\n");
	}
	|assign_stmt	
	{
		printf("[YACC] reduce: <statement> -> <assign_stmt>\n");
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
		printf("[YACC] reduce: <statement> -> ,<print>\n");
	}
	;

var_declaration:	 
	DECLARE var_list AS type';'
	{		
		printf("[YACC] reduce: <var_declaration> -> DECLARE <var_list> AS  TYPE = (DECLARE <var_list>\n");
		count = 0;				
	}
	;

type:
	INTEGER
	{
		printf("[YACC] reduce: <type> -> INTEGER\n");
	}
	|REAL
	{
		printf("[YACC] reduce: <type> -> REAL\n");	
	}
	|FLOAT
	{
		printf("[YACC] reduce: <type> -> FLOAT\n");
	}
	;

if_statement:
		IF do_if THEN if_list ENDIF
		{
			printf("[YACC] reduce: if_statement -> IF <if_list> ENDIF\n");
		}
		;

do_if:	
	'('expression compare expression')'
	{
		printf("[YACC] reduce: <do_if> -> (<expression> <compare> <expression>)\n");
	}
	;

if_list:
		ELSE IF statement_list ELSE statement_list
		{
			printf("[YACC] reduce: <if_list> -> ELSE IF <statement_list> ELSE <statement_list>\n");
		}
		|ELSE statement_list
		{
			printf("[YACC] reduce: <if_list> -> ELSE <statement_list>\n");
		}
		|statement_list
		{
			printf("[YACC] reduce: <if_list> -> <statement_list>\n");
		}
		;
compare:
	EQ{printf("[YACC] reduce: <compare> -> EQ\n");}
	|GE{printf("[YACC] reduce: <compare> -> GE\n");}
	|NE{printf("[YACC] reduce: <compare> -> NE\n");}
	|LE{printf("[YACC] reduce: <compare> -> LE\n");}
	|GT{printf("[YACC] reduce: <compare> -> GT\n");}
	|LT{printf("[YACC] reduce: <compare> -> LT\n");}
	;
for_statement:
	FOR range statement_list ENDFOR
	{
		generate("INC %s", ForVAR->name); 
		generate("CMP %s, %f", ForVAR->name, ForIL2); 
		generate("JL L%d", ForLabel); 
		printf("[YACC] reduce: FOR <range> <statement_list> ENDFOR\n");
	}
	;
range:
	'('NAME ASSIGN expression TO expression')' 
	{
		generate("I.store %f, %s", $4, $2->name);  
		ForLabel = newLabel();                  
		generate("LABEL L%d", ForLabel);          
		ForIL1 = $4;                              
		ForVAR = $2;                             
		ForIL2 = $6;                             
	}


assign_stmt:
	NAME ASSIGN expression
	{
		$1->value = $3;
		printf("[YACC] reduce: <assign_stmt> = <assign>;\n");
	}
	;

print_:
	PRINT'('print_list')'';'
	{
		printf("[YACC] reduce: <print_> -> PRINT(expression);\n");
	}
	;

print_list:
	print_list','expression
	{
		printf("[YACC] reduce: <print_list> -> <print_list>,expression\n");
	}
	|expression
	{
		printf("[YACC] reduce: <print_list> -> expression\n");
	}
var_list:	
	|var_list','NAME
	{
		strcpy(varchar[count], $3->name);
		printf("[YACC] reduce: <var_list> -> <var_list>, NAME\n");
		count++;
	}
	|NAME
	{
		strcpy(varchar[count], $1->name);
		printf("[YACC] reduce: <var_list> -> NAME\n");
		count++;
	}
	;
	
expression:	expression '+' expression { 
					    	$$ = $1 + $3;
					    	printf("[YACC] reduce: <E> -> <E> + <E>\n"); 		
					  }
	|	expression '-' expression { 
					    	$$ = $1 - $3;
					    	printf("[YACC] reduce: <E> -> <E> - <E>\n"); 				  
					  }
	|	expression '*' expression { 
        				    	$$ = $1 * $3; 
					   	 printf("[YACC] reduce: <E> -> <E> * <E>\n"); 
					  }
	|	expression '/' expression
				{	if($3 == 0.0)
						yyerror("divide by zero");
					else
					    	printf("[YACC] reduce: <E> -> <E> / <E>\n"); 
						$$ = $1 / $3;
				}
	|	'-' expression %prec UMINUS	{ 
							  $$ = -$2;
					    	  	printf("[YACC] reduce: <E> -> -<E>\n"); 
						}
	|	'(' expression ')'	{ 
						$$ = $2;
					    	printf("[YACC] reduce: <E> -> (<E>)\n"); 
					}

	|	NUMBER			{
						printf("[YACC] reduce: <E> -> NUMBER\n");
					} 			
	|	NAME			{ 
						$$ = $1->value;
					    	  	printf("[YACC] reduce: <E> -> NAME\n"); 
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

