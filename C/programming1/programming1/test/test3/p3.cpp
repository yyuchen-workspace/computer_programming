#include<stdio.h>
#include<string.h>

char GetDirection(int x, int y, int nx, int ny)
{
    if(nx > x && ny == y)
    {
        return 'E';
    }
    else if(ny > y  && nx == x)
    {
        return 'N';
    }
    else if(nx < x && ny == y)
    {
        return 'W';
    }
    else if(ny < y && nx == x)
    {
        return 'S';
    }
}

char GetTurn(int odir, int ndir)
{
    if(odir == ndir)
    {
        return '-';
    }
    else if(odir == 'E')
    {
        if(ndir == 'N')
        {
            return 'L';
        }
        if(ndir == 'S')
        {
            return 'R';
        }
    }
    else if(odir == 'W')
    {
        if(ndir == 'N')
        {
            return 'R';
        }
        if(ndir == 'S')
        {
            return 'L';
        }
    }
    else if(odir == 'N')
    {
        if(ndir == 'E')
        {
            return 'R';
        }
        if(ndir == 'W')
        {
            return 'L';
        }
    }
    else if(odir == 'S')
    {
        if(ndir == 'E')
        {
            return 'L';
        }
        if(ndir == 'W')
        {
            return 'R';
        }
    }
}

int main()
{
    int odir = 'E', ndir;
    char go = '-';
    int left = 0, right = 0;
    int x, y;
    int nx, ny;
    int t;
    scanf("%d", &t);
    scanf("%d%d", &x, &y);
    for(int T = 0 ; T < t - 1; T++)
    {
        scanf("%d%d", &nx, &ny);
        ndir = GetDirection(x, y, nx, ny);
        go = GetTurn(odir, ndir);
        if(go == 'L')
        {
            left += 1;
        }
        else if(go == 'R')
        {
            right+=1;
        }
        x = nx;
        y = ny;
        odir = ndir;
    }

    printf("%d %d\n", left, right);

}
