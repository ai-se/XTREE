Src=Manuscript
filename=Manuscript
response=response

all : dirs tex bib  tex tex embedfonts done

dirs :
	@- [ ! -d pdf ] && mkdir pdf

publish : dirs all
	cp $(HOME)/tmp/$(Src).pdf pdf/$(Name).pdf
	chmod a+r pdf/$(Name).pdf
	cp pdf/$(Name).pdf  $(HOME)/gits/timm/timm.github.io/pdf
	cd  $(HOME)/gits/timm/timm.github.io/pdf; git add * ; cd ..; make typo

one : dirs tex done

done :
	@printf "\n\n\n==============================================\n"
	@printf       "see output in $(Src).pdf\n"
	@printf       "==============================================\n\n\n"
	@printf "\n\nWarnings (may be none):\n\n"
	grep arning ${Src}.log


tex : dirs
	- pdflatex --shell-escape  $(Src)

embedfonts:
	@ gs -q -dNOPAUSE -dBATCH -dPDFSETTINGS=/prepress -sDEVICE=pdfwrite \
          -sOutputFile=$(Src)-embedded.pdf $(Src).pdf
	@ mv             $(Src)-embedded.pdf $(Src).pdf

bib :
	- bibtex $(Src)



read:
	evince ${filename}.pdf &

aread:
	acroread ${filename}.pdf

open:
	open ${filename}.pdf

git: ready clean
	@- git add --all .
	@- git commit -m "Makefile Commit"
	@- git push origin master

typo:   ready
	@- git status
	@- git commit -am "saving"
	@- git push origin master # <== update as needed

ready: rahlk
	@- git config --global credential.helper cache
	@- git config credential.helper 'cache --timeout=3600'

rahlk:  # <== change to your name
	@- git config --global user.name "rahlk"
	@- git config --global user.email i.m.ralk@gmail.com


clean_all:
	rm -f *.ps *.pdf *.log  *.aux  *.out  *.dvi  *.bbl  *.blg  *.thm   *.spl   *.synctex.gz .DS_Store

clean:
	rm -f *.ps *-eps-converted-to.pdf *.log *.aux *.out *.dvi *.blg *.thm *.spl *.synctex.gz .DS_Store
