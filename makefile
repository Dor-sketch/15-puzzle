CXXFLAGS = -Wall -Wextra -std=c++17 `pkg-config --cflags gtkmm-3.0` -O3 -march=native -flto `pkg-config --libs gtkmm-3.0`
OBJS = main.cpp

main: $(OBJS)
	$(CXX) $(CXXFLAGS) -o main $(OBJS)

clean:
	rm -f main