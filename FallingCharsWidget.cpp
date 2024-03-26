#include "FallingCharsWidget.h"

FallingCharsWidget::FallingCharsWidget() {
  Glib::signal_timeout().connect(
      [this] {
        queue_draw(); // Redraw the widget
        return true;
      },
      100); // Every 100 milliseconds
}

bool FallingCharsWidget::on_draw(
    const Cairo::RefPtr<Cairo::Context> &cr)  {
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
