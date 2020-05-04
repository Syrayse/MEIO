import numpy as np 

# Estimates, for each decision, the expected contribution.
def estContributions(k, tMat, cMat):
	return [np.array(np.sum(np.multiply(tMat[i],cMat[i]), axis=1)).reshape((k,1)) for i in range(k)]

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
	contribs = estContributions(nDecisions, transMat, contribMat)

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


t = []
t.append(np.array([[0.75,0.25],[0.3333,0.6667]]))
t.append(np.array([[0.75,0.25],[0.3333,0.6667]]))

c = []
c.append(np.array([[8,4],[6,-7.5]]))
c.append(np.array([[-10,6],[3,12]]))

print(valueIteration(2,2,t,c))