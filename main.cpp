#include <algorithm>
#include <array>
#include <gtk/gtk.h>
#include <gtkmm.h>
#include <random>

class Game {
public:
    Game() {
        std::iota(board.begin(), board.end(), 0);
    }

    void shuffle() {
        std::shuffle(board.begin(), board.end(), std::mt19937{std::random_device{}()});
    }

    bool isSolved() const {
        return std::is_sorted(board.begin(), board.end());
    }

    int operator[](int index) const {
        return board[index];
    }

    void move(int index) {
        if (index % 3 > 0 && board[index - 1] == 0) {
            std::swap(board[index], board[index - 1]);
        } else if (index % 3 < 2 && board[index + 1] == 0) {
            std::swap(board[index], board[index + 1]);
        } else if (index / 3 > 0 && board[index - 3] == 0) {
            std::swap(board[index], board[index - 3]);
        } else if (index / 3 < 2 && board[index + 3] == 0) {
            std::swap(board[index], board[index + 3]);
        }
    }

private:
    std::array<int, 9> board;
};

class MainWindow : public Gtk::Window {
public:
    MainWindow() {
        set_default_size(200, 200);
        set_title("8-Puzzle Game");

        grid.set_row_homogeneous(true);
        grid.set_column_homogeneous(true);
        add(grid);

        for (int i = 0; i < 9; ++i) {

            buttons[i].get_style_context()->add_class("puzzle-piece");
            buttons[i].set_label(std::to_string(game[i]));
            grid.attach(buttons[i], i % 3, i / 3, 1, 1);
            buttons[i].signal_clicked().connect([this, i] {
                game.move(i);
                updateBoard();
            });
        }



        game.shuffle();
        updateBoard();

        show_all_children();
    }

  private:
    void updateBoard() {
      for (int i = 0; i < 9; ++i) {
        if (game[i] != 0) {
          buttons[i].set_label(std::to_string(game[i]));
            buttons[i].get_style_context()->remove_class("tile-0");
        } else {
          buttons[i].set_label("");
          buttons[i].get_style_context()->add_class("tile-0");
        }
      }
    }

    Game game;
    Gtk::Grid grid;
    std::array<Gtk::Button, 9> buttons;
};

int main(int argc, char *argv[]) {
    auto app = Gtk::Application::create(argc, argv, "org.gtkmm.example");

    // Load the CSS
    auto css_provider = Gtk::CssProvider::create();
    css_provider->load_from_path("style.css");
    Gtk::StyleContext::add_provider_for_screen(Gdk::Screen::get_default(), css_provider, GTK_STYLE_PROVIDER_PRIORITY_USER);

    MainWindow window;

    return app->run(window);
}