CXX         = g++

CFLAGS = -g  -Wall -ansi -w


SRCPATH=src
OBJPATH=obj
LIBPATH=src/lib
BINPATH=bin

all:	$(BINPATH)/rnacontext

$(BINPATH)/rnacontext: \
		$(OBJPATH)/lbfgs.o \
	 	$(OBJPATH)/ap.o \
	 	$(OBJPATH)/rnacontext.o 
	$(CXX) $(CFLAGS) \
	$(OBJPATH)/lbfgs.o  $(OBJPATH)/rnacontext.o $(OBJPATH)/ap.o \
	-o $(BINPATH)/rnacontext 

$(OBJPATH)/lbfgs.o: \
		$(SRCPATH)/lbfgsb.cpp \
		$(LIBPATH)/lbfgsb.h \
		$(LIBPATH)/ap.h
	$(CXX) $(CFLAGS) \
	-c $(SRCPATH)/lbfgsb.cpp \
	-o $(OBJPATH)/lbfgs.o

$(OBJPATH)/ap.o: \
		$(SRCPATH)/ap.cpp \
		$(LIBPATH)/ap.h \
		$(LIBPATH)/apvt.h 
	$(CXX) $(CFLAGS) \
	-c $(SRCPATH)/ap.cpp \
	-o $(OBJPATH)/ap.o

$(OBJPATH)/rnacontext.o: \
		$(SRCPATH)/rnacontext.cpp \
		$(LIBPATH)/rnacontextHeader.h \
		$(LIBPATH)/lbfgsb.h 
	$(CXX) $(CFLAGS) \
	-c $(SRCPATH)/rnacontext.cpp \
	-o $(OBJPATH)/rnacontext.o

clean:
	rm -f $(OBJPATH)/*.o
	rm $(BINPATH)/rnacontext




