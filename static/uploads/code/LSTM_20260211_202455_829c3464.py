"""
===============================================================================
ML Learning Assistant - Generated Code
Topic: LSTM
Generated on: 2026-02-11 20:24:55

DEPENDENCIES:
pip install scikit-learn
pip install pandas
pip install matplotlib
pip install keras
pip install numpy

INSTRUCTIONS:
1. Install required dependencies using pip
2. Run this script in your Python environment
3. For Google Colab: Copy and paste directly
===============================================================================
"""

# Import necessary libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Dense, LSTM, Dropout
from keras.callbacks import EarlyStopping
from keras.optimizers import Adam
from keras.utils import to_categorical
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Define a function to load and preprocess the data
def load_and_preprocess_data(file_path):
    """
    Load the dataset and preprocess it.

    Args:
    - file_path (str): The path to the dataset file.

    Returns:
    - X (numpy array): The feature data.
    - y (numpy array): The target data.
    """
    try:
        # Load the dataset
        data = pd.read_csv(file_path)

        # Convert the data to numpy arrays
        X = data.drop('target', axis=1).values
        y = data['target'].values

        # Scale the data using Min-Max Scaler
        scaler = MinMaxScaler()
        X_scaled = scaler.fit_transform(X)

        return X_scaled, y

    except Exception as e:
        print(f"Error loading and preprocessing data: {e}")

# Define a function to split the data into training and testing sets
def split_data(X, y, test_size=0.2, random_state=42):
    """
    Split the data into training and testing sets.

    Args:
    - X (numpy array): The feature data.
    - y (numpy array): The target data.
    - test_size (float, optional): The proportion of the data to use for testing. Defaults to 0.2.
    - random_state (int, optional): The random seed to use for splitting the data. Defaults to 42.

    Returns:
    - X_train (numpy array): The training feature data.
    - X_test (numpy array): The testing feature data.
    - y_train (numpy array): The training target data.
    - y_test (numpy array): The testing target data.
    """
    try:
        # Split the data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)

        return X_train, X_test, y_train, y_test

    except Exception as e:
        print(f"Error splitting data: {e}")

# Define a function to create and compile the LSTM model
def create_and_compile_lstm_model(input_shape, output_units, dropout_rate=0.2, learning_rate=0.001):
    """
    Create and compile the LSTM model.

    Args:
    - input_shape (tuple): The shape of the input data.
    - output_units (int): The number of output units.
    - dropout_rate (float, optional): The dropout rate to use. Defaults to 0.2.
    - learning_rate (float, optional): The learning rate to use. Defaults to 0.001.

    Returns:
    - model (keras model): The compiled LSTM model.
    """
    try:
        # Create the LSTM model
        model = Sequential()
        model.add(LSTM(units=50, return_sequences=True, input_shape=input_shape))
        model.add(Dropout(dropout_rate))
        model.add(LSTM(units=50))
        model.add(Dropout(dropout_rate))
        model.add(Dense(output_units, activation='softmax'))

        # Compile the model
        optimizer = Adam(learning_rate=learning_rate)
        model.compile(loss='categorical_crossentropy', optimizer=optimizer, metrics=['accuracy'])

        return model

    except Exception as e:
        print(f"Error creating and compiling LSTM model: {e}")

# Define a function to train the LSTM model
def train_lstm_model(model, X_train, y_train, X_test, y_test, epochs=10, batch_size=32, patience=5):
    """
    Train the LSTM model.

    Args:
    - model (keras model): The LSTM model to train.
    - X_train (numpy array): The training feature data.
    - y_train (numpy array): The training target data.
    - X_test (numpy array): The testing feature data.
    - y_test (numpy array): The testing target data.
    - epochs (int, optional): The number of epochs to train for. Defaults to 10.
    - batch_size (int, optional): The batch size to use. Defaults to 32.
    - patience (int, optional): The patience to use for early stopping. Defaults to 5.

    Returns:
    - history (keras history): The training history.
    """
    try:
        # Define the early stopping callback
        early_stopping = EarlyStopping(patience=patience, restore_best_weights=True)

        # Train the model
        history = model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size, validation_data=(X_test, y_test), callbacks=[early_stopping])

        return history

    except Exception as e:
        print(f"Error training LSTM model: {e}")

# Define a function to evaluate the LSTM model
def evaluate_lstm_model(model, X_test, y_test):
    """
    Evaluate the LSTM model.

    Args:
    - model (keras model): The LSTM model to evaluate.
    - X_test (numpy array): The testing feature data.
    - y_test (numpy array): The testing target data.

    Returns:
    - loss (float): The test loss.
    - accuracy (float): The test accuracy.
    """
    try:
        # Evaluate the model
        loss, accuracy = model.evaluate(X_test, y_test)

        return loss, accuracy

    except Exception as e:
        print(f"Error evaluating LSTM model: {e}")

# Define a function to visualize the training and testing accuracy
def visualize_accuracy(history):
    """
    Visualize the training and testing accuracy.

    Args:
    - history (keras history): The training history.
    """
    try:
        # Plot the training and testing accuracy
        plt.plot(history.history['accuracy'], label='Training Accuracy')
        plt.plot(history.history['val_accuracy'], label='Testing Accuracy')
        plt.xlabel('Epochs')
        plt.ylabel('Accuracy')
        plt.legend()
        plt.show()

    except Exception as e:
        print(f"Error visualizing accuracy: {e}")

# Example usage
if __name__ == "__main__":
    # Load and preprocess the data
    X, y = load_and_preprocess_data('data.csv')

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = split_data(X, y)

    # Reshape the data for LSTM
    X_train = np.reshape(X_train, (X_train.shape[0], 1, X_train.shape[1]))
    X_test = np.reshape(X_test, (X_test.shape[0], 1, X_test.shape[1]))

    # One-hot encode the target data
    y_train = to_categorical(y_train)
    y_test = to_categorical(y_test)

    # Create and compile the LSTM model
    model = create_and_compile_lstm_model((1, X_train.shape[2]), y_train.shape[1])

    # Train the LSTM model
    history = train_lstm_model(model, X_train, y_train, X_test, y_test)

    # Evaluate the LSTM model
    loss, accuracy = evaluate_lstm_model(model, X_test, y_test)
    print(f"Test Loss: {loss}, Test Accuracy: {accuracy}")

    # Visualize the training and testing accuracy
    visualize_accuracy(history)

    # Make predictions
    predictions = model.predict(X_test)
    predicted_classes = np.argmax(predictions, axis=1)
    actual_classes = np.argmax(y_test, axis=1)

    # Print the classification report and confusion matrix
    print(classification_report(actual_classes, predicted_classes))
    print(confusion_matrix(actual_classes, predicted_classes))