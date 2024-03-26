#include "MainWindow.h"
#include "iostream"
#include <algorithm> // include this at the top of your file
#include <gtk/gtk.h>
#include <gtkmm.h>
#include <thread>

extern const std::string solve(const std::array<int, 9>& board);

void MainWindow::addButton(int i) {
  buttons[i].get_style_context()->add_class("puzzle-piece");
  buttons[i].set_label(std::to_string(game[i]));
  // attach to grid - from 2nd row
  grid.attach(buttons[i], i % 3, i / 3 + 1, 1, 1);
  buttons[i].signal_clicked().connect([this, i] {
    game.move(i);
    updateBoard();
  });
}

void MainWindow::initButtons() {
  for (int i = 0; i < 9; ++i) {
    addButton(i);
  }
}

void MainWindow::onMove(int index) {
std::cout<< "moving " << index << std::endl;
  game.move(index);
  updateBoard();
  // update gui
    while (gtk_events_pending())
        gtk_main_iteration();
    // Add a delay to give the GUI time to update
    show_all_children();
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
    auto string_moves = parseSolution(solution);
    moves.clear();
    for (const std::string& m : string_moves) {
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
std::vector<std::string> MainWindow::parseSolution(const std::string& solution) {
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

void MainWindow::onQuit() {
  hide();
}

void MainWindow::onSolved() {
  isSolved = true;
}

void MainWindow::onShuffled() {
  isShuffled = true;
}

void MainWindow::initControls() {
  shuffleButton.signal_clicked().connect([this] {
    game.shuffle();
    updateBoard();
  });
solveButton.signal_clicked().connect(sigc::mem_fun(*this, &MainWindow::onSolve));
resetButton.signal_clicked().connect([this] {
    game.reset();
    updateBoard();
  });
  quitButton.signal_clicked().connect([this] {
    hide();
  });
  buttonBox.pack_start(shuffleButton, Gtk::PACK_SHRINK);
  buttonBox.pack_start(solveButton, Gtk::PACK_SHRINK);
  buttonBox.pack_start(resetButton, Gtk::PACK_SHRINK);
  buttonBox.pack_start(quitButton, Gtk::PACK_SHRINK);
  box.pack_start(buttonBox, Gtk::PACK_SHRINK);
  movesLabel.set_text("Moves: 0");
  box.pack_start(movesLabel, Gtk::PACK_SHRINK);
  // attack to grid top row
    grid.attach(box, 0, 0, 3, 1);
}


MainWindow::MainWindow() {
    set_default_size(400, 400);
    set_title("8-Puzzle Game");
    grid.set_row_homogeneous(true);
    grid.set_column_homogeneous(true);
    add(grid);
    initControls();
    initButtons();


    game.shuffle();
    updateBoard();
    show_all_children();
}

void MainWindow::updateBoard() {
std::cout<< "updateBoard" << std::endl;
    int blank = 0;
  for (int i = 0; i < 9; ++i) {
    if (game[i] != 0) {
      buttons[i].set_label(std::to_string(game[i]));
      buttons[i].get_style_context()->remove_class("tile-0");
    } else {
        blank = i;
    }
  }
  buttons[blank].set_label("");
  buttons[blank].get_style_context()->add_class("tile-0");
}
