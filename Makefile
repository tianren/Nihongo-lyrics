compile_types = kanji-lyrics dual-lyrics

ifneq ($(lyricstypemake),)
lyrics = $(notdir $(wildcard ../source/*.tex))
lyricspdf = $(lyrics:%.tex=%.pdf)
target: $(lyricspdf)
$(lyricspdf): %.pdf: ../source/%.tex
	# $(if $(shell head $< | grep -i "TeX program" | grep -io "LuaLaTeX"), lualatex --file-line-error $<, xelatex -shell-escape $<)
	lualatex --file-line-error $<
	# if [ -n "$(DISPLAY)" ]; then evince $@ & fi
else
target: $(compile_types)

$(compile_types):
	export lyricstypemake=1 && make -C $@ --makefile=../Makefile
endif

debug:
	@echo $(lyrics)
	# @echo $(lyricspdf)

clean:
	find $(compile_types) \( -name *.log -o -name *.aux -o -name *.ltjruby \) -delete

.PHONY: $(compile_types) debug target clean
