compile_type = kanji
# compile_type = dual
build_dir = $(compile_type)-build
output_dir = $(compile_type)-lyrics

lyrics = $(notdir $(wildcard source/*.tex))
temppdf = $(lyrics:%.tex=$(build_dir)/%.pdf)
lyricspdf = $(lyrics:%.tex=$(output_dir)/%.pdf)

# lyricspdf = $(lyrics:%.tex=%.pdf)
target: $(lyricspdf)

$(lyricspdf): $(output_dir)/%.pdf: $(build_dir)/%.pdf
	# mkdir -p $(@D)
	cp -a $< $@

$(temppdf): $(build_dir)/%.pdf: source/%.tex
	# $(if $(shell head $< | grep -i "TeX program" | grep -io "LuaLaTeX"), lualatex --file-line-error $<, xelatex -shell-escape $<)
	# mkdir -p $(@D)
	mkdir -p $(build_dir)
	cd $(build_dir) ; \
	  lualatex --file-line-error ../$< ; \
		if grep -q itemmark ../$<; then lualatex --file-line-error ../$<; fi;

	# mv $(@:) $@
	# if [ -n "$(DISPLAY)" ]; then evince $@ & fi
	# if grep -q itemmark $<; then lualatex --file-line-error $<; fi


debug:
	@echo $(lyrics)
	@echo $(lyricspdf)
	@echo $(build_dir)

clean:
	find $(build_dir) \( -name *.log -o -name *.aux -o -name *.ltjruby \) -delete

.PHONY: debug target clean
