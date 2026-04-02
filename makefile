all: YIT.pdf

YIT.pdf: YIT.tex fonts $(wildcard src/*.tex src/**/*.tex)
	latexmk -xelatex YIT.tex

fonts:
	$(MAKE) -C fonts

clean:
	latexmk -C

clean-fonts:
	$(MAKE) -C fonts clean

.PHONY: all fonts clean clean-fonts
