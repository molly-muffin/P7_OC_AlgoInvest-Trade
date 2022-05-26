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


#################
### FUNCTIONS ###
#################
def create_list(file):
	file = open(file)
	reader = csv.reader(file)
	remove = next(reader)
	actions = [[line[0], float(line[1]), float(line[1]) * float(line[2]) / 100] for line in reader]
	file.close()

	return actions

def bruteforce(data):
	best_profit = 0
	best_comb = None
	expense = 0

	for i in range(len(data)):
		for comb in combinations(data, i + 1):
			price = sum([i[1] for i in comb])
			profit = sum([i[2]for i in comb])
			if price <= BUDGET_MAX and profit > best_profit:
				best_profit = profit
				best_comb = comb
				expense = price

	return best_profit, best_comb, expense


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
			actions = create_list(sys.argv[1])
		except FileNotFoundError:
			print(f"Aucun fichier ou dossier avec ce nom : '{sys.argv[1]}'\n")
			sys.exit(0)
	print("\n** Bruteforce en cours d'execution, merci de patienter **\n")
	print(f"\nListe de la meilleure combinaison d'actions pour un maximum de {BUDGET_MAX}€ : \n")
	best_profit, best_comb, expense = bruteforce(actions)
	for action in best_comb:
		print(f"** Nom : {str(action[0])} ** Prix de l'action : {round(float(action[1]), 2)}€ ** Profit : {round(float(action[2]), 2)}€ ")
	
	print(f"\nVous gagnerez : {round(best_profit, 2)}€ au bout de deux ans pour un placement de {round(expense, 2)}€.")

start = time.perf_counter()
if __name__ in "__main__":
	main()
end = time.perf_counter()
print(f"\n** Temps de calcul : {round(end - start, 2)} secondes. **")