#include<iostream>

using namespace std;

class Fish{

    int body_len;
    double fishbone;
    std::string fish_name;

    public: 
        void swim(){
            cout << fish_name << " can swim" << endl;
        }

        Fish(){
            body_len = 1;
            fishbone = 80.2;
            fish_name = "the fish";
        }


        Fish(int body, double bone, char *fish_name){
            body_len = body;
            fishbone = bone;
            this->fish_name = fish_name;
        }
        
}big_fish;

int main(){
    Fish shark;
    Fish goldfish(10, 8.5, "goldfish");

    cout << "fish name is: " << goldfish.fish_name << endl;


}




