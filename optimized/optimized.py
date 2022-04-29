#################
### LIBRARIES ###
#################

import sys
import csv
import time


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
			actions.append([action[NAME], float(action[PRICE]), float(action[PROFIT_PERCENT]), float(action[PRICE]) * float(action[PROFIT_PERCENT]) / 100])
		else:
			invalid_lines += 1
	file.close()

	return actions, total_lines, invalid_lines


@profile
def optimized(data):
	actions = sorted(data, key=lambda x: x[PROFIT_PERCENT])
	actions_combination = []
	expense = 0

	while actions:
		action = actions.pop()
		if action[PRICE] + expense < BUDGET_MAX:
			actions_combination.append(action)
			expense += action[PRICE]

	return actions_combination


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
			actions_combination = optimized(actions)
		except FileNotFoundError:
			print(f"Aucun fichier ou dossier avec ce nom : '{sys.argv[1]}'\n")
			sys.exit(0)

	print(f"\n** Analys des {total_lines} lignes du document **\n\n** Non prise en compte {invalid_lines} lignes invalides **\n\n")

	for action in actions_combination:
		print(f"** Nom : {action[NAME]} ** Prix de l'action : {round(action[PRICE], 2)}€ ** Profit : {round(action[PROFIT_EURO], 2)}€")

	print(f"\nVous gagnerez : {round(sum(action[PROFIT_EURO] for action in actions_combination), 2)} € au bout de deux ans pour un placement de {round(sum(action[PRICE] for action in actions_combination), 2)}€.")


start = time.perf_counter()
if __name__ in "__main__":
	main()
end = time.perf_counter()
print(f"\n** Temps de calcul : {round(end - start, 2)} secondes. **")