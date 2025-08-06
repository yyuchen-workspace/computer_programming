# 編譯器和標誌
CC = gcc
CFLAGS = -Wall -Wextra -g

# 目標文件名
TARGET = test
SOURCE = test.c

# 默認目標
all: $(TARGET)

# 編譯規則
$(TARGET): $(SOURCE)
	$(CC) $(CFLAGS) $(SOURCE) -o $(TARGET)

# 清理生成的文件
clean:
	rm -f $(TARGET)

# 運行程序
run: $(TARGET)
	./$(TARGET)

# 調試
debug: $(TARGET)
	gdb ./$(TARGET)

# 聲明偽目標（不是實際文件）
.PHONY: all clean run debug