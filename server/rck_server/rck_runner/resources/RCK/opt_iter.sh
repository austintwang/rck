#! /bin/tcsh

set seq=$1
set annot=$2
set alpha=$3
set output=$4

set lines=`wc -l $seq | cut -d" "  -f 1`
set alines=`wc -l $annot | cut -d" " -f 1`
echo $lines
set half=`echo "$lines / 2" | bc`
echo $half
set ratio=`echo "$alines / $lines" | bc`
echo $ratio
set ahalf=`echo "$ratio * $half" | bc`
echo $ahalf
head -$half $seq > $seq.1
set half=`echo "$half+1" | bc`
tail -n +$half $seq > $seq.2
head -$ahalf $annot > $annot.1
set ahalf=`echo "$ahalf+1" | bc`
tail -n +$ahalf $annot > $annot.2
./bin/rnacontext -b 10 -w 4-6 -a ACGU -e $alpha -s 1 -c $seq.1 -h $annot.1 -d $seq.2 -n $annot.2 -o $output > /dev/null
set max=0
set iter=0
set width=0
set step=10
foreach i (`seq 10 $step 410`)
	foreach w (`seq 4 1 6`)
#		ls -l outputs/test_${output}_$w.txt
		Rscript calc_cor.R outputs/test_${output}_$w.txt | grep correlation > /tmp/cor
		set ccc=`cat /tmp/cor | tail -1 | cut -d" " -f 4 | cut -b-10`
		set tmpccc=`echo "scale=4; 100000*$ccc" | bc | cut -d"." -f 1`
		set tmpmax=`echo "scale=4; 100000*$max" | bc | cut -d"." -f 1`
		echo "$ccc\t$i\t$w"
		echo "$max\t$iter\t$width"
		if ( $tmpccc > $tmpmax ) then
			set max = $ccc
			set width = $w
			set iter = $i
		endif
	end
	./bin/rnacontext -w 4-6 -a ACGU -e $alpha -s 1 -c $seq.1 -h $annot.1 -d $seq.2 -n $annot.2 -o $output -b $step -p aaa > /dev/null
end
echo "$width\t$iter\t$max"
#echo "width = $width"
#echo "iter = $iter"
