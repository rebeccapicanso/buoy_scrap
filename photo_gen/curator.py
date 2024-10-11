import numpy as np
import tensorflow as tf
from collections import deque
import random
import os
from PIL import Image
from sklearn.model_selection import train_test_split

def get_dominant_color(image):
    # Implement dominant color extraction logic
    # This is a placeholder implementation
    return random.randint(0, 2)  # Returns 0 (red), 1 (green), or 2 (blue)

def preprocess_image(image_path):
    # Load and preprocess the image
    img = Image.open(image_path)
    img = img.resize((64, 64))  # Resize to a standard size
    img_array = np.array(img) / 255.0  # Normalize pixel values
    return img_array

class ColorEnvironment:
    def __init__(self, images):
        self.images = images
        self.current_image = None

    def reset(self):
        self.current_image = random.choice(self.images)
        return preprocess_image(self.current_image)

    def step(self, action):
        reward = 1 if action == get_dominant_color(self.current_image) else -1
        done = True
        return preprocess_image(self.current_image), reward, done

class DQNAgent:
    def __init__(self, state_shape, num_actions):
        self.model = self.create_model(state_shape, num_actions)
        self.target_model = self.create_model(state_shape, num_actions)
        self.target_model.set_weights(self.model.get_weights())
        self.replay_memory = deque(maxlen=10000)
        self.gamma = 0.95
        self.epsilon = 1.0
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.batch_size = 32

    def create_model(self, input_shape, num_actions):
        model = tf.keras.models.Sequential([
            tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=input_shape),
            tf.keras.layers.MaxPooling2D((2, 2)),
            tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
            tf.keras.layers.MaxPooling2D((2, 2)),
            tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
            tf.keras.layers.Flatten(),
            tf.keras.layers.Dense(64, activation='relu'),
            tf.keras.layers.Dense(num_actions)
        ])
        model.compile(optimizer='adam', loss='mse')
        return model

    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(3)
        q_values = self.model.predict(state[np.newaxis, ...])
        return np.argmax(q_values[0])

    def remember(self, state, action, reward, next_state, done):
        self.replay_memory.append((state, action, reward, next_state, done))

    def train(self):
        if len(self.replay_memory) < self.batch_size:
            return
        minibatch = random.sample(self.replay_memory, self.batch_size)
        states, targets = [], []
        for state, action, reward, next_state, done in minibatch:
            target = self.model.predict(state[np.newaxis, ...])
            if done:
                target[0][action] = reward
            else:
                t = self.target_model.predict(next_state[np.newaxis, ...])
                target[0][action] = reward + self.gamma * np.amax(t)
            states.append(state)
            targets.append(target[0])
        self.model.fit(np.array(states), np.array(targets), epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def update_target_model(self):
        self.target_model.set_weights(self.model.get_weights())

def load_images(directory):
    images = []
    for filename in os.listdir(directory):
        if filename.endswith((".png", ".jpg", ".jpeg")):
            images.append(os.path.join(directory, filename))
    return images

def train_model(agent, env, episodes):
    for episode in range(episodes):
        state = env.reset()
        done = False
        while not done:
            action = agent.act(state)
            next_state, reward, done = env.step(action)
            agent.remember(state, action, reward, next_state, done)
            state = next_state
            agent.train()
        if episode % 10 == 0:
            agent.update_target_model()
        print(f"Episode: {episode+1}/{episodes}, Epsilon: {agent.epsilon:.2f}")

def evaluate_model(agent, env, num_episodes):
    correct_predictions = 0
    total_predictions = 0
    for _ in range(num_episodes):
        state = env.reset()
        action = agent.act(state)
        _, reward, _ = env.step(action)
        if reward == 1:
            correct_predictions += 1
        total_predictions += 1
    accuracy = correct_predictions / total_predictions
    print(f"Model Accuracy: {accuracy:.2f}")

def main():
    # Load your own images
    image_directory = "path/to/your/image/directory"
    all_images = load_images(image_directory)
    
    # Split images into training and testing sets
    train_images, test_images = train_test_split(all_images, test_size=0.2, random_state=42)
    
    # Create environment and agent
    train_env = ColorEnvironment(train_images)
    test_env = ColorEnvironment(test_images)
    state_shape = (64, 64, 3)  # Assuming 64x64 RGB images
    num_actions = 3  # Red, Green, Blue
    agent = DQNAgent(state_shape, num_actions)
    
    # Train the model
    train_model(agent, train_env, episodes=1000)
    
    # Evaluate the model
    evaluate_model(agent, test_env, num_episodes=100)

if __name__ == "__main__":
    main()