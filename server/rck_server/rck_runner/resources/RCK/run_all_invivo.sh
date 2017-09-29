#! /bin/tcsh

set aaa="A"
set bbb="B"

set file="/data/cb/yaronore/GraphProt/GraphProt-1.0.1/RNAcompete_derived_datasets/full/list.txt"
set lines=`wc -l $file | cut -f 1 -d" "`
foreach i (`seq 1 $lines`)
        set line=`cat $file | head -$i | tail -1`
        set cmpt=`echo $line | cut -f 1 -d" "`_data_full_$aaa.txt
        set invivo=`echo $line | cut -f 2 -d" "`
        echo $cmpt
        echo $invivo
	set dir="RNAcompete_derived_datasets/full/"
	set invivodir="../../RNAcompete/invivo_data/"
        set fasta="/data/cb/yaronore/RNAcompete/invivo_data/$invivo"
	set output="$invivo"
	echo "./bin/rnacontext -w 4-6 -a ACGU -e EHIMP -s 3 -c $dir/$cmpt -h $dir/$cmpt.fa.combined_profile.txt -d $invivodir/$invivo -n $invivodir/$invivo.fa.combined_profile.txt -o $invivo"
end
