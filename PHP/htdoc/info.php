<?php
// 定義 Person 類別
class Person {
    public $firstName;
    public $lastName;

    public function __construct($firstName, $lastName) {
        $this->firstName = $firstName;
        $this->lastName = $lastName;
    }
}

// 建立總統名單
$presidents[] = new Person('A', 'B');
$presidents[] = new Person('C', 'D');
$presidents[] = new Person('E', 'F');
$presidents[] = new Person('G', 'H');
$presidents[] = new Person('I', 'J');

// 定義排序函數
function presidential_sorter($left, $right) {
    return [$left->lastName, $left->firstName]
         <=>
         [$right->lastName, $right->firstName];
}

// 使用 usort 排序
usort($presidents, 'presidential_sorter');

// 顯示排序結果
foreach ($presidents as $president) {
    echo $president->lastName . ', ' . $president->firstName . PHP_EOL;
}
?>
