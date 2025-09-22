import csv

class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

def print_header():
    print(f"{Colors.HEADER}{Colors.BOLD}")
    print("╔══════════════════════════════════════════════════════════╗")
    print("║             🚗 CAR PRICE PREDICTION MODEL 🚗              ║")
    print("║             Machine Learning - Linear Regression         ║")
    print("╚══════════════════════════════════════════════════════════╝")
    print(f"{Colors.END}\n")

def print_data_info(mileages, prices):
    print(f"{Colors.GREEN}Data loaded successfully!{Colors.END}")
    print(f"{Colors.BLUE}Mileage range: {Colors.YELLOW}{min(mileages):.0f} - {max(mileages):.0f} km{Colors.END}")
    print(f"{Colors.BLUE}Price range: {Colors.YELLOW}{min(prices):.0f} - {max(prices):.0f} €{Colors.END}\n")

def print_final_results(theta0, theta1):
    print(f"\n{Colors.GREEN}{Colors.BOLD}")
    print("╔══════════════════════════════════════════════════════════╗")
    print("║                    🎯 FINAL RESULTS 🎯                    ║")
    print("╚══════════════════════════════════════════════════════════╝")
    print(f"{Colors.END}")
    
    print(f"{Colors.CYAN}Model parameters for original data:{Colors.END}")
    print(f"{Colors.YELLOW}   theta0 (base price): {Colors.BOLD}{theta0:.2f}€{Colors.END}")
    print(f"{Colors.YELLOW}   theta1 (price per km): {Colors.BOLD}{theta1:.6f}€{Colors.END}")

def print_completion_message():
    print(f"\n{Colors.GREEN}{Colors.BOLD}Model training completed successfully!{Colors.END}")
    print(f"{Colors.CYAN}Your model is ready to predict car prices!{Colors.END}\n")

def load_data(file_path):
	km = []
	prices = []
	try:
		with open(file_path, 'r') as csvfile:
			reader = csv.reader(csvfile)
			next(reader)
			for row in reader:
				km_value = float(row[0])
				prices_value = float(row[1])
				km.append(km_value)
				prices.append(prices_value)
			print(f"{Colors.GREEN}Loaded {len(km)} entries from {file_path}{Colors.END}")
		return km, prices
	except FileNotFoundError:
		print(f"{Colors.RED}Error: The file {file_path} was not found.{Colors.END}")
		return [], []
	except Exception as e:
		print(f"{Colors.RED}An error occurred: {e}{Colors.END}")
		return [], []

def normalize_data(km):
	if not km:
		return [], 0, 1
	mean_km = sum(km) / len(km)
	
	total_squared_deviations = 0
	for x in km:
		deviation = x - mean_km
		squared_deviation = deviation ** 2
		total_squared_deviations += squared_deviation
	variance = total_squared_deviations / len(km)
	
	std_mileage = variance ** 0.5
	if std_mileage == 0:
		std_mileage = 1
	normalized_km = [(x - mean_km) / std_mileage for x in km]
	return normalized_km, mean_km, std_mileage

def estimate_price(km, theta0, theta1):
	return theta0 + (theta1 * km)

def calculate_total_error(km, prices, theta0, theta1):
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
    theta0 = 0.0
    theta1 = 0.0
    m = len(mileages)
    
    print(f"{Colors.BLUE}Starting training with {m} examples{Colors.END}")
    print(f"{Colors.BLUE}Learning rate: {learning_rate}, Max iterations: {max_iterations}{Colors.END}\n")
    
    for iteration in range(max_iterations):
        if iteration % 100 == 0:
            cost = calculate_total_error(mileages, prices, theta0, theta1)
            print(f"{Colors.CYAN}Iteration {iteration}: Error = {Colors.YELLOW}{cost:.2f}{Colors.CYAN}, theta0 = {theta0:.6f}, theta1 = {theta1:.6f}{Colors.END}")
        
        sum_error_theta0 = 0
        sum_error_theta1 = 0
        
        for i in range(m):
            prediction = estimate_price(mileages[i], theta0, theta1)
            error = prediction - prices[i]
            sum_error_theta0 += error
            sum_error_theta1 += error * mileages[i]
        
        tmp_theta0 = learning_rate * (1/m) * sum_error_theta0
        tmp_theta1 = learning_rate * (1/m) * sum_error_theta1
        
        theta0 = theta0 - tmp_theta0
        theta1 = theta1 - tmp_theta1
        
        if iteration > 0 and abs(tmp_theta0) < 1e-8 and abs(tmp_theta1) < 1e-8:
            print(f"{Colors.GREEN}Convergence reached at iteration {iteration}!{Colors.END}")
            break
    
    return theta0, theta1

def denormalize_thetas(theta0, theta1, mean_mileage, std_mileage):
    original_theta1 = theta1 / std_mileage
    original_theta0 = theta0 - (original_theta1 * mean_mileage)
    return original_theta0, original_theta1

def save_thetas(theta0, theta1):
    try:
        with open("thetas.txt", "w") as file:
            file.write(f"{theta0}\n")
            file.write(f"{theta1}\n")
        print(f"{Colors.GREEN}Parameters saved to thetas.txt{Colors.END}")
    except Exception as e:
        print(f"{Colors.RED}Error saving parameters: {e}{Colors.END}")

def main():
    print_header()

    mileages, prices = load_data("data.csv")
    
    if not mileages:
        print(f"{Colors.RED}No data loaded. Stopping program.{Colors.END}")
        return
    
    print_data_info(mileages, prices)
    
    print(f"{Colors.CYAN}Normalizing data...{Colors.END}")
    normalized_mileages, mean_mileage, std_mileage = normalize_data(mileages)
    
    print(f"{Colors.HEADER}Starting model training...{Colors.END}\n")
    theta0_norm, theta1_norm = train_model(normalized_mileages, prices, 
                                          learning_rate=0.01, max_iterations=1000)
    
    theta0, theta1 = denormalize_thetas(theta0_norm, theta1_norm, mean_mileage, std_mileage)
    
    print_final_results(theta0, theta1) 

    save_thetas(theta0, theta1)
    
    print_completion_message()
    
if __name__ == "__main__":
    main()
