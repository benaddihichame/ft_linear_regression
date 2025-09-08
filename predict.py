import os

def load_thetas():
    try:
        with open("thetas.txt", "r") as file:
            line = file.readlines()
            theta0 = float(line[0].strip())
            theta1 = float(line[1].strip())
            return theta0, theta1
    except (FileNotFoundError, IndexError, ValueError):
        print("No thetas found, returning 0.0, 0.0")
        return 0.0, 0.0


def estimate_price(mileage, theta0, theta1):
    return theta0 + theta1 * mileage

def get_mileage_from_user():
    while True:
        try:
            mileage_input = input("Enter the mileage of the car: ")
            mileage = float(mileage_input)

            if mileage < 0:
                print("Mileage cannot be negative. Please enter a valid mileage.")
                continue
            return mileage
        except ValueError:
            print("Invalid input. Please enter a numeric value for mileage.")
        except KeyboardInterrupt:
            print("\nProcess interrupted by user. Exiting.")
            exit()

def main():
    print("Welcome to the car price estimator!")
    print()
    theta0, theta1 = load_thetas()
    print(f"Loaded thetas: theta0 = {theta0:.6f}, theta1 = {theta1:.6f}")
    print()

    while True:
        try:
            mileage = get_mileage_from_user()
            price = estimate_price(mileage, theta0, theta1)
            print(f"Estimated price for a car with {mileage:.0f} mileage is: ${price:.2f}")
            print()

            continue_choice = input("Would you like to estimate another price? (yes/no): ").strip().lower()
            if continue_choice not in ['yes', 'y', 'ye']:
                break

        except KeyboardInterrupt:
            print("\nProcess interrupted by user. Exiting.")
            break
    print("Thank you for using the car price estimator. Goodbye!")

if __name__ == "__main__":
    main()