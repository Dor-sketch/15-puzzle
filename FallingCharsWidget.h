#pragma once

# include <gtkmm.h>
# include <random>
# include <ctime>
#include <gtk/gtk.h>


class FallingCharsWidget : public Gtk::DrawingArea {
public:
  FallingCharsWidget();

protected:
  bool on_draw(const Cairo::RefPtr<Cairo::Context> &cr) override;
};