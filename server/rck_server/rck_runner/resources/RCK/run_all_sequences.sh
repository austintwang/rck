#! /bin/tcsh

foreach a (`ls -l /data/cb/yaronore/sequences/GraphProt_CLIP_sequences/*sequences_A.RNAcontext* | cut -b45-`)
	echo $a
	set b=`echo $a | cut -d"." -f 1-2`.sequences_B.RNAcontext
	echo $b
	set annota=`echo $a | cut -d"." -f 1-2`.annotations_A.RNAcontext
	set annotb=`echo $b | cut -d"." -f 1-2`.annotations_B.RNAcontext
	echo $annota
	echo $annotb
	set output=`echo $a | cut -d"/" -f7`.output
	echo "./bin/rnacontext -w 4-5 -a ACGU -e EHIMP -s 3 -c $a -h $annota -d $b -n $annotb -o $output"
end
