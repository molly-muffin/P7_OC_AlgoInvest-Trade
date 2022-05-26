#################
### LIBRARIES ###
#################

import sys
import csv
import time
from itertools import combinations


#################
### VARIABLES ###
#################

BUDGET_MAX = 500

NAME = 0
PRICE = 1
PROFIT_PERCENT = 2 
PROFIT_EURO = 3


#################
### FUNCTIONS ###
#################

def create_list(file):
	actions = []
	total_lines = 0
	invalid_lines = 0

	file = open(sys.argv[1])
	csvreader = csv.reader(file)
	remove = next(csvreader)
	for action in csvreader:
		total_lines += 1
		if float(action[PRICE]) > 0 and float(action[PROFIT_PERCENT]) > 0:
			actions.append([action[NAME], round(float(action[PRICE])), round(float(action[PROFIT_PERCENT])), round(float(action[PRICE]) * float(action[PROFIT_PERCENT])) / 100])
		else:
			invalid_lines += 1
	file.close()

	return actions, total_lines, invalid_lines


def algorithm_bruteforce(data):
	best_profit = 0
	best_comb = None

	for action in range(len(data)):
		for comb in combinations(data, action + 1):
			price = sum([action[PRICE] for action in comb])
			profit = sum([action[PROFIT_EURO]for action in comb])
			if price <= BUDGET_MAX and profit > best_profit:
				best_profit = profit
				actions_combination = comb

	return  actions_combination


def algorithm_optimized(wallet, data):
	number_of_actions = len(data)
	actions_combination = []

	matrix = [[0 for x in range(wallet + 1)] for x in range(number_of_actions +1)]

	for i in range(1, number_of_actions + 1):
		for x in range(1, wallet + 1):
			if data[i-1][PRICE] <= x:
				matrix[i][x] = max(data[i-1][PROFIT_EURO] + matrix[i-1][x-data[i-1][PRICE]], 
				matrix[i-1][x])
			else:
				matrix[i][x] = matrix[i-1][x]
	
	while wallet >= 0 and number_of_actions >= 0:
		if matrix[number_of_actions][wallet] != matrix[number_of_actions-1][wallet]:
			actions_combination.append(data[number_of_actions-1])
			wallet -= data[number_of_actions-1][PRICE]
		number_of_actions -= 1
 
	return actions_combination


def choice(data):
	choice = None
	while not choice:
		choice = input("Choisir un algorithme :\n\n"
					   "[1] Algorithme Bruteforce (combination)\n"
					   "[2] Algorithme Optimized (dynamic)\n\n"
					   "--> ")

		if choice == '1':
			algorithm = algorithm_bruteforce(data)
		elif choice == '2':
			algorithm = algorithm_optimized(BUDGET_MAX, data)

	return algorithm


############
### MAIN ###
############
def main():
	if len(sys.argv) < 2:
		print("Vous devez indiquer un fichier en argument.")
		sys.exit(0)
	elif len(sys.argv) != 2:
		print("Vous avez indiquez trop d'arguments.")
		sys.exit(0)
	else:
		try:
			print("\n** Traitement des données **\n")
			actions, total_lines, invalid_lines = create_list(sys.argv[1])
			actions_combination = choice(actions)
		except FileNotFoundError:
			print(f"Aucun fichier ou dossier avec ce nom : '{sys.argv[1]}'\n")
			sys.exit(0)

	print(f"\n** Analys des {total_lines} lignes du document **\n\n** Non prise en compte {invalid_lines} lignes invalides **\n\n")

	for action in actions_combination:
		print(f"** Nom : {action[NAME]} ** Prix de l'action : {round(action[PRICE], 2)}€ ** Profit : {round(action[PROFIT_EURO], 2)}€")

	print(f"\nVous gagnerez : {round(sum(action[PROFIT_EURO] for action in actions_combination), 2)} € au bout de deux ans pour un placement de {round(sum(action[PRICE] for action in actions_combination), 2)}€.")

	total_investment = sum([(x[PRICE]) for x in actions_combination])
	total_profit = sum([(x[PROFIT_EURO]) for x in actions_combination])
	print(f"\nCe qui représente un retour sur investissement de : {round(total_profit / total_investment * 100, 2)}% \n")

start = time.perf_counter()
if __name__ in "__main__":
	main()
end = time.perf_counter()
print(f"\n** Temps de calcul : {round(end - start, 2)} secondes. **")