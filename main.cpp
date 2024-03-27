#include "MainWindow.h"
#include <gtk/gtk.h>
#include <gtkmm.h>
#include <iostream>

int main(int argc, char *argv[]) {
  auto app = Gtk::Application::create(argc, argv, "org.gtkmm.example");

  // Load the CSS
  auto css_provider = Gtk::CssProvider::create();
  try {
    css_provider->load_from_path("style.css");
  } catch (const Glib::FileError &ex) {
    std::cerr << "FileError: " << ex.what() << std::endl;
    return 1;
  } catch (const Gtk::CssProviderError &ex) {
    std::cerr << "CssProviderError: " << ex.what() << std::endl;
    return 1;
  }
  Gtk::StyleContext::add_provider_for_screen(Gdk::Screen::get_default(),
                                             css_provider,
                                             GTK_STYLE_PROVIDER_PRIORITY_USER);

  MainWindow window;

  return app->run(window);
}
