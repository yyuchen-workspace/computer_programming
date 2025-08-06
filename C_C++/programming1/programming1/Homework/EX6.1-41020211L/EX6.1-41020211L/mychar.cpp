int islower2(int ch)
{
    return (ch >= 'a' && ch <= 'z');
}

int isupper2(int ch)
{
    return (ch >= 'A' && ch <= 'Z');
}

int isalpha2(int ch)
{
    return (islower2(ch) || isupper2(ch));
}

int isdigit2(int ch)
{
    return (ch >= '0' && ch <= '9');
}

int toupper2(int ch)
{
    if (islower2(ch))
    {
        return ch - ('a' - 'A');
    }
    return ch;
}

int tolower2(int ch)
{
    if (isupper2(ch))
    {
        return ch + ('a' - 'A');
    }
    return ch;
}

