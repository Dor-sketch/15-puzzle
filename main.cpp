#include "MainWindow.h"
#include <gtk/gtk.h>
#include <gtkmm.h>
#include <iostream>

int SIZE = 9;

int main(int argc, char *argv[]) {
  int newSizeArgIndex = 0;

  // Find the -s argument and get the size
  for (int i = 1; i < argc; ++i) {
    std::string arg = argv[i];
    if (arg == "-s" && i + 1 < argc) {
      SIZE = std::stoi(argv[++i]);
      newSizeArgIndex = i;
      break;
    }
  }

  // Create a new argv array with only the arguments after the size
  int newArgc = argc - newSizeArgIndex - 1;
  char** newArgv = new char*[newArgc + 1]; // +1 for the program name

  newArgv[0] = argv[0]; // the program name
  for (int i = 1; i <= newArgc; ++i) {
    newArgv[i] = argv[i + newSizeArgIndex];
  }

  auto app = Gtk::Application::create(newArgc, newArgv, "org.gtkmm.example");

  // Don't forget to delete the newArgv array when you're done with it
  delete[] newArgv;

  std::cout << "SIZE: " << SIZE << std::endl;
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
  std::cout << "SIZE: " << SIZE << std::endl;
  Gtk::StyleContext::add_provider_for_screen(Gdk::Screen::get_default(),
                                             css_provider,
                                             GTK_STYLE_PROVIDER_PRIORITY_USER);

  MainWindow window;
  std::cout << "SIZE: " << SIZE << std::endl;

  return app->run(window);
}
