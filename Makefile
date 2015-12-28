ghc=ghc
python=python
sed=./sed.sh
hslib=mylib.hs
p1=Q1.hs
p1o=Q1
p2=Q2.py
p3=Q3.hs
p3o=Q3
MAINFONT ?=  Lucida Grande
pandoc= pandoc -s #--latex-engine=xelatex  -V mainfont="$(MAINFONT)"
readme= README.md
report= report.pdf
testi=test.txt
traini=train.txt
testo=testTable.txt
traino=trainTable.txt

all: ${p1o} ${testo} ${p3o} ${traino} $(report)


${p1o}: ${p1} ${hslib}
	${ghc} ${p1} -o ${p1o}

${p3o}: ${p3} ${hslib}
	${ghc} ${p3} -o ${p3o}

${testo}: ${testi}
	${sed} ${testi} ${testo}

${traino}: ${traini}
	${sed} ${traini} ${traino}
$(report): $(readme)
	$(pandoc) $(readme) -o $(report)

runQ1:
	./${p1o}

runQ2:
	$(python) $(p2)

clean:
	rm -rf *.o *.hi
