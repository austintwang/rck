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
	foreach a (`ls ../../RNAcompete/data/*sequences_$aaa.RNAcontext`)
		echo $a
		set length=`echo $a | wc -c`
		echo $length
		set newlen=`echo $length-6 | bc`
		set b=`echo $a | cut -d"." -f 1-5`.sequences_$bbb.RNAcontext
		echo $b
		set output=`echo $a | cut -d"/" -f 5`
		set annot=`echo $a | cut -d"." -f 1-5`
		echo "./bin/rnacontext -w 4-5 -a ACGU -e EHIMP -s 3 -c $a -h $annot.annotations_${aaa}.RNAcontext -d $b -n $annot.annotations_${bbb}.RNAcontext -o $output"
	end
end
