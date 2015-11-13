ghc=ghc
sed=./sed.sh
p1=main.hs
p1o=main
testi=test.txt
traini=train.txt
testo=testTable.txt
traino=trainTable.txt
run=./run.sh

all: ${p1o} ${testo} ${traino}


${p1o}: ${p1}
	${ghc} ${p1}

${testo}: ${testi}
	${sed} ${testi} ${testo}

${traino}: ${traini}
	${sed} ${traini} ${traino}

run: ${run}
	${run}
