
#include "MainWindow.h"
#include <gtkmm.h>
#include <gtk/gtk.h>


int main(int argc, char *argv[]) {
    auto app = Gtk::Application::create(argc, argv, "org.gtkmm.example");

    // Load the CSS
    auto css_provider = Gtk::CssProvider::create();
    css_provider->load_from_path("style.css");
    Gtk::StyleContext::add_provider_for_screen(Gdk::Screen::get_default(), css_provider, GTK_STYLE_PROVIDER_PRIORITY_USER);

    MainWindow window;

    return app->run(window);
}