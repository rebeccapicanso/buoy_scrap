import numpy as np
from typing import List, Tuple, Optional

class ReinforcedClassifier:
    def __init__(self, input_size: int, n_classes: int, learning_rate: float = 0.01):
        """
        Initialize the reinforced classifier
        
        Args:
            input_size: Number of input features
            n_classes: Number of classification classes
            learning_rate: Learning rate for weight updates
        """
        self.input_size = input_size
        self.n_classes = n_classes
        self.learning_rate = learning_rate
        
        # Initialize weights randomly
        self.weights = np.random.randn(input_size, n_classes) * 0.01
        self.bias = np.zeros((1, n_classes))
        
        # Keep track of the policy history
        self.state_history: List[np.ndarray] = []
        self.action_history: List[int] = []
        self.reward_history: List[float] = []

    def softmax(self, x: np.ndarray) -> np.ndarray:
        """Apply softmax function to get action probabilities"""
        exp_x = np.exp(x - np.max(x, axis=1, keepdims=True))
        return exp_x / np.sum(exp_x, axis=1, keepdims=True)

    def forward(self, x: np.ndarray) -> np.ndarray:
        """Forward pass to get class probabilities"""
        logits = np.dot(x, self.weights) + self.bias
        return self.softmax(logits)

    def choose_action(self, state: np.ndarray) -> int:
        """Choose an action (class) based on current policy"""
        probabilities = self.forward(state)
        action = np.random.choice(self.n_classes, p=probabilities[0])
        
        self.state_history.append(state)
        self.action_history.append(action)
        
        return action

    def give_reward(self, reward: float):
        """Store reward for the last action"""
        self.reward_history.append(reward)

    def update_policy(self):
        """Update the policy based on collected experience"""
        for state, action, reward in zip(
            self.state_history, 
            self.action_history, 
            self.reward_history
        ):
            # Calculate gradients
            probabilities = self.forward(state)
            d_softmax = probabilities.copy()
            d_softmax[0, action] -= 1  # Derivative of cross-entropy
            
            # Update weights and bias
            gradient_w = np.dot(state.T, d_softmax) * reward
            gradient_b = d_softmax * reward
            
            self.weights -= self.learning_rate * gradient_w
            self.bias -= self.learning_rate * gradient_b
        
        # Clear history
        self.state_history = []
        self.action_history = []
        self.reward_history = []

    def train(self, 
              X: np.ndarray, 
              y: np.ndarray, 
              episodes: int, 
              batch_size: Optional[int] = None) -> List[float]:
        """
        Train the model
        
        Args:
            X: Training features
            y: True labels
            episodes: Number of training episodes
            batch_size: Batch size for training (optional)
        
        Returns:
            List of average rewards per episode
        """
        if batch_size is None:
            batch_size = len(X)
            
        avg_rewards = []
        
        for episode in range(episodes):
            episode_rewards = []
            
            # Random batch selection
            indices = np.random.choice(len(X), batch_size, replace=False)
            batch_X = X[indices]
            batch_y = y[indices]
            
            for state, true_class in zip(batch_X, batch_y):
                state = state.reshape(1, -1)
                
                # Choose action and get reward
                predicted_class = self.choose_action(state)
                reward = 1.0 if predicted_class == true_class else -1.0
                self.give_reward(reward)
                episode_rewards.append(reward)
            
            # Update policy after collecting batch experience
            self.update_policy()
            
            # Store average reward for this episode
            avg_reward = np.mean(episode_rewards)
            avg_rewards.append(avg_reward)
            
        return avg_rewards

    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Predict classes for input data
        
        Args:
            X: Input features
        
        Returns:
            Predicted class labels
        """
        probabilities = self.forward(X)
        return np.argmax(probabilities, axis=1)

# Example usage
if __name__ == "__main__":
    # Generate some dummy data
    np.random.seed(42)
    X_train = np.random.randn(100, 4)  # 100 samples, 4 features
    y_train = np.random.randint(0, 3, 100)  # 3 classes
    
    # Create and train the model
    model = ReinforcedClassifier(input_size=4, n_classes=3)
    rewards = model.train(X_train, y_train, episodes=100, batch_size=32)
    
    # Make predictions
    predictions = model.predict(X_train)
    accuracy = np.mean(predictions == y_train)
    print(f"Training accuracy: {accuracy:.2f}")