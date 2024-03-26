#include <gtk/gtk.h>
#include <gtkmm.h>
#include "Game.h"

class FallingCharsWidget : public Gtk::DrawingArea {
public:
  FallingCharsWidget() {
    Glib::signal_timeout().connect(
        [this] {
          queue_draw(); // Redraw the widget
          return true;
        },
        100); // Every 100 milliseconds
  }

protected:
  bool on_draw(const Cairo::RefPtr<Cairo::Context> &cr) override {
    Gtk::Allocation allocation = get_allocation();
    const int width = allocation.get_width();
    const int height = allocation.get_height();

    // Clear the widget
    cr->set_source_rgb(0, 0, 0);
    cr->rectangle(0, 0, width, height);
    cr->fill();

    // Draw the characters
    cr->set_source_rgb(0, 1, 0);
    cr->select_font_face("Monospace", Cairo::FONT_SLANT_NORMAL,
                         Cairo::FONT_WEIGHT_BOLD);
    cr->set_font_size(20);

    for (int i = 0; i < width; i += 20) {
      for (int j = 0; j < height; j += 20) {
        cr->move_to(i, j);
        cr->show_text(std::string(1, 'A' + rand() % 26));
      }
    }

    return true;
  }
};

class MainWindow : public Gtk::Window {
public:
  MainWindow();

private:
  FallingCharsWidget fallingCharsWidget;
  std::array<Gtk::Overlay, 9> overlays; // Add this line

  std::vector<int> moves;
  void processNextMove();
  void processMove(int tile);
  std::vector<std::string> parseSolution(const std::string &solution);
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
  char randomCharacter();
};