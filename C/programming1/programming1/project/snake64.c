#include <SFML/Graphics.hpp>
#include <SFML/Window.hpp>
#include <SFML/System.hpp>
#include <cstdlib>
#include <ctime>
#include <vector>

#define map_size 17

enum Direction { UP, DOWN, LEFT, RIGHT };

const int tileSize = 32; // 每個方格的大小（像素）

struct SnakeSegment {
    int x, y;
};

std::vector<SnakeSegment> snake = {{8, 8}}; // 初始化蛇的位置
Direction currentDirection = RIGHT;
bool grow = false;
sf::Vector2i foodPos;

void generateFood() {
    foodPos.x = std::rand() % (map_size - 2) + 1;
    foodPos.y = std::rand() % (map_size - 2) + 1;

    for (const auto& segment : snake) {
        if (segment.x == foodPos.x && segment.y == foodPos.y) {
            generateFood(); // 如果食物生成在蛇身上，重新生成
            return;
        }
    }
}

bool isAlive() {
    const SnakeSegment& head = snake[0];

    // 撞牆
    if (head.x <= 0 || head.x >= map_size - 1 || head.y <= 0 || head.y >= map_size - 1) {
        return false;
    }

    // 撞到自己
    for (size_t i = 1; i < snake.size(); ++i) {
        if (head.x == snake[i].x && head.y == snake[i].y) {
            return false;
        }
    }

    return true;
}

void moveSnake() {
    SnakeSegment newHead = snake[0];

    // 移動頭部
    switch (currentDirection) {
        case UP:    newHead.y -= 1; break;
        case DOWN:  newHead.y += 1; break;
        case LEFT:  newHead.x -= 1; break;
        case RIGHT: newHead.x += 1; break;
    }

    // 檢查是否吃到食物
    if (newHead.x == foodPos.x && newHead.y == foodPos.y) {
        grow = true;
        generateFood();
    }

    // 插入新頭部
    snake.insert(snake.begin(), newHead);

    if (!grow) {
        // 移除尾巴
        snake.pop_back();
    } else {
        grow = false;
    }
}

int main() {
    // 初始化 SFML
    sf::RenderWindow window(sf::VideoMode(map_size * tileSize, map_size * tileSize), "Snake Game");
    window.setFramerateLimit(10);

    // 初始化隨機數
    std::srand(static_cast<unsigned>(std::time(nullptr)));
    generateFood();

    // 矩形形狀，用於渲染牆壁、蛇、食物
    sf::RectangleShape tile(sf::Vector2f(tileSize - 2, tileSize - 2)); // 留空隙作為邊框

    while (window.isOpen()) {
        // 處理事件
        sf::Event event;
        while (window.pollEvent(event)) {
            if (event.type == sf::Event::Closed) {
                window.close();
            } else if (event.type == sf::Event::KeyPressed) {
                if (event.key.code == sf::Keyboard::W && currentDirection != DOWN) {
                    currentDirection = UP;
                } else if (event.key.code == sf::Keyboard::S && currentDirection != UP) {
                    currentDirection = DOWN;
                } else if (event.key.code == sf::Keyboard::A && currentDirection != RIGHT) {
                    currentDirection = LEFT;
                } else if (event.key.code == sf::Keyboard::D && currentDirection != LEFT) {
                    currentDirection = RIGHT;
                }
            }
        }

        // 移動蛇
        moveSnake();

        // 檢查是否死亡
        if (!isAlive()) {
            window.close();
            break;
        }

        // 渲染
        window.clear(sf::Color::Black);

        // 畫牆
        tile.setFillColor(sf::Color::White);
        for (int i = 0; i < map_size; ++i) {
            tile.setPosition(i * tileSize, 0);
            window.draw(tile);
            tile.setPosition(i * tileSize, (map_size - 1) * tileSize);
            window.draw(tile);

            tile.setPosition(0, i * tileSize);
            window.draw(tile);
            tile.setPosition((map_size - 1) * tileSize, i * tileSize);
            window.draw(tile);
        }

        // 畫食物
        tile.setFillColor(sf::Color::Red);
        tile.setPosition(foodPos.x * tileSize, foodPos.y * tileSize);
        window.draw(tile);

        // 畫蛇
        tile.setFillColor(sf::Color::Green);
        for (const auto& segment : snake) {
            tile.setPosition(segment.x * tileSize, segment.y * tileSize);
            window.draw(tile);
        }

        window.display();
    }

    return 0;
}
