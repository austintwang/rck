#! /bin/tcsh

set file="/data/cb/yaronore/sequences/overlap_GraphProt_RNAcompete.txt"
set lines=`wc -l $file | cut -f 1 -d" "`
set testdir="/data/cb/yaronore/sequences/GraphProt_CLIP_sequences"
set traindir="../../RNAcompete/for_RNAcontext/"
foreach i (`seq 1 $lines`)
	foreach aaa (A B)
		set bbb="B"
		if (aaa == "B") then
			set bbb = "A"
		endif
	        set line=`cat $file | head -$i | tail -1`
	        set testseq=`echo $line | cut -f 3 -d" "`.train.sequences_$aaa.RNAcontext
		set testannot=`echo $line | cut -f 3 -d" "`.train.annotations_$aaa.RNAcontext
                set trainseq=`echo $line | cut -f 1 -d" "`.txt.sequences_$aaa.RNAcontext
                set trainannot=`echo $line | cut -f 1 -d" "`.txt.annotations_$aaa.RNAcontext
		echo $testseq
		echo $trainseq
	end
#	set dir="RNAcompete_derived_datasets/full/"
#	set invivodir="/data/cb/yaronore/sequences/GraphProt_CLIP_sequences/"
#        set fasta="/data/cb/yaronore/RNAcompete/invivo_data/$invivo"
	set output="$trainseq.$testseq"
	echo "./bin/rnacontext -w 4-6 -a ACGU -e PHIME -s 3 -c $traindir/$trainseq -h $traindir/$trainannot -d $testdir/$testseq -n $testdir/$testannot -o $output"
end
