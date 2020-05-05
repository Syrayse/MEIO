import numpy as np 

"""
Calculates the values of (i,j), without overflow.
Returns (X,Y). Where X represents the probability
of (i,j). Y represents resulting un-weighted profit.
"""
def prob(i, j, C, requests, deliveries):
	X = 0
	Y = 0

	for p in range( max(0, i-j), i ):
		prob = requests[p] * deliveries[p - (i - j)]
		X += prob
		Y += prob * p

	for p in range( i, C + 1 ):
		prob = requests[p] * deliveries[j]
		X += prob
		Y += prob * i

	return (X,Y*30)

"""
Calculates the vales of (i,j), considering overflow.
Returns (X,Y). Where X represents the probability
of (i,j). Y represents resulting un-weighted profit.
"""
def phi(i, C, requests, deliveries):
	X = 0
	Y = 0

	for k in range(0, i):
		for w in range(1, i - k + 1):
			prob = requests[k] * deliveries[C - i + w + k]
			X += prob
			Y += prob * k

	return (X,Y*30)

"""
Builds both the transation matrix and contribution
matrix.
Returns (tMat,cMat). Where tMat represente the transition
matrix and cMat represents the contribution matrix.

nTrans indicates the number of transfered vehicles to that
branch. If nTrans > 0, then the branch is the reciever of
vehicles. If nTrans = 0, the branch does not provide nor
recieve any vehicles. If nTrans < 0, then the branch is
the sender of the vehicles.
"""
def buildMatrixes(C, nTrans, requests, deliveries):
	X = np.zeros((C+1,C+1))
	Y = np.zeros((C+1,C+1))

	for i in range(0, C + 1):

		for j in range( max(0,nTrans), min(C, C + nTrans) + 1):
			(a,b) = prob(i, j - nTrans, C, requests, deliveries)
			X[i,j] += a
			Y[i,j] += b

		# Added the excess for reciever
		for j in range(C - nTrans + 1, C + 1):
			(a,b) = prob(i, j, C, requests, deliveries)
			X[i,C] += a
			Y[i,C] += b

		if nTrans >= 0:
			(a,b) = phi(i, C, requests, deliveries)
			X[i,C] += a
			Y[i,C] += b
		else:
			(a,b) = phi(i, C, requests, deliveries)
			X[i,C+nTrans] += a
			Y[i,C+nTrans] += b
			for j in range(0, abs(nTrans)):
				(a,b) = prob(i, j, C, requests, deliveries)
				X[i,j] += a
				Y[i,j] += b

	for i in range(0, C + 1):
		for j in range(0, C + 1):
			if X[i,j] == 0:
				Y[i,j] = 0
			else:
				Y[i,j] = Y[i,j] / X[i,j]
	
	# Include the cost for extra space if j > 8	
	extra = np.zeros( (C+1, C+1) )

	for i in range(0, C + 1):
		for j in range(9, C + 1):
			extra[i,j] = -10

	Y = np.add(Y,extra)

	# Price per transfer
	if nTrans < 0:
		Y = np.add(Y, 7 * nTrans)

	
	return (X,Y)

"""
Binds separate transition and contributions matrixes,
of both matrixes together, aggregating them together.
Returns (X,Y). Where X is the binding of the transitions
and Y is the binding of the contributions.
"""
def bindMatrixes(C, (a1,b1), (a2,b2)):
	k = C + 1
	N = k * k
	X = np.zeros( (N, N) )
	Y = np.zeros( (N, N) )

	for i in range(0, N):
		
		i0 = i // k
		i1 = i % k

		for j in range(0, N):
			
			f0 = j // k
			f1 = j % k

			X[i,j] = a1[i0,f0] * a2[i1,f1]
			Y[i,j] = b1[i0,f0] + b2[i1,f1]

	return (X,Y)

# Generates all possibilites
def entryProblem(requests, deliveries):
	tMats = []
	cMats = []
	dict = {}
	k = 1

	F1 = buildMatrixes(12,0,requests[0],deliveries[0])
	F2 = buildMatrixes(12,0,requests[1],deliveries[1])
	(a,b) = bindMatrixes(12, F1, F2)
	tMats.append(a)
	cMats.append(b)
	dict[0] = '(0,0)'

	for i in range(-3, 4):
		if i != 0:
			F1 = buildMatrixes(12,i,requests[0],deliveries[0])
			F2 = (a1,b1) = buildMatrixes(12,-i,requests[1],deliveries[1])
			(a,b) = bindMatrixes(12, F1, F2)
			tMats.append(a)
			cMats.append(b)
			dict[k] = '(' + str(i) + "," + str(-i) + ')'
			k = k + 1

	return (tMats, cMats, dict)

