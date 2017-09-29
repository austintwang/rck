options(echo=TRUE)
args <- commandArgs(trailingOnly=TRUE)
print(args)

a<-read.table(args[1])
res = cor(a[,1],a[,2])
#res = (a[,1]-a[,2])^2
#res = cor.test(a[,1],a[,2], method="spearman")$estimate
paste("correlation", args[1], res, sep=" ")

a<-a[order(a[,2]),]
tmppos = 0
tmpneg = 0
area = 0
j = 0
n = 100
pos = length(a[,1][a[,1]==1])
neg = length(a[,1][a[,1]==-1])
n = (pos + neg)/2
for (i in 1:dim(a)[1]) {
	if (tmpneg / neg >= (1/n * j)) {
		j = j+1
		area = area + tmppos / pos
	}
	if (a[i,1]==1)
		tmppos = tmppos + 1
	else
		tmpneg = tmpneg + 1
}
paste("aupr", args[1], 1 - (area) / n, sep=" ")

