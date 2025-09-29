# Car Price Prediction - Linear Regression

A machine learning project that predicts car prices based on mileage using linear regression with gradient descent algorithm.

## Overview

This project implements a linear regression model from scratch to predict car prices based on their mileage. The model uses gradient descent optimization and includes data normalization for better performance.

## Features

- Custom linear regression implementation
- Gradient descent optimization algorithm
- Data normalization for improved training
- Interactive prediction system
- Model persistence (save/load trained parameters)
- Input validation and error handling

## Project Structure

```
ft_linear_regression/
├── data.csv           # Training dataset (mileage, price)
├── load_data.py       # Model training script
├── predict.py         # Price prediction script
├── thetas.txt         # Trained model parameters
└── README.md          # Documentation
```

## Usage

### Training the Model

```bash
python3 load_data.py
```

This will:
- Load the dataset (24 car examples)
- Normalize the mileage data
- Train the linear regression model using gradient descent
- Save the trained parameters to `thetas.txt`

### Making Predictions

```bash
python3 predict.py
```

This will:
- Load the trained model parameters
- Provide an interactive interface to predict car prices
- Handle input validation

## Algorithm

The model learns the relationship:
```
Price = θ₀ + θ₁ × Mileage
```

Where:
- **θ₀ (theta0)**: Base price of a car with 0 km
- **θ₁ (theta1)**: Price change per kilometer

### Training Process

1. **Data Normalization**: Convert mileage to standard scale
2. **Gradient Descent**: Iteratively optimize parameters
3. **Cost Function**: Mean Squared Error (MSE)
4. **Convergence**: Stop when parameter changes become minimal

## Performance

- Training Examples: 24 cars
- Mileage Range: 22,899 - 240,000 km
- Price Range: 3,650 - 8,290 €
- Average Error: ~680€ per prediction

## Mathematical Foundation

The gradient descent algorithm:

```
Cost Function: J(θ₀,θ₁) = (1/2m) × Σ(h(x⁽ⁱ⁾) - y⁽ⁱ⁾)²

Update Rules:
θ₀ := θ₀ - α × (1/m) × Σ(h(x⁽ⁱ⁾) - y⁽ⁱ⁾)
θ₁ := θ₁ - α × (1/m) × Σ((h(x⁽ⁱ⁾) - y⁽ⁱ⁾) × x⁽ⁱ⁾)

Where:
- m = number of training examples
- α = learning rate (0.01)
- h(x) = θ₀ + θ₁ × x (hypothesis function)
```

## Example Predictions

| Mileage (km) | Predicted Price|
|--------------|----------------|
| 50,000       | 7,427€         |
| 100,000      | 6,355€ 		|
| 150,000      | 5,283€ 		|
| 200,000      | 4,210€			|

## Requirements

- Python 3.8+
- No external ML libraries required for core functionality
