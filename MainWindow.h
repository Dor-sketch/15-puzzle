#include <gtk/gtk.h>
#include <gtkmm.h>
#include "Game.h"

class MainWindow : public Gtk::Window {
public:
  MainWindow();

private:
std::vector<int> moves;
void processNextMove();
void processMove(int tile);
std::vector<std::string> parseSolution(const std::string& solution);
void initControls();
void initButtons();
  void addButton(int i);
  void updateBoard();
  void onShuffle();
  void onSolve();
  void onReset();
  void onQuit();
  void onMove(int index);
  void onSolved();
  void onShuffled();
  Game game;
  Gtk::Grid grid;
  std::array<Gtk::Button, 9> buttons;
  Gtk::Button shuffleButton{"Shuffle"};
  Gtk::Button solveButton{"Solve"};
  Gtk::Button resetButton{"Reset"};
  Gtk::Button quitButton{"Quit"};
  Gtk::Box box{Gtk::ORIENTATION_VERTICAL, 10};
  Gtk::Box buttonBox{Gtk::ORIENTATION_HORIZONTAL, 10};
  Gtk::Label label;
  Gtk::Label movesLabel;
  int moves_count = 0;
  bool isSolving = false;
  bool isShuffling = false;
  bool isResetting = false;
  bool isQuitting = false;
  bool isSolved = false;
  bool isShuffled = false;
  bool isReset = false;
  bool isQuit = false;
  bool isSolve = false;
  bool isShuffle = false;
  bool isMove = false;
  bool isUpdate = false;
  bool isInit = false;
};