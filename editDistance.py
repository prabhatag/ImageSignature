import os

def getIndex(arr_score,val):
	for i in arr_score:
		if i[1] == val:
			return i[0]

def getImgName(index):
	#print(index)
	img_names = os.listdir()
	return img_names[index]

def getAllSignatures(fileName):
	signatureFile = open(fileName,"r")
	sig = []
	for line in signatureFile.readlines():
		sig.append(list(map(float,line[1:-2].split(","))))
	return sig

def distanceMatrix(sig):
	all_sig_dist = []
	for i in range(len(sig)):
		dist = []
		for j in range(len(sig)):
			score = 0
			if not i==j:
				for k in range(len(sig[0])):
					score+=(sig[i][k]-sig[j][k])**2
				dist.append((j,score**0.5))
		all_sig_dist.append(dist)

	return all_sig_dist

def getMinMaxSimilarity(sig):
	min_max_sim = []
	all_sig_dist = distanceMatrix(sig)
	for i in range(len(all_sig_dist)):
		maxIndex = getIndex(all_sig_dist[i],max(x[1] for x in all_sig_dist[i]))
		minIndex = getIndex(all_sig_dist[i],min(x[1] for x in all_sig_dist[i]))
		print("maxindex",maxIndex)
		print("minindex",minIndex)
		min_max_sim.append((getImgName(i),getImgName(minIndex),min(x[1] for x in all_sig_dist[i]),getImgName(maxIndex),max(x[1] for x in all_sig_dist[i])))
	return min_max_sim

sig_arr = getAllSignatures("signatures.txt")
similarityScore = getMinMaxSimilarity(sig_arr)
print("Image\tMostSimilar\tMinDistance\tLeastSimilar\tMaxDist")
for i in similarityScore:
	print(i[0],i[1],i[2],i[3],i[4],sep="\t")

# all_sig_dist = []
# min_max_sim = []
# for i in range(len(sig)):
# 	dist = []
# 	for j in range(len(sig)):
# 		score = 0
# 		if not i==j:
# 			for k in range(len(sig[0])):
# 				score+=(sig[i][k]-sig[j][k])**2
# 			dist.append((j,score**0.5))
# 	all_sig_dist.append(dist)
# 	maxIndex = getIndex(dist,max(x[1] for x in dist))
# 	minIndex = getIndex(dist,min(x[1] for x in dist))
	
# 	min_max_sim.append((getImgName(i),getImgName(minIndex),min(x[1] for x in dist),getImgName(maxIndex),max(x[1] for x in dist)))

# print("Image\tMostSimilar\tLeastSimilar")
# for i in min_max_sim:
# 	print(i[0],i[1],i[2],i[3],i[4],sep="\t")