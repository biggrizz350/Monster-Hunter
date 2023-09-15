import requests
import tkinter as tk
from tkinter import ttk, messagebox


class MonsterStatsApp:
    def __init__(self):
        # Create a window and set its title
        self.window = tk.Tk()
        self.window.title("Monster Stats App")

        # Create a label and an entry widget for the monster name
        label = ttk.Label(self.window, text="Enter a monster name:")
        label.pack(pady=10)
        self.monster_name_entry = ttk.Entry(self.window)
        self.monster_name_entry.pack(pady=5)

        # Create a button to retrieve the monster stats
        button = ttk.Button(self.window, text="Get Stats", command=self.get_monster_stats)
        button.pack(pady=10)

        # Create a text widget to display the monster stats
        self.stats_text = tk.Text(self.window, width=50, height=20, wrap=tk.WORD)
        self.stats_text.pack(pady=10)

        # Set the style of the window using the ttk Style class
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TLabel', foreground='#3b3f3f', font=('Arial', 12))
        self.style.configure('TButton', foreground='#ffffff', background='#2c2f31', font=('Arial', 12))

        # Run the main loop to display the window
        self.window.mainloop()

    def get_monster_stats(self):
        # Get the monster name from the entry widget
        monster_name = self.monster_name_entry.get()

        # Make a GET request to the Monster Hunter World API to retrieve the list of monsters
        response = requests.get('https://mhw-db.com/monsters')

        # Check if the response was successful
        if response.status_code == 200:
            # Retrieve the JSON data from the response
            data = response.json()

            # Create a dictionary of monsters with their IDs as keys for easy lookup
            monsters = {}
            for monster in data:
                monsters[monster['id']] = monster

            # Search for the ID of the corresponding monster
            monster_id = None
            for id, monster in monsters.items():
                if monster['name'].lower() == monster_name.lower():
                    monster_id = id
                    break

            if monster_id is not None:
                # Make a GET request to the Monster Hunter World API to retrieve monster data
                response = requests.get(f'https://mhw-db.com/monsters/{monster_id}')

                # Check if the response was successful
                if response.status_code == 200:
                    # Retrieve the JSON data from the response
                    data = response.json()

                    # Create a string with the monster's name and stats
                    stats = f"Name: {data['name']}\n"
                    stats += f"Species: {data['species']}\n"
                    stats += f"Type: {data['type']}\n"
                    stats += f"Description: {data['description']}\n\n"

                    # Create a string with the monster's weaknesses
                    weaknesses = "Weaknesses:\n"
                    for weakness in data['weaknesses']:
                        stars = "★" * int(weakness['stars'])
                        weaknesses += f"- {weakness['element']} ({stars})\n"

                    # Display the monster's stats and weaknesses in the text widget
                    self.stats_text.delete('1.0', tk.END)
                    self.stats_text.insert(tk.END, stats)
                    self.stats_text.insert(tk.END, weaknesses)
                else:
                    messagebox.showerror("Error", f"Error retrieving data for monster '{monster_name}'. Status code: {response.status_code}")
            else:
                messagebox.showerror("Error", f"No monster found with the name '{monster_name}'.")
        else:
            messagebox.showerror("Error", f"Error retrieving monster list. Status code: {response.status_code}")


if __name__ == '__main__':
    # Create an instance of the MonsterStatsApp
    app = MonsterStatsApp()
