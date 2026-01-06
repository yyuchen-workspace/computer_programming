#include <iostream>
#include <string>


using namespace std;

class Fish {
public:
	int body_len;
	double fishbone;
	std::string name;
    
	void swim() {
		cout << name << " can swim" << endl;
	}

    // Constructor: 在這邊定義物件成員的初始狀態
	Fish(){
		body_len = 1;
		fishbone = 80.2;
		name = "the fish";
	}

    // Destructor: 在物件消失時，會執行裡面的內容
	~Fish() {
		cout << "bye~" << endl;
	}

} big_fish;



int main()
{
	Fish shark; //初始化呼叫destructor函數
	
	cout << "shark body len is: " << shark.body_len << endl;
	cout << "big_fish body len is: " << big_fish.body_len << endl;
	shark.swim();

    // 在main函數結束時，會呼叫兩次Fish的destructor函數
}





