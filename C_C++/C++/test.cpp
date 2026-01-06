#include <iostream>
using namespace std;
constexpr int NAME = 10;
class Fish {
public:
	int body_len;
	char name[NAME] = {};
    double length;
	void swim() {
		cout << name << " can swim" << endl;
	}

    // Constructor: 在這邊定義物件成員的初始狀態
	Fish(){
		body_len = 1;
		strcpy_s(name, sizeof(name), "the fish");
		fishbone = 80.2;
	}

    // Destructor: 在物件消失時，會執行裡面的內容
	~Fish() {
		cout << "bye~" << endl;
	}

	// overloading: 不一定只有上面建構子預設的數值，也可以透過多載讓使用者自定義預設數值
    //好處是可以根據傳入的參數類型來決定要呼叫哪一個建構子
	Fish(int body){
		body_len = body;
	}

    Fish(int body, double len){
        body_len = body;
        length = len;
    }


	Fish(int body, double len, char *name_str){
        body_len = body;
        length = len;
		strcpy_s(name, sizeof(name), name_str);
    }


private:
	double fishbone;


protected:
    int age;

} big_fish;



int main()
{
	Fish shark;
	/*shark.body_len = 20;

	big_fish.body_len = 99;*/

	cout << "shark body len is: " << shark.body_len << endl;
	cout << "big_fish body len is: " << big_fish.body_len << endl;
	shark.swim();

    Fish goldfish(10);
    cout << "goldfish body len is: " << goldfish.body_len << endl;
   

    Fish catfish(5, 3.5, "catfish");
    cout << "catfish body len is: " << catfish.body_len << endl;
    cout << "goldfish body length is: " << catfish.length << endl;
	printf("My name is %s\n", catfish.name);


    // 在main函數結束時，會呼叫兩次Fish的destructor函數
}