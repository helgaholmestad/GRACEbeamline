CC = g++
LIBS = `pkg-config --libs ibsimu-1.0.6`
LDFLAGS = -Wall -g
CXXFLAGS = -Wall -g `pkg-config --cflags --libs gtk+-3.0 ibsimu-1.0.6`

all: simu analysis

simu: simu.o
	$(CC) $(LDFLAGS) $^ $(LIBS) -o $@
analysis: analysis.o
	$(CC) $(LDFLAGS) $^ $(LIBS) -o $@

.cpp.o:
	$(CC) $(CXXFLAGS) -c $< -o $@

clean:
	$(RM) *.o simu analysis *~
