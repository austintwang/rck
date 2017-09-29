#! /bin/tcsh

foreach a (`ls -l /data/cb/yaronore/sequences/GraphProt_CLIP_sequences/*sequences*RNAcontext | cut -b45-`)
	set trainseq=$a
	set label=`echo $a | cut -d"." -f 3 | cut -d"_" -f 2 | cut -d"." -f 1`
	set bbb="B"
	if ($label == "B") then
		set bbb = "A"
	endif
	set testseq=`echo $a | cut -d"." -f 1-2`.sequences_$bbb.RNAcontext
	echo $trainseq
	echo $testseq
	set trainannot=`echo $a | cut -d"." -f 1-2`.annotations_$label.RNAcontext
	set testannot=`echo $a | cut -d"." -f 1-2`.annotations_$bbb.RNAcontext
	set output=`echo $a | cut -d"/" -f 7`
	./bin/rnacontext -w 4-5 -a ACGU -e PLMUE -s 3 -c $trainseq  -h $trainannot -d $testseq -n $testannot -o $output
end
