#! /bin/tcsh

set prefix="100"
#set prefix="sho"
foreach a (`ls -l *.$prefix | cut -b47-`)
	echo $a
	set id=`echo $a | cut -d"." -f 1`
	rm $a.fa
	foreach b (`ls -l /scratch/yaronore/hg19/chr*fa | cut -b55- | grep -v "_"`)
		echo $b
		~/AFS/bedtools/bedtools2/bin/bedtools getfasta -s -fi $b -bed $a -fo /tmp/getfasta_output.fa >& /dev/null
		cat /tmp/getfasta_output.fa >> $a.fa
	end
end
