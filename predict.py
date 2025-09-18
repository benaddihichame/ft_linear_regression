import os

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

def load_thetas():
    try:
        with open("thetas.txt", "r") as file:
            line = file.readlines()
            theta0 = float(line[0].strip())
            theta1 = float(line[1].strip())
            print(f"{Colors.GREEN}✅ Model parameters loaded successfully!{Colors.END}")
            return theta0, theta1
    except (FileNotFoundError, IndexError, ValueError):
        print(f"{Colors.RED}❌ No trained model found! Please run 'python3 load_data.py' first.{Colors.END}")
        return 0.0, 0.0


def estimate_price(mileage, theta0, theta1):
    return theta0 + theta1 * mileage

def get_mileage_from_user():
    while True:
        try:
            mileage_input = input(f"{Colors.CYAN}🚗 Enter the car's mileage (km): {Colors.YELLOW}")
            print(f"{Colors.END}", end="")
            mileage = float(mileage_input)

            if mileage < 0:
                print(f"{Colors.RED}❌ Mileage cannot be negative. Please enter a valid mileage.{Colors.END}")
                continue
            
            # Validation basée sur les données d'entraînement
            if mileage > 300000:
                print(f"{Colors.YELLOW}⚠️  Warning: This mileage ({mileage:.0f} km) is very high!{Colors.END}")
                print(f"{Colors.YELLOW}   Our model was trained on cars with max 240,000 km.{Colors.END}")
                print(f"{Colors.YELLOW}   Prediction might be unreliable.{Colors.END}")
                
                confirm = input(f"{Colors.CYAN}   Continue anyway? (y/n): {Colors.YELLOW}").strip().lower()
                print(f"{Colors.END}", end="")
                if confirm not in ['y', 'yes']:
                    continue
            
            return mileage
        except ValueError:
            print(f"{Colors.RED}❌ Invalid input. Please enter a numeric value.{Colors.END}")
        except KeyboardInterrupt:
            print(f"\n{Colors.YELLOW}👋 Process interrupted by user. Goodbye!{Colors.END}")
            exit()

def main():
    print(f"{Colors.HEADER}{Colors.BOLD}")
    print("╔══════════════════════════════════════════════════════════╗")
    print("║            CAR PRICE PREDICTION SYSTEM                   ║")
    print("║              AI-Powered Price Estimator                  ║")
    print("╚══════════════════════════════════════════════════════════╝")
    print(f"{Colors.END}\n")
    
    print(f"{Colors.BLUE}🤖 Loading trained AI model...{Colors.END}")
    theta0, theta1 = load_thetas()
    
    if theta0 == 0.0 and theta1 == 0.0:
        print(f"{Colors.RED}🚫 Cannot proceed without a trained model. Exiting...{Colors.END}")
        return
    
    print(f"{Colors.GREEN}📊 Model parameters:{Colors.END}")
    print(f"{Colors.BLUE}   🔸 Base price (theta0): {Colors.YELLOW}{theta0:.2f}€{Colors.END}")
    print(f"{Colors.BLUE}   🔸 Price per km (theta1): {Colors.YELLOW}{theta1:.6f}€{Colors.END}")
    print()

    print(f"{Colors.CYAN}{Colors.BOLD}🎯 Ready to predict car prices!{Colors.END}\n")

    while True:
        try:
            mileage = get_mileage_from_user()
            price = estimate_price(mileage, theta0, theta1)
            
            print(f"\n{Colors.GREEN}{Colors.BOLD}")
            print("╔══════════════════════════════════════════════════════════╗")
            print("║                    💰 PREDICTION RESULT 💰               ║")
            print("╚══════════════════════════════════════════════════════════╝")
            print(f"{Colors.END}")
            
            print(f"{Colors.BLUE}🚗 Car with {Colors.YELLOW}{mileage:.0f} km{Colors.BLUE} mileage{Colors.END}")
            
            if price < 0:
                print(f"{Colors.RED}💰 Estimated price: {Colors.BOLD}{price:.2f}€{Colors.END}")
                print(f"{Colors.RED}⚠️  Warning: Negative price indicates the car is beyond economic repair!{Colors.END}")
                quality = f"{Colors.RED}🚫 Beyond economic viability{Colors.END}"
            else:
                print(f"{Colors.GREEN}💰 Estimated price: {Colors.BOLD}{Colors.YELLOW}{price:.2f}€{Colors.END}")
                # Ajout d'une évaluation qualitative
                if price > 7000:
                    quality = f"{Colors.GREEN}🟢 Excellent condition{Colors.END}"
                elif price > 5000:
                    quality = f"{Colors.YELLOW}🟡 Good condition{Colors.END}"
                elif price > 3000:
                    quality = f"{Colors.YELLOW}🟠 Fair condition{Colors.END}"
                else:
                    quality = f"{Colors.RED}🔴 High mileage{Colors.END}"
            
            print(f"{Colors.BLUE}📈 Assessment: {quality}")
            print()

            continue_choice = input(f"{Colors.CYAN}🔄 Would you like to estimate another price? {Colors.BOLD}(y/n): {Colors.YELLOW}").strip().lower()
            print(f"{Colors.END}", end="")
            
            if continue_choice not in ['yes', 'y', 'ye']:
                break
            print()

        except KeyboardInterrupt:
            print(f"\n{Colors.YELLOW}👋 Process interrupted by user.{Colors.END}")
            break
    
    print(f"\n{Colors.GREEN}{Colors.BOLD}")
    print("╔══════════════════════════════════════════════════════════╗")
    print("║                     👋 GOODBYE! 👋                       ║")
    print("║           Thank you for using our AI system!            ║")
    print("╚══════════════════════════════════════════════════════════╝")
    print(f"{Colors.END}")

if __name__ == "__main__":
    main()