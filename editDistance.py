import os

def getIndex(arr_score,val):
	for i in arr_score:
		if i[1] == val:
			return i[0]

def getImgName(index):
	img_names = os.listdir()
	return img_names[index][:]


signatureFile = open("signatures.txt","r")
sig = []
for line in signatureFile.readlines():
	sig.append(list(map(float,line[1:-2].split(","))))

#print(sig[0])


dist = []

for i in range(len(sig)-1):
	score = 0
	for j in range(len(sig[i+1])):
		score += (sig[0][j]-sig[i+1][j])**2

	dist.append(score)

# print(dist)
# print("Max-dist",dist.index(max(dist)), max(dist))
# print("Min-dist",dist.index(min(dist)), min(dist))

all_sig_dist = []
min_max_sim = []
for i in range(len(sig)):
	dist = []
	for j in range(len(sig)):
		score = 0
		if not i==j:
			for k in range(len(sig[0])):
				score+=(sig[i][k]-sig[j][k])**2
			dist.append((j,score**0.5))
	all_sig_dist.append(dist)
	#print(dist)
	#print(dist)
	maxIndex = getIndex(dist,max(x[1] for x in dist))
	minIndex = getIndex(dist,min(x[1] for x in dist))
	
	# print(i," : Max-dist",getIndex(dist,max(x[1] for x in dist)),max(x[1] for x in dist))
	# print(i," : Min-dist",getIndex(dist,min(x[1] for x in dist)),min(x[1] for x in dist))
	
	min_max_sim.append((getImgName(i),getImgName(minIndex),getImgName(maxIndex)))
# print(all_sig_dist)

# print(min_max_sim)

print("Image\tMostSimilar\tLeastSimilar")
for i in min_max_sim:
	print(i[0],i[1],i[2],sep="\t")

# for i in sig[0]:
# 	print(i)