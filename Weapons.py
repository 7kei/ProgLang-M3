import pygame
import os

class Item:
    def __init__(self, x, y, item_images, window):
        """
        Initializes the Item class with three item slots.
        
        Args:
            x (int): The x-coordinate of the top-left corner for the items display.
            y (int): The y-coordinate of the top-left corner for the items display.
            item_images (list of str): List of paths to the item images (each item has two images - [unselected, selected]).
            window (pygame.Surface): The window where items will be displayed.
        """
        self.window = window
        self.item_images = [self.load_images(path) for path in item_images]
        self.selected_item = None
        self.item_boxes = [pygame.Rect(x + i * 110, y, 100, 100) for i in range(3)]

    def load_images(self, path):
        """Loads both versions (unselected and selected) of an item image."""
        unselected = pygame.image.load(path[0])
        selected = pygame.image.load(path[1])
        return {"unselected": unselected, "selected": selected}

    def draw(self):
        """Draws the item boxes and items, updating appearance based on selection."""
        for i, item_box in enumerate(self.item_boxes):
            pygame.draw.rect(self.window, (255, 255, 255), item_box, 2)  # Draw item box frame
            
            # Determine if item is selected and get corresponding image
            item_state = "selected" if self.selected_item == i else "unselected"
            item_image = self.item_images[i][item_state]
            
            # Center the item image inside the box
            item_rect = item_image.get_rect(center=item_box.center)
            self.window.blit(item_image, item_rect)

    def handle_event(self, event):
        """Handles keyboard input to select items."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                self.selected_item = 0
            elif event.key == pygame.K_2:
                self.selected_item = 1
            elif event.key == pygame.K_3:
                self.selected_item = 2

# Usage within the game loop:
# Initialize items (provide paths for unselected and selected images for each item)
items = Item(100, 750, [
    ["D:/Downloads/A.Y 2024 - 2025/1st Term/CS121/proglang proj/assets/weapons/weapon icons (toggled, untoggled)/1.png", "D:/Downloads/A.Y 2024 - 2025/1st Term/CS121/proglang proj/assets/weapons/weapon icons (toggled, untoggled)/2.png"],
    ["D:/Downloads/A.Y 2024 - 2025/1st Term/CS121/proglang proj/assets/weapons/weapon icons (toggled, untoggled)/3.png", "D:/Downloads/A.Y 2024 - 2025/1st Term/CS121/proglang proj/assets/weapons/weapon icons (toggled, untoggled)/4.png"],
    ["D:/Downloads/A.Y 2024 - 2025/1st Term/CS121/proglang proj/assets/weapons/weapon icons (toggled, untoggled)/5.png", "D:/Downloads/A.Y 2024 - 2025/1st Term/CS121/proglang proj/assets/weapons/weapon icons (toggled, untoggled)/6.png"]
], window)

# Within the main loop or update method:
for event in pygame.event.get():
    items.handle_event(event)
items.draw()
