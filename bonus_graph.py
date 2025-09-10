import csv
import matplotlib.pyplot as plt
import numpy as np

def load_data(file_path):
    km = []
    prices = []
    try:
        with open(file_path, 'r') as csv_files:
            reader = csv.reader(csv_files)
            next(reader)
            for row in reader:
                km_value = float(row[0])
                price_value = float(row[1])
                km.append(km_value)
                prices.append(price_value)
        print(f"Loaded {len(km)} data points from {file_path}")
        return km, prices
    except FileNotFoundError:
        print(f"Error: the file {file_path} was not found")
        return [], []
    except Exception as e:
        print(f"An error occrured: {e}")
        return [], []

def load_thetas():
    try:
        with open("thetas.txt", "r") as file:
            line = file.readline()
            theta0 = float(line[0].strip())
            theta1 = float(line[1].strip())
            return theta0, theta1
    except (FileNotFoundError, IndexError, ValueError):
        print("No thetas found, using default value (0,0)")
        return 0.0 , 0.0


def estimate_price(km, theta0, theta1):
    return theta0 + theta1 * km

def calculate_r_squared(actual_price, predicted_price):

    mean_actual = sum(actual_price) / len(actual_price)
    ss_res = sum((actual - predicted) ** 2 for actual, predicted in zip(actual_price, predicted_price))
    ss_tot = sum((actual - mean_actual) ** 2 for actual in actual_price)

    if ss_tot == 0:
        return 1.0
    
    r_squared = 1 - (ss_res / ss_tot)
    return r_squared

def create_visualization():
    print("===== Creation of the Graph =========")
    print()


    mileages , prices = load_data("data.csv")
    if not mileages:
        print("Impossible to load data, STOP")
        return
    theta0, theta1 = load_thetas()
    print(f"Parameter of the model: theta = {theta0: .2f}, theta1 = {theta1:.6f}")
    predicted_prices = [estimate_price(km, theta0, theta1) for km in mileages]

    r_squared = calculate_r_squared(prices, predicted_prices)
    print(f"Coefficient R² = {r_squared:.4f}")

    plt.figure(figsize =(12, 8))

    plt.scatter(mileages, prices, color = 'blue', alpha=0.7, s=50, label = 'real data', edgecolors='navy', linewidths=0.5)

    min_km =min(mileages)
    max_km= max(mileages)
    line_km = np.linspace(min_km, max_km, 100)
    line_prices = [estimate_price(km, theta0, theta1) for km in line_km]

    plt.plot(line_km, line_prices, color = 'red', linewidth=2, label=f'Linear Regression\n(y = {theta0:.0f} + {theta1:.4f}x)')


    plt.xlabel("Kilometrage (km)", fontsize=12, fontweight='bold')
    plt.ylabel("Price (€)", fontsize=12, fontweight='bold')
    plt.title("Price prediction of the car compared with de Mileage",fontsize=14, fontweight='bold', pad=20)

    plt.grid(True, alpha = 0.3, linestyle='--')
    plt.legend(fontsize=11,loc='upper right')

    textstr = f'''Statistiques du modèle:
    • Nombre d'échantillons: {len(mileages)}
    • Coefficient R²: {r_squared:.4f}
    • Intercept (θ₀): {theta0:.0f} €
    • Pente (θ₁): {theta1:.6f} €/km'''

    props = dict(boxstyle='round', facecolor='wheat', alpha=0.8)
    plt.text(0.02, 0.98,textstr, transform=plt.gca().transAxes, fontsize=10, verticalalignment='top', bbox=props)

    plt.tight_layout()
    print()
    print("=== Exemples de prédictions ===")
    test_kms = [0, 50000, 100000, 150000, 200000]
    for km in test_kms:
        predicted = estimate_price(km, theta0, theta1)
        print(f"{km:6d} km → {predicted:7.0f} €")
    
    # 7. Affiche le graphique
    print()
    print("Affichage du graphique... (fermez la fenêtre pour continuer)")
    plt.show()
    
    # 8. Option pour sauvegarder
    save_choice = input("Voulez-vous sauvegarder le graphique ? (o/n): ").lower()
    if save_choice in ['o', 'oui', 'y', 'yes']:
        filename = "linear_regression_visualization.png"
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"Graphique sauvegardé dans {filename}")

def main():
    """
    Fonction principale
    """
    print("🎨 === BONUS - Visualisation de la régression linéaire ===")
    print()
    
    try:
        create_visualization()
    except ImportError:
        print("❌ Erreur: matplotlib n'est pas installé.")
        print("Installez-le avec: pip install matplotlib")
    except Exception as e:
        print(f"❌ Erreur inattendue: {e}")
    
    print()
    print("✨ Visualisation terminée !")

if __name__ == "__main__":
    main()