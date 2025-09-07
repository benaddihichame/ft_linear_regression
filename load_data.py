import csv

def load_data(file_path):
	km = []
	prices = []
	try:
		with open(file_path, 'r') as csvfile:
			reader = csv.reader(csvfile)
			next(reader)  # Skip header row
			for row in reader:
				km = float(row[0])
				prices = float(row[1])
				km.append(km)
				prices.append(prices)
			print(f"Loaded {len(km)} entries from {file_path}")
		return km, prices
	except FileNotFoundError:
		print(f"Error: The file {file_path} was not found.")
		return [], []
	except Exception as e:
		print(f"An error occurred: {e}")
		return [], []

def normalize_data(km):
	if not km:
		return [], 0, 1
	
	mean_km = sum(km) / len(km)
	variance = sum((x - mean_km) ** 2 for x in km) / len(km)
	std_mileage = variance ** 0.5
	if std_mileage == 0:
		std_mileage = 1
	normalized_km = [(x - mean_km) / std_mileage for x in km]
	return normalized_km, mean_km, std_mileage

def estimate_price(km, theta0, theta1):
	return theta0 + (theta1 * km)

def calculate_cost(km, prices, theta0, theta1):
	if not km:
		return 0
	total_error = 0
	k = len(km)
	for i in range(k):
		predicted_price = estimate_price(km[i], theta0, theta1)
		error = predicted_price - prices[i]
		total_error += error ** 2
	return total_error / (2 * k)

def train_model(mileages, prices, learning_rate=0.01, max_iterations=1000):
    """
    Entraîne le modèle en utilisant l'algorithme de gradient descent
    """
    # Initialisation des paramètres
    theta0 = 0.0
    theta1 = 0.0
    m = len(mileages)  # Nombre d'exemples (c'est le 'm' du sujet !)
    
    print(f"Début de l'entraînement avec {m} exemples")
    print(f"Learning rate: {learning_rate}, Max iterations: {max_iterations}")
    print()
    
    # Boucle d'entraînement
    for iteration in range(max_iterations):
        # Calcule le coût actuel pour le monitoring
        if iteration % 100 == 0:  # Affiche tous les 100 itérations
            cost = calculate_cost(mileages, prices, theta0, theta1)
            print(f"Itération {iteration}: Coût = {cost:.2f}, theta0 = {theta0:.6f}, theta1 = {theta1:.6f}")
        
        # Calcule les gradients selon les formules du sujet
        sum_error_theta0 = 0  # Pour tmpθ0
        sum_error_theta1 = 0  # Pour tmpθ1
        
        # Parcours tous les exemples
        for i in range(m):
            # Calcule la prédiction avec les paramètres actuels
            prediction = estimate_price(mileages[i], theta0, theta1)
            
            # Calcule l'erreur
            error = prediction - prices[i]
            
            # Accumule les sommes pour les gradients
            sum_error_theta0 += error
            sum_error_theta1 += error * mileages[i]
        
        # Calcule les gradients (formules exactes du sujet)
        tmp_theta0 = learning_rate * (1/m) * sum_error_theta0
        tmp_theta1 = learning_rate * (1/m) * sum_error_theta1
        
        # Met à jour les paramètres SIMULTANÉMENT (très important !)
        theta0 = theta0 - tmp_theta0
        theta1 = theta1 - tmp_theta1
        
        # Vérifie la convergence (arrêt anticipé)
        if iteration > 0 and abs(tmp_theta0) < 1e-8 and abs(tmp_theta1) < 1e-8:
            print(f"Convergence atteinte à l'itération {iteration}")
            break
    
    # Coût final
    final_cost = calculate_cost(mileages, prices, theta0, theta1)
    print()
    print(f"Entraînement terminé !")
    print(f"Coût final: {final_cost:.2f}")
    print(f"Paramètres finaux: theta0 = {theta0:.6f}, theta1 = {theta1:.6f}")
    
    return theta0, theta1

def denormalize_thetas(theta0, theta1, mean_mileage, std_mileage):
    """
    Convertit les paramètres normalisés vers l'échelle originale
    """
    # Formules de dénormalisation
    original_theta1 = theta1 / std_mileage
    original_theta0 = theta0 - (original_theta1 * mean_mileage)
    
    return original_theta0, original_theta1

def save_thetas(theta0, theta1):
    """
    Sauvegarde les paramètres dans un fichier
    """
    try:
        with open("thetas.txt", "w") as file:
            file.write(f"{theta0}\n")
            file.write(f"{theta1}\n")
        print(f"Paramètres sauvegardés dans thetas.txt")
    except Exception as e:
        print(f"Erreur lors de la sauvegarde : {e}")

def main():
    """
    Fonction principale du programme d'entraînement
    """
    print("=== Entraînement du modèle de prédiction de prix ===")
    print()
    
    # 1. Charge les données
    mileages, prices = load_data("data.csv")
    
    if not mileages:
        print("Aucune donnée chargée. Arrêt du programme.")
        return
    
    print(f"Plage des kilomètrages: {min(mileages):.0f} - {max(mileages):.0f} km")
    print(f"Plage des prix: {min(prices):.0f} - {max(prices):.0f} €")
    print()
    
    # 2. Normalise les données
    normalized_mileages, mean_mileage, std_mileage = normalize_data(mileages)
    
    # 3. Entraîne le modèle
    theta0_norm, theta1_norm = train_model(normalized_mileages, prices, 
                                          learning_rate=0.01, max_iterations=1000)
    
    # 4. Dénormalise les paramètres pour l'usage réel
    theta0, theta1 = denormalize_thetas(theta0_norm, theta1_norm, mean_mileage, std_mileage)
    
    print()
    print("=== Paramètres pour les données originales ===")
    print(f"theta0 = {theta0:.6f}")
    print(f"theta1 = {theta1:.6f}")
    
    # 5. Sauvegarde les paramètres
    save_thetas(theta0, theta1)
    
    # 6. Test rapide
    print()
    print("=== Test rapide ===")
    test_mileages = [0, 50000, 100000, 150000, 200000]
    for km in test_mileages:
        predicted_price = theta0 + (theta1 * km)
        print(f"Prédiction pour {km:6d} km: {predicted_price:7.0f} €")

if __name__ == "__main__":
    main()
