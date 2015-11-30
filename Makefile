
ifneq ($(MAKECMDGOALS), clean)
ifneq ($(MAKECMDGOALS), distclean)
include config.mk
endif
endif


.PHONY : all check run clean distclean


#HEAD = $(SRC:.$(EXT)=.h)
OBJ = $(subst .cc, .o, $(SRC)) # prend tous les fichiers en .c et établit une liste de o

# $* recupere la valeur de % dans la cible.
SRC = $(wildcard $(srcdir)*.cc)

default: all test

################################################################################
# top level compilation rules
################################################################################

all: src/*.o
	@echo "linking"
	@$(CC) $(CFLAGS) -o $(bindir)$(EXEC) $^

install:: all

uninstall: distclean

distclean:: clean
	@rm -vf bin/*

create:
	@mkdir bin test src doc


clean::
	@rm -vf *.o
	@rm -vf */*.o
	@rm -vf *~
	@rm -vf */*~
	@rm -vf .*.swp
	@rm -vf */.*.swp
	@rm -vf .*.swo
	@rm -vf */.*.swo

re:: clean install

################################################################################
# Suffixes compilation rules
################################################################################

.SUFFIXES: .cc .c .o .po .h

.c.o:
	@echo "Compiling $< C file"
	@$(CC) $(CFLAGS) -c $< -o $@

.cc.o:
	@echo "Compiling $<, C++ file"
	@$(CXX) $(CFLAGS) -c $< -o $@

.cc.po:
	@echo "Compiling $< C++ file test"
	@$(CXX) $(CFLAGS) -c $< -o $@


################################################################################


archive:
	-@rm $(archive).tar
	@echo "\033[31m"removing old file "\033[0m"
	@tar -cvf $(archive).tar src* test* doc* bin* README.pdf Makefile
	@echo "\033[31m"archive done"\033[0m"

readme:
	@echo "\033[31m"Editing README"\033[0m"
	@vim doc/readme.md
	@echo "\033[31m"Generating html and pdf file"\033[0m"
	@pandoc doc/readme.md -o doc/README.html
	@pandoc -V geometry:margin=2cm doc/readme.md -o README.pdf
	@$(PDF_READER) README.pdf&

# @for i in $(srcdir); do (cd $$i; $(MAKE) all); done
#	@$(MAKE) $(EXEC)

$(EXEC): $(OBJ)
	$(CC) -o $(bindir)$@ $(CFLAGS) $?

run: $(bindir)$(EXEC)
	$(bindir)$(EXEC) bin/test

test: $(bindir)$(EXEC) test/hello.o
	@rm test/hello.o
# -$(bindir)$(EXEC)
	-@$(bindir)$(EXEC) test/hello.c
# -$(bindir)$(EXEC) /etc/shadow

#flex: src/specif.l specif.tab.c
#	vim src/specif.l
#	flex -o bin/lex.yy.c src/specif.l
#	gcc bin/lex.yy.c -ll specif.tab.c -ly -o bin/lexical
#	bin/lexical < test/hello.c
#
#bison: src/specif.y
#	vim src/specif.y
#	bison -d src/specif.y
#
#specif.tab.c: bison
#
#install: $(bindir)$(EXEC)
#	@echo "todo"
