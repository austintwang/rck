#! /bin/tcsh

set file="/data/cb/yaronore/sequences/overlap_invivo_invitro.txt"
set lines=`wc -l $file | cut -f 1 -d" "`
set testdir="/data/cb/yaronore/sequences/GraphProt_CLIP_sequences"
set traindir="RNAcompete_derived_datasets/full"
foreach i (`seq 1 $lines`)
	foreach aaa (A B)
		set bbb="B"
		if (aaa == "B") then
			set bbb = "A"
		endif
	        set line=`cat $file | head -$i | tail -1`
	        set testseq=`echo $line | cut -f 1 -d" "`.train.sequences_$bbb.RNAcontext
		set testannot=`echo $line | cut -f 1 -d" "`.train.annotations_$bbb.RNAcontext
                set trainseq=`echo $line | cut -f 2 -d" "`$aaa.txt
                set trainannot=`echo $line | cut -f 2 -d" "`$aaa.txt.fa.combined_profile.txt
		echo $testseq
		echo $trainseq
	end
#	set dir="RNAcompete_derived_datasets/full/"
#	set invivodir="/data/cb/yaronore/sequences/GraphProt_CLIP_sequences/"
#        set fasta="/data/cb/yaronore/RNAcompete/invivo_data/$invivo"
	set output="$trainseq.$testseq"
	./bin/rnacontext -w 4-6 -a ACGU -e EHIMP -s 3 -c $traindir/$trainseq -h $traindir/$trainannot -d $testdir/$testseq -n $testdir/$testannot -o $output
end
