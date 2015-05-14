#election thingy
#potentiall nmodify schem to include
#schema of import data: party, name, vote
#schema of operating data: party, name, first prefs, current vote, vote history
#very broken, somewhere

from operator import itemgetter
import csv

#functions
def calculateElectorate(constituencyArray):
	electorate = 0
	for each in constituencyArray:
		electorate += each[2]
	return electorate 

def calculateQuota(electorate, seats):
	return (electorate/(seats+1)) + 1

def distributeSurplus(data, party, surplus):
	#returns a modified array with the new votes added
	#try and make this more efficient
	for each in data:
		if each[0] == party:
			each[3] += surplus
			break
	destination = transferParty(party)
	for each in data:
		if each[0] == destination:
			each[3] += surplus
			break
	return data

def transferParty(party):
	return raw_input(party + " transfers to: ")

data = []
seats = 5
winners = []
losers = []

with open("election.csv", "rb") as csvfile:
	reader = csv.reader(csvfile)
	for row in reader:
		row[2] = int(row[2])
		row.append(row[2])
		row.append([])
		data.append(row)
		print row

electorate = calculateElectorate(data)
quota = calculateQuota(electorate, seats)
print electorate, quota

while len(winners) < seats:
	#sort
	data = sorted(data, reverse=True, key=itemgetter(2))
	#check if someone is over the quota
	if data[0][3] >= quota:
		#elect and distribute surplus
		#watch out for multiple elections - while might work here
		#unit test - six candidates, five seats, five are over quota
		elected = data.pop(0)
		surplus = elected[3] - quota
		elected[4].append("ELECTED")
		party = elected[0]
		winners.append(elected)
		print elected
	#potential problem for non-quota victories? make a unit test whatever it is
	#eliminate lowest	
	else:
		eliminated = data.pop()
		surplus = eliminated[3]
		eliminated[4].append("ELIMINATED")
		party = eliminated[0]
		losers.append(eliminated)
		print eliminated
	data = distributeSurplus(data, party, surplus)

print	
print winners
print
print losers	
	#distribute
	#sort again
	#check for quota
