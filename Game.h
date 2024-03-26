#include <algorithm>
#include <array>
#include <random>

class Game {
public:
  Game();
  void shuffle();
  bool isSolved() const;
  int operator[](int index) const { return board[index]; }
  void move(int index);
    const std::string solve();
    void quit();
    void update();
    void init();
    void reset();
    const std::array<int, 9>& getBoard() const { return board; }
private:
      // the solution path
  std::array<int, 9> board;
};
