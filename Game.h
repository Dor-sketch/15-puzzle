#pragma once

#include <array>

class Game {
public:
  Game();
  int operator[](int index) const { return board[index]; }
  const std::array<int, 9> &getBoard() const { return board; }
  bool isSolved() const;
  void shuffle();
  void move(int index);
  void update();
  void reset();
  void quit();

private:
  std::array<int, 9> board;
};
