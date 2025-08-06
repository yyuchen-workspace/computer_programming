#include<stdio.h>
#include<stdlib.h>
#include<stdbool.h>
#include<time.h>

// ---------- Initialization ---------
    constexpr int NumMonsters = 5;
int main()
{
    int monster[NumMonsters] = {0};
    int player_life = 30;
    for (int i=0; i<NumMonsters; i+=1)
    {
         monster[i] = 10;
    }

    // ---------- Game starts ---------
    int die = 0;
    int num;

    while(die < NumMonsters)
    {
        // ---------- Show game state ---------

        system("cls");
        printf("***Monster Hunting Game***\n\n");
        for (int i=0; i<NumMonsters; i+=1)
        {
            printf("Monster %d", i+1, monster[i]);
            if(monster[i] <= die)
            {
                printf("-DEAD-");
            }
            else
            {
                printf("(%d)", monster[i]);
                for(int j = 0 ; j < monster[i] ; j++)
                {
                    printf("*");
                }
            }
            printf("\n");
        }
        printf("\n");
        printf("Player's life: (%d)", player_life);
        for(int i = 0 ; i < player_life ; i++)
        {
            printf("*");
        }
        printf("\n");
        // ---------- Player's turn ---------
        bool win = true;
        bool is_attack = false;
        int attack = 0;
        int player_hit = 0, monster_hit = 0;
        srand(time(0));
        printf("\033[38;2;173;216;230mPlayer's turn: (1) single attack ( 7 P) (2) group attack ( 2 P)...>\033[0m");
        scanf("%d", &attack);
        while(!is_attack)
        {
            if(attack == 1)
            {
                printf("Which monster do you want to attack?...>");
                scanf("%d", &num);
                if(num > NumMonsters || num < 0)
                {
                    printf("Please enter Monster number (1 ~ %d)...>", NumMonsters);

                    scanf("%d", &num);
                }
                num -= 1;
                player_hit = rand() % 10;

                if(monster[num] > 0)
                {
                    if(player_hit > 2)//20% hit
                    {
                        monster[num] -= 7;
                        printf("You hit monster %d by 7 points!\n", num+1);
                    }
                    else
                    {
                        printf("\033[38;2;0;255;0mMissed! You do not hit Monster %d\033[0m\n", num+1);
                    }
                    is_attack = true;
                }

                for(int i = 0 ; i < NumMonsters ; i++)
                {
                    if(monster[i] != 0)
                    {
                        win = false;
                    }
                }
                if(win)
                {
                    printf("You have killed all monsters!\n");
                }

            }
            else if(attack == 2)
            {
                printf("You hit all monsters by 2 points!\n");
                for(int i = 0 ; i < NumMonsters ; i++)
                {
                    if(monster[i] > 0)
                    {
                        monster[i] -= 2;
                        is_attack = true;
                    }
                }
                for(int i = 0 ; i < NumMonsters ; i++)
                {
                    if(monster[i] > 0)
                    {
                        win = false;
                    }

                }
                if(win)
                {
                    printf("You have killed all monsters!\n");
                    system("pause");
                    return 0;
                }
            }
            else//輸入非1、2
            {
                printf("Error: Please enter (1)single attack<7P> (2)group attack<2P>...>");
                scanf("%d", &attack);
            }
        }
        system("pause");
        //monsters

        bool is_heal = false;
        for(int i = 0 ; i < NumMonsters ; i++)
        {
            if(monster[i] > 0)
            {
                monster_hit = rand() % 10;
                is_heal = false;
                for(int j = 0 ; j < NumMonsters ; j++)//確認血量，是否回血
                {
                    if(monster[j] <= 3 && monster[j] > 0)
                    {

                        monster[j] += 1;
                        printf("\033[38;2;255;0;255mMonster %d heals monster %d by 1 point\033[0m\n", i+1, j+1);
                        is_heal = true;
                        break;
                    }
                }
                if(!is_heal)//沒有回血則攻擊
                {
                    if(monster_hit > 1)//10% hit 1HP
                    {
                        printf("Monster %d hits you by 1 point!\n", i+1);
                        player_life -= 1;
                    }
                    else
                    {
                        printf("\033[38;2;255;255;0mCombo hit! monster %d hits you by 3 points!\033[0m\n", i+1);
                        player_life -= 3;
                    }
                }
            }
            if(player_life <= die)
            {
                printf("\033[38;2;255;0;0mOh no, you are killed.\033[0m\n");
                system("pause");
                return 0;
            }
        }



        // ---------- Stopping criterion ---------
        system("pause");
    }
    // ---------- Game ends ---------


    return 0;
}
