PREFIX ?= /usr/local

VERSION := 1.0.0
DIST := image-factory image-factory.1.md image-factory.conf image_factory.py \
	image-factory-sudo-helper image-factory-sudo-helper.1.md LICENSE Makefile NEWS README.md \
	tests/__init__.py tests/pylint.conf tests/test_cli.py tests/test_flake8.py \
	tests/test_helper.py tests/test_pylint.py tests/test_sudo_helper.py \
	$(wildcard data/*.cfg) $(wildcard data/*.xml)

all: doc

check:
	python3 -m unittest discover -v

clean:
	rm -f *.1

dist: image-factory-$(VERSION).tar.xz image-factory-$(VERSION).tar.xz.asc

version:
	@echo $(VERSION)

%.asc: %
	gpg --armor --batch --detach-sign --yes --output $@ $^

%.tar.xz: $(DIST)
	tar -c --exclude-vcs --transform="s@^@$*/@S" $^ | xz -cz9 > $@

doc: image-factory.1 image-factory-sudo-helper.1

%.1: %.1.md
	pandoc -s -t man $^ -o $@

install:
	install -D -m 755 image-factory $(DESTDIR)$(PREFIX)/bin/image-factory
	install -D -m 755 image-factory-sudo-helper $(DESTDIR)$(PREFIX)/bin/image-factory-sudo-helper
	install -D -m 644 image-factory.1 $(DESTDIR)$(PREFIX)/share/man/man1/image-factory.1
	install -D -m 644 image-factory-sudo-helper.1 $(DESTDIR)$(PREFIX)/share/man/man1/image-factory-sudo-helper.1
	install -d $(DESTDIR)$(PREFIX)/share/image-factory
	install -m 644 $(wildcard data/*) $(DESTDIR)$(PREFIX)/share/image-factory
	install -D -m 644 image-factory.conf $(DESTDIR)$(PREFIX)/share/doc/image-factory/image-factory.conf

.PHONY: all check clean doc install version
