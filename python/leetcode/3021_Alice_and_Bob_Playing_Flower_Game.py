# 真正簡潔解法
class Solution(object):
    def flowerGame(self, n, m):
        return (n // 2) * ((m + 1) // 2) + ((n + 1) // 2) * (m // 2)





class Flower_Game():
    def __init__(self, n, m):
        self.x = n
        self.y = m

    def win_sets(self):
        return (self.x // 2) * ((self.y + 1) // 2) + ((self.x + 1) // 2 ) * (self.y // 2)
    
    # 可以算出詳細有哪幾組
    def who_wins(self):
        Alice_win_list = []
        win_count = 0
        for x in range(1, self.x+1):
            for y in range(1, self.y+1):
                if (x + y) % 2:
                    Alice_win_list.append((x, y))   
                    win_count += 1
        return Alice_win_list, win_count


if __name__ == "__main__":
    
    n = int(input("請輸入x路線數字："))
    m = int(input("請輸入y路線數字："))
            
    if n <= 0 or m <= 0:
        print("Error: 1 <= n, m <= 100000")

    
       
    game = Flower_Game(n, m)
    # win_list, win_count = game.who_wins()
    # print(f"Alice有{win_count}種贏的可能, 分別為{win_list}")
    win_count = game.win_sets()
    print(f"Alice有{win_count}種贏的可能")
