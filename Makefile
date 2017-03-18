texfiles = $(wildcard *.tex)
lyrics = $(shell ls *.tex | grep -v ' ' | grep -iv  'macros')
lyricspdf = $(lyrics:%.tex=%.pdf)

target: $(lyricspdf) $(lyricspdf-lua)

$(lyricspdf): %.pdf: %.tex
	$(if $(shell head $< | grep -i "TeX program" | grep -io "LuaLaTeX"), lualatex --file-line-error $<, xelatex -shell-escape $<)
	if [ -n "$(DISPLAY)" ]; then evince $@ & fi

# $(lyricspdf-lua): %.pdf: %.tex
# 	lualatex --file-line-error $<
# 	evince $@ &

debug:
	echo $(sort $(lyrics))
