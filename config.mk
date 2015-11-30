# Mode
# (None)

# Binary
bindir=bin/
EXEC=server
CC=gcc
archive=TiWim_$(EXEC)
DOXYGEN=/usr/bin/doxygen
MAKE=/usr/bin/make
PYTHON=/usr/bin/python2.7
PYTHON_CONFIG=/usr/bin/python-config
CFLAGS=-g -Wall -fPIC -O2 -fstrict-aliasing -I. -Wp,-D_FORTIFY_SOURCE=2
CFLAGS+=-Werror
THREAD_LIBS=-lpthread
COVERAGE=$(EXEC)_cover
TESTS=$(EXEC)_test
PACKAGE_VERSION=1.0.0
PDF_READER=zathura
