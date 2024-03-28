#include "MainWindow.h"
#include "iostream"
#include <algorithm>
#include <ctime>
#include <gtk/gtk.h>
#include <gtkmm.h>
#include <random>
#include <thread>

extern const std::string solve(const std::array<int, 9> &board);

MainWindow::MainWindow() {
  fallingCharsWidgets.resize(9);
  initMenuBar();
  set_default_size(840, 840);
  set_title("8-Puzzle Game");
  grid.set_row_homogeneous(true);
  grid.set_column_homogeneous(true);
  initButtons();

  // Add the grid to the box, not the window
  box.pack_start(grid);
  // Add the box to the window
  add(box);
  start();
}

void MainWindow::start() {
  game.shuffle();
  updateBoard();
  show_all_children();
}

void MainWindow::initMenuBar() {
  // Create an AccelGroup
  Glib::RefPtr<Gtk::AccelGroup> accelGroup = Gtk::AccelGroup::create();

  // Add menu items directly to the menu bar
  Gtk::MenuItem *shuffleItem = Gtk::manage(new Gtk::MenuItem("Shuffle (N)"));
  shuffleItem->signal_activate().connect(
      sigc::mem_fun(*this, &MainWindow::onShuffle));
  shuffleItem->add_accelerator("activate", accelGroup, 'n', Gdk::CONTROL_MASK,
                               Gtk::ACCEL_VISIBLE);
  menuBar.append(*shuffleItem);

  Gtk::MenuItem *solveItem = Gtk::manage(new Gtk::MenuItem("Solve (S)"));
  solveItem->signal_activate().connect(
      sigc::mem_fun(*this, &MainWindow::onSolve));
  solveItem->add_accelerator("activate", accelGroup, 's', Gdk::CONTROL_MASK,
                             Gtk::ACCEL_VISIBLE);
  menuBar.append(*solveItem);

  Gtk::MenuItem *resetItem = Gtk::manage(new Gtk::MenuItem("Reset (R)"));
  resetItem->signal_activate().connect(
      sigc::mem_fun(*this, &MainWindow::onReset));
  resetItem->add_accelerator("activate", accelGroup, 'r', Gdk::CONTROL_MASK,
                             Gtk::ACCEL_VISIBLE);
  menuBar.append(*resetItem);

  Gtk::MenuItem *quitItem = Gtk::manage(new Gtk::MenuItem("Quit"));
  quitItem->signal_activate().connect(
      sigc::mem_fun(*this, &MainWindow::onQuit));
  menuBar.append(*quitItem);

  Gtk::MenuItem *solvedItem =
      Gtk::manage(new Gtk::MenuItem("Change Theme (T)"));
  solvedItem->signal_activate().connect(
      sigc::mem_fun(*this, &MainWindow::onTheme));
  solvedItem->add_accelerator("activate", accelGroup, 't', Gdk::CONTROL_MASK,
                              Gtk::ACCEL_VISIBLE);
  menuBar.append(*solvedItem);

  // Add the menu bar to the box
  box.pack_start(menuBar, Gtk::PACK_SHRINK);

  // add css class
  get_style_context()->add_class("menu-bar");

  // Add the AccelGroup to the window
  add_accel_group(accelGroup);
}void MainWindow::onTheme() {
  // change css file
  // open file dialog to choose file
  Gtk::FileChooserDialog dialog("Please choose a CSS file",
                                Gtk::FILE_CHOOSER_ACTION_OPEN);
  dialog.add_button("_Cancel", Gtk::RESPONSE_CANCEL);
  dialog.add_button("_Open", Gtk::RESPONSE_OK);

  // Add filters, so that only certain file types can be selected:
  auto filter_text = Gtk::FileFilter::create();
  filter_text->set_name("CSS files");
  filter_text->add_mime_type("text/css");
  dialog.add_filter(filter_text);

  // Show the dialog and wait for a user response:
  int result = dialog.run();

  // Handle the response:
  switch (result) {
  case (Gtk::RESPONSE_OK): {
    std::string filename = dialog.get_filename();
    auto css_provider = Gtk::CssProvider::create();
    css_provider->load_from_path(filename);
    Gtk::StyleContext::add_provider_for_screen(
        Gdk::Screen::get_default(), css_provider,
        GTK_STYLE_PROVIDER_PRIORITY_USER);

    // Create a file monitor
    auto file = Gio::File::create_for_path(filename);
    auto monitor = file->monitor_file();

    // Connect the file monitor's changed signal to a handler that reloads the CSS
    monitor->signal_changed().connect([css_provider, filename](const Glib::RefPtr<Gio::File>&, const Glib::RefPtr<Gio::File>&, Gio::FileMonitorEvent) {
        try {
            css_provider->load_from_path(filename);
        } catch (const Glib::Error& ex) {
            std::cerr << "Error reloading CSS: " << ex.what() << std::endl;
        }
    });

    break;
  }
  case (Gtk::RESPONSE_CANCEL): {
    std::cout << "Cancel clicked." << std::endl;
    break;
  }
  default: {
    std::cout << "Unexpected button clicked." << std::endl;
    break;
  }
  }
}

