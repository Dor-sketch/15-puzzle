#pragma once

#include "FallingCharsWidget.h"
#include "Game.h"
#include <gtk/gtk.h>
#include <gtkmm.h>

class MainWindow : public Gtk::Window {
public:
  MainWindow();

private:
  std::vector<std::string> parseSolution(const std::string &solution);
  void initMenuBar();
  void initButtons();
  void start();
  void processNextMove();
  void processMove(int tile);
  void addButton(int i);
  void updateBoard();
  void onShuffle();
  void onSolve();
  void onReset();
  void onQuit();
  void onMove(int index);
  void onSolved();
  void onShuffled();
  void onTheme();
  char randomCharacter();

  bool isSolved = false;
  bool isShuffled = false;
  std::vector<FallingCharsWidget> fallingCharsWidgets;
  std::vector<int> moves;
  std::array<Gtk::Overlay, 9> overlays;
  Gtk::MenuBar menuBar;
  Gtk::Grid grid;
  Gtk::Label label;
  Gtk::Label movesLabel;
  std::array<Gtk::Button, 9> buttons;
  Gtk::Button shuffleButton{"Shuffle"};
  Gtk::Button solveButton{"Solve"};
  Gtk::Button resetButton{"Reset"};
  Gtk::Button quitButton{"Quit"};
  Gtk::Box box{Gtk::ORIENTATION_VERTICAL, 10};
  Gtk::Box buttonBox{Gtk::ORIENTATION_HORIZONTAL, 10};
  Game game;
};