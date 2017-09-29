options(echo=TRUE)
args <- commandArgs(trailingOnly=TRUE)
print(args)

a<-read.table(args[1])
res = cor(a[,1],a[,2])
#res = (a[,1]-a[,2])^2
#res = cor.test(a[,1],a[,2], method="spearman")$estimate
paste("correlation", args[1], res, sep=" ")

b<-read.table(args[2])
protein<-strsplit(args[1],"_")[[1]][2]
c<-b[match(protein,t(b[1])),]

pos=as.numeric(c[6]+c[7])
neg=as.numeric(c[8]+c[9])
len=dim(a)[1]
pos
neg
len
a<-a[order(a[,1]),]
a<-a[c(1:pos,(len-neg):len),]
a<-data.frame(a,1:dim(a)[1])
cor(a[,1],a[,2])

a<-a[order(a[,2]),]
tmppos = 0
tmpneg = 0
area = 0
j = 0
n = 100
for (i in 1:dim(a)[1]) {
	if (tmppos / pos >= (1/n * j)) {
		j = j+1
		area = area + tmppos / i
	}
	if (a[i,3]<=pos)
		tmppos = tmppos +1
	else
		tmpneg + tmpneg + 1
}
paste("aupr", args[1], (area+1) / n, sep=" ")

