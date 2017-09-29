#! /bin/tcsh

set aaaa="A"
set bbbb="B"

foreach i (`echo 1 2`)
	if ($i == 1) then
		set aaa=$aaaa
		set bbb=$bbbb
	else
		set aaa=$bbbb
		set bbb=$aaaa
	endif
	foreach a (`ls ../../RNAcontext/RNAcontext/RNAcompete_derived_datasets/full/*_$aaa.txt`)
		echo $a
		set length=`echo $a | wc -c`
		echo $length
		set newlen=`echo $length-6 | bc`
		set b=`echo $a | cut -b-$newlen`$bbb.txt
		echo $b
		set output=`echo $a | cut -d"/" -f 7`
		./opt_iter.sh $a $a.fa.combined_profile.txt PHIME $output > $a.params
		set width=`cat $a.params | tail -1 | cut -f 1 -d" "`
		set iter=`cat $a.params | tail -1 | cut -f 2 -d" "`
		./bin/rnacontext -b $iter -w $width-$width -a ACGU -e PHIME -s 3 -c $a -h $a.fa.combined_profile.txt -d $b -n $b.fa.combined_profile.txt -o $output
	end
end
