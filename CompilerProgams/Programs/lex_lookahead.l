%{
%}
spa [ \t\n]*
digit [0-9]+
var [a-zA-Z][a-zA-Z0-9]*
%%
{spa}	;
DO/({spa}{digit}{spa}{var}{spa}={spa}{digit}{spa},)     {return 1;}
{var}   {return 2;}
{digit}	{return 3;}
{digit}\.{digit}	{return 4;}
","	{return 5;}
"="	{return 6;}
%%
main(int argc,char** argv){
	int i;
	FILE *fp;
/*	fp=fopen(argv[1],"r");
	yyin=fp;*/
        while(i=yylex()){
	        printf("%s is a token,num is %d\n",yytext,i);
	}
}



