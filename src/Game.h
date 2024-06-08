#pragma once

#include <array>
#include <vector>
extern int SIZE;

class Game {
public:
  Game();
  int operator[](int index) const { return board[index]; }
  const std::vector<int> &getBoard() const { return board; }
  bool isSolved() const;
  void shuffle();
  void move(int index);
  void update();
  void reset();
  void quit();

private:
  std::vector<int> board;
};
