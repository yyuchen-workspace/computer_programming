#include <iostream>
using namespace std;

// 函式指標的前置宣告
int add(int a, int b);
int multiply(int a, int b);

struct Student {
    string name;
    int age;
    
    // 使用 'this' 指標的方法
    void displayInfo() {
        cout << "姓名: " << this->name << ", 年齡: " << this->age << endl;
        // 'this->name' 等同於 'name'
        // 'this' 是指向目前物件的指標
    }
    
    // 明確使用 this 的方法
    Student* setAge(int newAge) {
        this->age = newAge;
        return this;  // 回傳目前物件的指標，支援方法鏈式呼叫
    }
};

int main() {
    cout << "=== C++ 指標完整教學 ===" << endl << endl;
    
    // 1. 基礎指標
    cout << "1. 基礎指標:" << endl;
    int number = 42;
    int* ptr = &number;  // ptr 儲存 number 的記憶體位址
    
    cout << "number = " << number << endl;
    cout << "&number = " << &number << " (number的位址)" << endl;
    cout << "ptr = " << ptr << " (儲存位址)" << endl;
    cout << "*ptr = " << *ptr << " (解參考 - 取得數值)" << endl;
    
    *ptr = 100;  // 透過指標改變數值
    cout << "執行 *ptr = 100 後, number = " << number << endl << endl;
    
    // 2. 指向指標的指標 (雙重指標)
    cout << "2. 指向指標的指標:" << endl;
    int value = 25;
    int* firstPtr = &value;         // firstPtr 指向 value
    int** secondPtr = &firstPtr;    // secondPtr 指向 firstPtr
    
    cout << "value = " << value << endl;
    cout << "*firstPtr = " << *firstPtr << endl;
    cout << "**secondPtr = " << **secondPtr << " (雙重解參考)" << endl;
    
    **secondPtr = 50;  // 透過雙重指標改變數值
    cout << "執行 **secondPtr = 50 後, value = " << value << endl;
    
    cout << "位址關係:" << endl;
    cout << "&value = " << &value << endl;
    cout << "firstPtr = " << firstPtr << endl;
    cout << "&firstPtr = " << &firstPtr << endl;
    cout << "secondPtr = " << secondPtr << endl << endl;
    
    // 3. 陣列指標
    cout << "3. 陣列指標:" << endl;
    int arr[5] = {10, 20, 30, 40, 50};
    int* arrPtr = arr;  // arr 等同於 &arr[0]
    
    cout << "使用陣列表示法存取元素:" << endl;
    for (int i = 0; i < 5; i++) {
        cout << "arr[" << i << "] = " << arr[i] << endl;
    }
    
    cout << "\n使用指標算術存取元素:" << endl;
    for (int i = 0; i < 5; i++) {
        cout << "*(arrPtr + " << i << ") = " << *(arrPtr + i) << endl;
    }
    
    // 指向整個陣列的指標 (不同於指向第一個元素的指標)
    int (*ptrToArray)[5] = &arr;  // 指向整個陣列
    cout << "\narr 和 &arr 的差異:" << endl;
    cout << "arr = " << arr << " (指向第一個元素)" << endl;
    cout << "&arr = " << &arr << " (指向整個陣列)" << endl;
    cout << "ptrToArray = " << ptrToArray << endl;
    cout << "(*ptrToArray)[2] = " << (*ptrToArray)[2] << endl << endl;
    
    // 4. 結構體和 'this' 指標
    cout << "4. 結構體和 'this' 指標:" << endl;
    Student student1;
    student1.name = "小明";
    student1.age = 20;
    
    cout << "student1 的位址: " << &student1 << endl;
    student1.displayInfo();  // 在此方法內，'this' 指向 student1
    
    // 使用 'this' 進行方法鏈式呼叫
    Student* result = student1.setAge(21);
    cout << "執行 setAge(21) 後: ";
    student1.displayInfo();
    cout << "setAge 回傳的指標: " << result << endl;
    cout << "它們是同一個嗎? " << (result == &student1 ? "是" : "否") << endl << endl;
    
    // 5. 函式指標
    cout << "5. 函式指標:" << endl;
    
    // 宣告函式指標
    int (*operation)(int, int);  // 指向接受兩個int參數並回傳int的函式的指標
    
    // 指派函式位址
    operation = add;  // 或寫成 operation = &add; (兩種都可以)
    int sum = operation(15, 25);  // 透過指標呼叫函式
    cout << "15 + 25 = " << sum << " (使用 add 函式指標)" << endl;
    
    operation = multiply;  // 改為指向不同的函式
    int product = operation(6, 7);
    cout << "6 * 7 = " << product << " (使用 multiply 函式指標)" << endl;
    
    // 函式指標陣列
    int (*operations[2])(int, int) = {add, multiply};
    cout << "\n使用函式指標陣列:" << endl;
    cout << "operations[0](10, 5) = " << operations[0](10, 5) << endl;
    cout << "operations[1](10, 5) = " << operations[1](10, 5) << endl;
    
    // 函式指標作為參數
    auto calculator = [](int a, int b, int (*func)(int, int)) {
        return func(a, b);
    };
    
    cout << "\n將函式指標作為參數:" << endl;
    cout << "calculator(8, 3, add) = " << calculator(8, 3, add) << endl;
    cout << "calculator(8, 3, multiply) = " << calculator(8, 3, multiply) << endl << endl;
    
    // 6. 綜合範例 - 學生管理系統
    cout << "6. 綜合範例:" << endl;
    
    // TODO(human): 在此實作學生管理系統
    
    return 0;
}

// 函式實作
int add(int a, int b) {
    return a + b;
}

int multiply(int a, int b) {
    return a * b;
}