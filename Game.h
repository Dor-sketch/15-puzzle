#pragma once

#include <array>
#include "tiles.h"

class Game {
public:
  Game();
  int operator[](int index) const { return board[index]; }
  const std::array<int, SIZE> &getBoard() const { return board; }
  bool isSolved() const;
  void shuffle();
  void move(int index);
  void update();
  void reset();
  void quit();

private:
  std::array<int, SIZE> board;
};
