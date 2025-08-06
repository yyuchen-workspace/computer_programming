%{
/*
 * this sample demonstrates (very) simple recognition:
 * a verb/not a verb.
 */

%}
%%

[\t ]+		/* ignore white space */ ;

is |
am |
are |
were |
was |
be |
being |
been |
do |
does |
did |
will |
would |
should |
can |
could |
has |
have |
had |
go		{
		return 1; }

[a-zA-Z]+ 	{ return 2; }

.|\n     	{  
                   printf ("(%s)\n",yytext); 
                    /* normal default anyway */ }
%%

main()
{
 int i;
 
 i=yylex();
 printf("return value is %d, token is %s\n", i,yytext);
 
 i=yylex();
 printf("return value is %d, token is %s\n", i,yytext);
 
 i=yylex();
 printf("return value is %d, token is %s\n", i,yytext);
}



