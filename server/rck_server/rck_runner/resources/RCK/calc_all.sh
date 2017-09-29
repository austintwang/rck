#! /bin/tcsh

foreach a (`ls outputs/test*full*_5.txt | grep "[A-T]" | grep -v org | grep -v seq | grep -v single`)
#foreach a (`ls outputsFromCluster/test*full*_5.txt | grep "[A-T]" | grep -v org | grep -v seq `)
#foreach a (`ls ../../RNAcontextorg/RNAcontext/outputs/*_seq.txt | grep "[A-T]"`)
#	echo $a
	Rscript calc_cor.R $a numbers.txt | grep corr | tail -1
#	Rscript calc_cor.R $a numbers.txt | grep aupr | tail -1
end