void MainWindow::addButton(int i) {
  buttons[i].set_size_request(100, 100);
  buttons[i].get_style_context()->add_class("tile");
  buttons[i].get_style_context()->add_class("puzzle-piece");
  buttons[i].set_label(std::to_string(game[i]));

  overlays[i].add_overlay(
      fallingCharsWidgets[i]);         // Add the matrix effect to the overlay
  overlays[i].add_overlay(buttons[i]); // Add the button to the overlay

  // attach to grid - from 2nd row
  grid.attach(overlays[i], i % 3, i / 3 + 1, 1, 1);
  buttons[i].signal_clicked().connect([this, i] {
    game.move(i);
    updateBoard();
  });

  // Add hover signals
  buttons[i].signal_enter_notify_event().connect([this](GdkEventCrossing *) {
    buttons[0].get_style_context()->add_class("hovered");
    return false;
  });

  buttons[i].signal_leave_notify_event().connect([this](GdkEventCrossing *) {
    buttons[0].get_style_context()->remove_class("hovered");
    return false;
  });
}

void MainWindow::updateBoard() {
  std::cout << "updateBoard" << std::endl;
  int blank = 0;
  for (int i = 0; i < 9; ++i) {
    if (game[i] != 0) {
      buttons[i].set_label(std::to_string(game[i]));
      buttons[i].get_style_context()->remove_class("tile-0");
      fallingCharsWidgets[i]
          .hide(); // Hide the matrix effect for non-blank tiles
    } else {
      blank = i;
    }
  }
  buttons[blank].set_label("");
  buttons[blank].get_style_context()->add_class("tile-0");
  fallingCharsWidgets[blank]
      .show(); // Show the matrix effect for the blank tile
}

char MainWindow::randomCharacter() {
  static std::mt19937 generator(
      time(0)); // Mersenne twister random number generator
  std::uniform_int_distribution<int> distribution(
      'A', 'Z'); // distribution in range ['A', 'Z']
  return static_cast<char>(distribution(generator));
}

void MainWindow::initButtons() {
  for (int i = 0; i < 9; ++i) {
    addButton(i);
  }
}

void MainWindow::onMove(int index) {
  std::cout << "moving " << index << std::endl;
  game.move(index);
  updateBoard();
}

void MainWindow::onShuffle() {
  game.shuffle();
  updateBoard();
}

// Modify the onSolve function
void MainWindow::onSolve() {
  auto solution = solve(game.getBoard());
  std::cout << "Solution: " << solution << std::endl;
  if (solution.empty()) {
    std::cerr << "No solution returned\n";
    return;
  }
  // turn of the falling chars
  for (auto &f : fallingCharsWidgets) {
    f.hide();
  }
  auto string_moves = parseSolution(solution);
  moves.clear();
  for (const std::string &m : string_moves) {
    moves.push_back(std::stoi(m));
  }
  // Start processing the moves
  processNextMove();
}

// Modify the processMove function to process the next move in the moves vector
void MainWindow::processMove(int tile) {
  auto board = game.getBoard();
  auto it = std::find(board.begin(), board.end(), tile);
  if (it != board.end()) {
    int index = std::distance(board.begin(), it);
    onMove(index);
    Glib::signal_timeout().connect_once(
        sigc::mem_fun(*this, &MainWindow::processNextMove),
        1000); // delay in milliseconds
  } else {
    std::cerr << "Tile " << tile << " not found in board\n";
  }
}

// Add a new function to process the next move
void MainWindow::processNextMove() {
  if (!moves.empty()) {
    int next_move = moves.front();
    moves.erase(moves.begin());
    processMove(next_move);
  }
}
// Helper function to parse the solution string and return a vector of moves
std::vector<std::string>
MainWindow::parseSolution(const std::string &solution) {
  std::string numbers = solution.substr(1, solution.size() - 2);
  std::vector<std::string> moves;
  std::string move;
  for (char c : numbers) {
    if (c == ',') {
      moves.push_back(move);
      move.clear();
    } else {
      move += c;
    }
  }
  moves.push_back(move);
  return moves;
}

void MainWindow::onReset() {
  game.reset();
  updateBoard();
}

void MainWindow::onQuit() { hide(); }

void MainWindow::onSolved() { isSolved = true; }

void MainWindow::onShuffled() { isShuffled = true; }