# Estimates, for each decision, the expected contribution.
def estContributions(k, w, tMat, cMat):
	return [np.array(np.sum(np.multiply(tMat[i],cMat[i]), axis=1)).reshape((w,1)) for i in range(k)]

# Estimates, for each decisions, the total expected contribution.
def estTotalContribs(k, cts, tMat, optPolicy):
	return [np.add(cts[i], np.matmul(tMat[i],optPolicy)) for i in range(k)]

# Applies the value iteration algorithm.
def valueIteration(nDecisions, nStates, transMat, contribMat, iterMax = 20):
	n = 0
	# Define def. margin.
	epsilon = 0.0001

	# Establish F0.
	Fn = F = np.zeros((nStates,1))

	# Decision taken in each state.
	calls = np.zeros(nStates)

	# Establish expected contribution for each decision.
	contribs = estContributions(nDecisions, nStates, transMat, contribMat)

	while n < iterMax:

		# Calculates total expected contribution.
		Vn = estTotalContribs(nDecisions, contribs, transMat, Fn)

		# Intermediate matrix for different decisions.
		tmp = np.concatenate(Vn, axis=1)

		# Specify the chosen policies.
		calls = np.argmax(tmp, axis=1)

		Fn = np.array(np.max(tmp, axis=1)).reshape((nStates,1))
		Dn = Fn.T - F.T
		F = Fn

		# Leave if Verication Condition checks out.
		if np.max(Dn) - np.min(Dn) < epsilon:
			break

		n = n + 1

	return calls

"""
# UNCOMMENT FOR VALUE ITERATION TEST
t = []
t.append(np.array([[0.75,0.25],[0.3333,0.6667]]))
t.append(np.array([[0.75,0.25],[0.3333,0.6667]]))

c = []
c.append(np.array([[8,4],[6,-7.5]]))
c.append(np.array([[-10,6],[3,12]]))

print(valueIteration(2,2,t,c))
"""

# Dados Relativos a filial 1.
requests1 =  [0.0356,0.0904,0.1380,0.1400,0.1224,0.1292,0.0952,0.0820,0.0560,0.0496,0.0324,0.0216, 0.0076]
deliveries1 = [0.0448,0.1632,0.2220,0.2092,0.1620,0.1056,0.0556,0.0236,0.0100,0.0036,0.0000,0.0000,0.0004]

#requests1 = [ 0.114 , 0.2652, 0.2784, 0.1916, 0.0956, 0.0404, 0.0116, 0.0028, 0.0   , 0.0   , 0.0   , 0.0004, 0.0] 
#deliveries1 = [  0.0184,  0.0872,  0.1416,  0.198,  0.2016,  0.1592,  0.1,  0.0548,  0.0264,  0.0076,  0.0044,  0.0004,  0.0004]


# Dados Relativos a filial 2.
requests2  = [0.0612,0.1204,0.1476,0.1228,0.1080,0.1100,0.0788,0.0776,0.0576,0.0516,0.0328,0.0236,0.0080]
deliveries2 = [0.0192,0.0848,0.1540,0.1956,0.2040,0.1528,0.0884,0.0556,0.0284,0.0100,0.0040,0.0024,0.0008]

#requests2 = [0.0456, 0.0804, 0.1328, 0.1316, 0.1348, 0.1136, 0.098 , 0.084 , 0.0592, 0.0504, 0.0408, 0.02  , 0.0088]
#deliveries2 = [0.0444,0.0776,0.1324,0.144,0.1376,0.1048,0.0944,0.0832,0.0636,0.0516,0.0356,0.0236,0.0072]


(tMat,cMat,dict) = entryProblem([requests1,requests2],[deliveries1,deliveries2])

k = 169

calls = valueIteration(7, 169, tMat, cMat)

for i in range(0, 13):
	for j in range(0,12):
		print(dict.get(calls[i*13+j]) + '\t'),
	print(dict.get(calls[i*13+12]))

