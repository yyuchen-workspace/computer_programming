%{
#include<stdio.h>
#include<stdlib.h>
#include"ch3hdr.h"
#include"y.tab.h"
#include<math.h>
void print_token(const char *token_type, const char *yytext)
{
	printf("Token value is %s\n", yytext);
}

int countline = 1;

%}

%%


[ \t\r]+				{/*ignore*/}
\n					{countline+=1;}
"%%".*\n				{/*ignore this line*/}
[Pp][Rr][Oo][Gg][Rr][Aa][Mm]		{print_token("100", yytext);return PROGRAM;} 
[Bb][Ee][Gg][Ii][Nn]			{print_token("1", yytext);return KW_BEGIN;} 
[Ee][Nn][Dd]				{print_token("2", yytext);return END;}
[Rr][Ee][Aa][Dd]			{print_token("3", yytext);return READ;}
[Ww][Rr][Ii][Tt][Ee]			{print_token("4", yytext);return WRITE;}
[Ii][Ff]				{print_token("25", yytext);return IF;}
[Tt][Hh][Ee][Nn]			{print_token("26", yytext);return THEN;}
[Ee][Ll][Ss][Ee]			{print_token("27", yytext);return ELSE;}
[Ee][Nn][Dd][Ii][Ff]			{print_token("28", yytext);return ENDIF;}
[Ff][Oo][Rr]				{print_token("29", yytext);return FOR;}
[Tt][Oo]				{print_token("30", yytext);return TO;}
[Ee][Nn][Dd][Ff][Oo][Rr]		{print_token("31", yytext);return ENDFOR;}
[Ww][Hh][Ii][Ll][Ee]			{print_token("32", yytext);return WHILE;}
[Ee][Nn][Dd][Ww][Hh][Ii][Ll][Ee]	{print_token("33", yytext);return ENDWHILE;}
[Dd][Ee][Cc][Ll][Aa][Rr][Ee]		{print_token("34", yytext);return DECLARE;}
[Aa][Ss]				{print_token("35", yytext);return AS;}
[Ii][Nn][Tt][Ee][Gg][Ee][Rr]		{print_token("36", yytext);return INTEGER;}
[Rr][Ee][Aa][Ll]			{print_token("37", yytext);return REAL;}
[Ff][Ll][Oo][Aa][Tt]			{print_token("102", yytext);return FLOAT;}
[Pp][Rr][Ii][Nn][Tt]			{print_token("103", yytext);return PRINT;}


[0-9]+\.[0-9]+([eE][-+]?[0-9]+)?		{yylval.dval = atof(yytext);print_token("5", yytext);return NUMBER;}
[0-9]+						{yylval.dval = atof(yytext);print_token("5", yytext);return NUMBER;}
[A-Za-z][A-Za-z0-9]*				{yylval.symp = symlook(yytext);print_token("8", yytext);return NAME;}

\"[^\"]*\"	{print_token("9", yytext);}
"("	{print_token("10", yytext);return '(';}
")"	{print_token("11", yytext);return ')';}
"["	{print_token("100", yytext);return '[';}
"]"	{print_token("101", yytext);return ']';}
";"	{print_token("12", yytext);return ';';}
","	{print_token("13", yytext);return ',';}
":="	{print_token("14", yytext);return ASSIGN;}
"+"	{print_token("15", yytext);return '+';}
"-"	{print_token("16", yytext);return '-';}
"*"	{print_token("17", yytext);return '*';}
"/"	{print_token("18", yytext);return '/';}
"!="	{print_token("19", yytext);return NE;}
">"	{print_token("20", yytext);return GT;}
"<"	{print_token("21", yytext);return LT;}
">="	{print_token("22", yytext);return GE;}
"<="	{print_token("23", yytext);return LE;}
"=="	{print_token("24", yytext);return EQ;}

<<EOF>>	{/*print_token("38", "ScanEof");*/ return 0;}
.	{printf("Lexial Error: Unrecognized token '%s' in line %d\n", yytext, countline);}

%%


