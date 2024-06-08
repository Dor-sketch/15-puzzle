#include "Game.h"
#include <random>

const int NUMBER_OF_MOVES = 30;
extern int SIZE;

Game::Game() {
board.resize(SIZE);
std::iota(board.begin(), board.end(), 0); }

void Game::shuffle() {
  // shuffle solvable board by generating random list NUMBER_OF_MOVES long
  static std::random_device rd;
  static std::mt19937 g(rd());
  for (int i = 0; i < NUMBER_OF_MOVES; ++i) {
    std::uniform_int_distribution<> dist(0, SIZE - 1);
    move(dist(g));
  }
}

bool Game::isSolved() const {
  return std::is_sorted(board.begin(), board.end());
}

void Game::reset() { std::iota(board.begin(), board.end(), 0); }

void Game::move(int index) {
  auto root = static_cast<int>(std::sqrt(SIZE));
  if (index % root > 0 && board[index - 1] == 0) {
    std::swap(board[index], board[index - 1]);
  } else if (index % root < root - 1 && board[index + 1] == 0) {
    std::swap(board[index], board[index + 1]);
  } else if (index / root > 0 && board[index - root] == 0) {
    std::swap(board[index], board[index - root]);
  } else if (index / root < root - 1 && board[index + root] == 0) {
    std::swap(board[index], board[index + root]);
  }
}
