import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os
import shutil
from assistant import analyze_image
from curator import ColorEnvironment, DQNAgent

class ImageReviewApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Image Review for Model Training")
        self.master.geometry("800x600")

        self.base_dir = "scraped_images"
        self.current_image_path = ""
        self.accepted_dir = "accepted_images"
        self.discarded_dir = "discarded_images"
        self.images = []
        self.current_index = 0

        self.create_widgets()
        self.load_model()

    def create_widgets(self):
        self.image_label = tk.Label(self.master)
        self.image_label.pack(pady=10)

        self.button_frame = tk.Frame(self.master)
        self.button_frame.pack(pady=10)

        self.accept_button = tk.Button(self.button_frame, text="Accept", command=self.accept_image)
        self.accept_button.pack(side=tk.LEFT, padx=5)

        self.discard_button = tk.Button(self.button_frame, text="Discard", command=self.discard_image)
        self.discard_button.pack(side=tk.LEFT, padx=5)

        self.load_images_button = tk.Button(self.master, text="Load Images", command=self.load_images)
        self.load_images_button.pack(pady=10)

        self.train_button = tk.Button(self.master, text="Train Model", command=self.train_model)
        self.train_button.pack(pady=10)

    def load_model(self):
        state_shape = (64, 64, 3)
        num_actions = 3
        self.agent = DQNAgent(state_shape, num_actions)

    def load_images(self):
        self.images = []
        for root, dirs, files in os.walk(self.base_dir):
            for file in files:
                if file.endswith(('.png', '.jpg', '.jpeg')) and 'segment' in file:
                    self.images.append(os.path.join(root, file))
        
        if self.images:
            self.current_index = 0
            self.show_image()
        else:
            messagebox.showinfo("No Images", "No images found in the scraped_images directory.")

    def show_image(self):
        if self.images:
            self.current_image_path = self.images[self.current_index]
            image = Image.open(self.current_image_path)
            image = image.resize((400, 400), Image.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            self.image_label.config(image=photo)
            self.image_label.image = photo

    def accept_image(self):
        if self.current_image_path:
            os.makedirs(self.accepted_dir, exist_ok=True)
            shutil.move(self.current_image_path, os.path.join(self.accepted_dir, os.path.basename(self.current_image_path)))
            self.next_image()

    def discard_image(self):
        if self.current_image_path:
            os.makedirs(self.discarded_dir, exist_ok=True)
            shutil.move(self.current_image_path, os.path.join(self.discarded_dir, os.path.basename(self.current_image_path)))
            self.next_image()

    def next_image(self):
        self.current_index += 1
        if self.current_index < len(self.images):
            self.show_image()
        else:
            self.image_label.config(image=None)
            self.image_label.image = None
            messagebox.showinfo("Complete", "All images have been reviewed.")

    def train_model(self):
        accepted_images = [os.path.join(self.accepted_dir, f) for f in os.listdir(self.accepted_dir)]  
        env = ColorEnvironment(accepted_images)
        num_episodes = 1000

        for episode in range(num_episodes):
            state = env.reset()
            done = False
            while not done:
                action = self.agent.act(state)
                next_state, reward, done = env.step(action)
                self.agent.remember(state, action, reward, next_state, done)
                state = next_state
                self.agent.train()
            if episode % 10 == 0:
                self.agent.update_target_model()
            
            if episode % 100 == 0:
                messagebox.showinfo("Training Progress", f"Completed {episode} episodes")

        self.agent.model.save('color_selection_model.h5')
        messagebox.showinfo("Training Complete", "Model has been trained with accepted images.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageReviewApp(root)
    root.mainloop()