#include <algorithm>
#include <array>
#include <random>
#include "Game.h"
#include <iostream>
#include <sstream>
#include <gtk/gtk.h>

const int NUMBER_OF_MOVES = 10;

Game::Game(){ std::iota(board.begin(), board.end(), 0); }

void Game::shuffle() {
  // shuffle solvable board by generating random list NUMBER_OF_MOVES long
    static std::random_device rd;
    static std::mt19937 g(rd());
    for (int i = 0; i < NUMBER_OF_MOVES; ++i) {
        std::uniform_int_distribution<> dist(0, 8);
        move(dist(g));
    }

}


bool Game::isSolved() const {
  return std::is_sorted(board.begin(), board.end());
}

void Game::reset() {
  std::iota(board.begin(), board.end(), 0);
}



void Game::move(int index) {
  if (index % 3 > 0 && board[index - 1] == 0) {
    std::swap(board[index], board[index - 1]);
  } else if (index % 3 < 2 && board[index + 1] == 0) {
    std::swap(board[index], board[index + 1]);
  } else if (index / 3 > 0 && board[index - 3] == 0) {
    std::swap(board[index], board[index - 3]);
  } else if (index / 3 < 2 && board[index + 3] == 0) {
    std::swap(board[index], board[index + 3]);
  }
  // update main window
}
