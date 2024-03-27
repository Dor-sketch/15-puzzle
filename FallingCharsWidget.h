#pragma once

#include <gtk/gtk.h>
#include <gtkmm.h>

class FallingCharsWidget : public Gtk::DrawingArea {
public:
  FallingCharsWidget();

protected:
  bool on_draw(const Cairo::RefPtr<Cairo::Context> &cr) override;
};