int if_hit_the_wall(int move, unsigned char computer_x, unsigned char computer_y)
{
    bool go = false;
    while(!go)
    {
        if((computer_x == 1 && computer_y == 1 && (move == 0 || move == 2)) ||    //左上
            (computer_x == map_size - 2 && computer_y == 1 && (move == 1 || move == 3)) ||  //右下
            (computer_x == 1 && computer_y == map_size - 2 && (move == 0 || move == 3)) ||  //右上
            (computer_x == map_size - 2 && computer_y == map_size - 2 && (move == 1 || move == 2)) ||   //左下
            (computer_x == 1 && move == 0) ||  //上
            (computer_x == map_size - 2 && move == 1) ||   //下
            (computer_y == 1 && move == 2) ||  //左
            (computer_y == map_size - 2 && move == 3))  //右
        {
           move = rand() % 4;
        }
        else
        {
            go = true;
        }
    }
    return move;
}







int if_hit_the_wall(int move, unsigned char computer_x, unsigned char computer_y)
{
    bool valid_moves[4] = {true, true, true, true}; // 初始所有方向都合法

    // 检查每个方向是否撞墙
    if (computer_x == 1) valid_moves[0] = false; // 不能向上
    if (computer_x == map_size - 2) valid_moves[1] = false; // 不能向下
    if (computer_y == 1) valid_moves[2] = false; // 不能向左
    if (computer_y == map_size - 2) valid_moves[3] = false; // 不能向右

    // 如果当前位置在角落，进一步限制方向
    if (computer_x == 1 && computer_y == 1)
    { // 左上角
        valid_moves[0] = valid_moves[2] = false;
    }
    else if (computer_x == 1 && computer_y == map_size - 2)
    { // 右上角
        valid_moves[0] = valid_moves[3] = false;
    }
    else if (computer_x == map_size - 2 && computer_y == 1)
    { // 左下角
        valid_moves[1] = valid_moves[2] = false;
    }
    else if (computer_x == map_size - 2 && computer_y == map_size - 2)
    { // 右下角
        valid_moves[1] = valid_moves[3] = false;
    }

    // 随机选择一个合法方向
    while (!valid_moves[move])
    {
        move = rand() % 4; // 随机生成新的方向
    }

    return move;
}





///
int if_hit_the_wall(int move, unsigned char computer_x, unsigned char computer_y)
{

}

bool valid_move[4] = {true, true, true, true};
    if(computer_x == 1) valid_move[0] = false;//不能往上
    if(computer_x == map_size - 2) valid_move[1] = false;//不能往下
    if(computer_y == 1) valid_move[2] = false;//不能往上
    if(computer_y == map_size - 2) valid_move[3] = false;//不能往下

    bool has_valid_move = false;
    for(int i = 0 ; i < 4 ; ++i)
    {
        if(valid_move[i])
        {
            has_valid_move = true;
            break;
        }
    }

    if(!has_valid_move)
    {
        return move;
    }

    while(!valid_move[move])
    {
        move = rand() % 4;
    }

    return move;


