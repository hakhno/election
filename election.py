#election thingy
#potentiall nmodify schem to include
#schema of import data: party, name, vote
#schema of operating data: party, name, first prefs, current vote, vote history
#to-dos:
#first:
#scrape data
#chunk things
#refactor a bit
#make it do all of the things
#second:
#add in proportional surpluses
#third
#run a bunch of sims

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
	#get index of first party name
	parties = [x[0] for x in data]
	try:
		destination = parties.index(party)
	except ValueError:
		x = transferParty(party)
		try:
			destination = parties.index(x)
		except ValueError:
			x = noPartyTransfer(party)
			destination = parties.index(x)
	data[destination][3] += surplus
	#this is in the wrong place
	for each in data:
		y = each[3]
		each[4].append(y)
	return data

def transferParty(party):
	try:
		return transfers[party]
	except:
		return raw_input(party + " transfers to: ")

def noPartyTransfer(party):
	if party == "Labour":
		return "Conservative"
	return raw_input("No match. " + party + " transfers to: ")

def testPrintTable():
	print "Count " + str(count)
	print "--------"
	print "ELECTED:"
	print "--------"
	for each in winners:
		print each[0] + "\t" + str(each[3])
	print "RUNNING:"
	print "--------"
	for each in data:
		print each[0] + "\t" + str(each[3])
	print "ELIMINATED:"
	print "-----------"
	for each in losers:
		print each[0] + "\t" + str(each[3])
	print

data = []
seats = 5
winners = []
losers = []
count = 1
transfers = {"Mebyon Kernow": "Green Party", "Green Party": "Labour", "Labour": "Liberal Democrat", "Liberal Democrat": "Conservative", "Conservative": "UKIP", "UKIP": "Conservative", "The Principles Of Politics Party": "Mebyon Kernow", "Restore the Family for Children's Sake": "Mebyon Kernow", "National Health Action": "Mebyon Kernow", "Independent": "Mebyon Kernow"}

with open("election.csv", "rb") as csvfile:
	reader = csv.reader(csvfile)
	for row in reader:
		row[2] = int(row[2])
		row.append(row[2])
		row.append([])
		data.append(row)
		#print row

electorate = calculateElectorate(data)
quota = calculateQuota(electorate, seats)
#print electorate, quota

while len(winners) < seats:
	#sort
	data = sorted(data, reverse=True, key=itemgetter(3))
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
		flag = "ELECTED"
	elif (len(winners) + len(data)) == seats:
		pass
		#everyone remaining is elected
	#potential problem for non-quota victories? make a unit test whatever it is
	#probably just add something if the test above is one greater than seats
	#eliminate lowest	
	else:
		eliminated = data.pop()
		surplus = eliminated[3]
		eliminated[4].append("ELIMINATED")
		party = eliminated[0]
		losers.append(eliminated)
		flag = "ELIMINATED"
	#testPrintTable()
	#print flag
	if len(winners) < seats:
		data = distributeSurplus(data, party, surplus)
	if len(data) == 1 and len(winners) == seats:
		eliminated = data.pop()
		eliminated[4].append("ELIMINATED")
		losers.append(eliminated)
		flag = "ELIMINATED"
	#print
	count += 1

# print "DONE"
# print
winnersSorted = sorted(winners, reverse=True, key=itemgetter(3))
losersSorted = sorted(losers, reverse=True, key=itemgetter(3))
for each in winnersSorted:
	output = each[0] + " "*(25-len(each[0]))
	output += each[1] + " "*(25-len(each[1]))
	output += str(each[2]) + " "*(7-len(str(each[2])))
	output += str(each[3])
	print output
for each in losersSorted:
	output = each[0][:23] + " "*(23-len(each[0])) + "  "
	output += each[1] + " "*(25-len(each[1]))
	output += str(each[2]) + " "*(7-len(str(each[2])))
	output += str(each[3])
	print output
# print
# print losers	

#now write everything to a CSV
