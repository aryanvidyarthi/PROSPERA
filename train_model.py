# train_model.py

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import joblib
import os
import sys

def main():
    # Define the path to the CSV file
    csv_file = 'stock_data.csv'

    # Check if the CSV file exists
    if not os.path.exists(csv_file):
        print(f"Error: '{csv_file}' not found in the current directory.")
        sys.exit(1)

    # Load the dataset
    try:
        data = pd.read_csv(csv_file)
        print("CSV file loaded successfully.")
    except pd.errors.EmptyDataError:
        print(f"Error: '{csv_file}' is empty.")
        sys.exit(1)
    except pd.errors.ParserError:
        print(f"Error: '{csv_file}' is malformed or contains parsing errors.")
        sys.exit(1)

    # Verify that necessary columns exist
    required_columns = ['Open', 'High', 'Low', 'Close', 'Volume', 'Recommendation']
    if not all(column in data.columns for column in required_columns):
        print(f"Error: '{csv_file}' must contain the following columns: {', '.join(required_columns)}")
        sys.exit(1)

    # Feature selection
    X = data[['Open', 'High', 'Low', 'Close', 'Volume']]
    y = data['Recommendation']

    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Initialize the model
    model = RandomForestClassifier(n_estimators=100, random_state=42)

    # Train the model
    model.fit(X_train, y_train)
    print("Model training completed.")

    # Predictions
    y_pred = model.predict(X_test)

    # Evaluation
    print("Classification Report:")
    print(classification_report(y_test, y_pred))
    print(f"Accuracy: {accuracy_score(y_test, y_pred)}")

    # Save the model
    model_file = 'stock_recommendation_model.pkl'
    joblib.dump(model, model_file)
    print(f"Model saved as '{model_file}'")

if __name__ == "__main__":
    main()

