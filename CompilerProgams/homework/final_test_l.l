%{
#include "y.tab.h"
#include <ctype.h>
%}

%%
[Pp][Rr][Oo][Gg][Rr][Aa][Mm]      { return PROGRAM; }
[Bb][Ee][Gg][Ii][Nn]               { return BEGIN; }
[Ee][Nn][Dd]                       { return END; }
[Dd][Ee][Cc][Ll][Aa][Rr][Ee]       { return DECLARE; }
[Aa][Ss]                           { return AS; }
[Ii][Nn][Tt][Ee][Gg][Ee][Rr]       { return INTEGER; }
[Ff][Ll][Oo][Aa][Tt]               { return FLOAT; }
[Ff][Oo][Rr]                       { return FOR; }
[Tt][Oo]                           { return TO; }
[Dd][Oo][Ww][Nn][Tt][Oo]           { return DOWNTO; }
[Ee][Nn][Dd][Ff][Oo][Rr]           { return ENDFOR; }
[Ii][Ff]                           { return IF; }
[Tt][Hh][Ee][Nn]                   { return THEN; }
[Ee][Nn][Dd][Ii][Ff]               { return ENDIF; }
[Ee][Ll][Ss][Ee]                   { return ELSE; }
[Pp][Rr][Ii][Nn][Tt]               { return PRINT; }
[A-Za-z_][A-Za-z0-9_]*             { yylval.str = strdup(yytext); return NAME; }
[0-9]+                             { yylval.dval = atof(yytext); return NUMBER; }
"("                                { return '('; }
")"                                { return ')'; }
","                                { return ','; }
";"                                { return ';'; }
"="                                { return '='; }
"+"                                { return '+'; }
"-"                                { return '-'; }
"*"                                { return '*'; }
"/"                                { return '/'; }
"<"                                { return '<'; }
">"                                { return '>'; }
"<="                               { return LE; }
">="                               { return GE; }
"=="                               { return EQ; }
"!="                               { return NE; }
[ \t\n]+                           { /* Ignore whitespace */ }
.                                  { printf("Unknown character: %s\n", yytext); }
%%
