from __future__ import division
import sys

MRR = 0
MAP = 0
num = 0
bugid = ''
avgP = 0
top1 = 0
top5 = 0
top10 = 0
top20 = 0
ranking = 0
top = {}
total = 0

for it in range(0,200):
	top[str(it)] = 0

for line in open(sys.argv[1]):
	rank = line.split(',')[2]
	score = line.split(',')[3]
	MRR = MRR + 1 / (int(rank) + 1)
	if bugid != line.split(',')[0]:
		if num:
			MAP = MAP + avgP / num
		bugid = line.split(',')[0]
		total = total + 1
		num = 1
		avgP = num / (int(rank) + 1)
		if int(rank) == 0:
			top1 = top1 + 1
		if int(rank) < 5:
			top5 = top5 + 1
		if int(rank) < 10:
			top10 = top10 + 1
		if int(rank) < 20:
			top20 = top20 + 1
		if int(rank) < 200:
			for it in range(int(rank),200):
				top[str(it)] = top[str(it)] + 1
	else:
		num = num + 1
		avgP = avgP + num / (int(rank) + 1)
	ranking = ranking + int(rank)
#print ranking
#print top1
#print top5
#print top10
#print top20
#print total
#print MRR
#print MAP

print "\n"
for it in range(0,20):
#	print str(top[str(it)])
	print str(top[str(it)]/total)