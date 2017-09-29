#! /bin/tcsh

set file="/data/cb/yaronore/GraphProt/GraphProt-1.0.1/RNAcompete_derived_datasets/full/list_gp.txt"
set lines=`wc -l $file | cut -f 1 -d" "`
foreach i (`seq 1 $lines`)
        set line=`cat $file | head -$i | tail -1`
        set pos=`echo $line | cut -f 2 -d" "`.train.positives.fa
	set neg=`echo $line | cut -f 2 -d" "`.train.negatives.fa
        echo $pos
        echo $neg
#	set dir="RNAcompete_derived_datasets/full/"
	set invivodir="/data/cb/yaronore/sequences/GraphProt_CLIP_sequences/"
#        set fasta="/data/cb/yaronore/RNAcompete/invivo_data/$invivo"
#	set output="$invivo"
	echo "./bin/rnacontext -w 4-6 -a ACGU -e EHIMP -s 3 -c $invivodir/$pos -h $invivodir/$pos.combined_profile.txt -d $invivodir/$invivo -n $invivodir/$invivo.fa.combined_profile.txt -o $invivo"
end
