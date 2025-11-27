import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os
import webbrowser


# Bee Swarm Simulator GUI Progress Calculator



# ITEM DATA

ITEM_DATA = {
    "Honey Mask": {
        "image": "images/honey_mask.png",
        "materials": {
            "Honey": 5000000,
            "Oil": 5,
            "Enzymes": 5,
            "Glue": 15,
            "Royal Jelly": 250,
        },
    },
    "Gummy Mask": {
        "image": "images/gummy_mask.png",
        "materials": {
            "Honey": 5000000000,
            "Glue": 250,
            "Enzymes": 100,
            "Gumdrops": 5000,
            
        },
    },
    "Petal Wand": {
        "image": "images/petal_wand.png",
        "materials": {
            "Honey": 15000000000,
            "Petals": 10,
            "Spirit Petals": 3,
            "Drops of Devotion": 100,
            "Star Jelly": 75,
        },
    },
    "Gummy Baller": {
        "image": "images/Gummy_Baller.png",
        "materials": {
            "Honey": 10000000000000,
            "Glues": 1500,
            "Gumdrops": 2000,
            "Caustic Wax": 50,
            "Super Smoothie": 50,
            "Turpentine": 5,
            "Satisfying Vials": 3,
        },
    },
}


# PLAYER INVENTORY

player_inventory = {
    "Blue Extract": 0,
    "Caustic Wax": 0,
    "Coconut": 0,
    "Comforting Vial": 0,
    "Enzymes": 0,
    "Glue": 0,
    "Glitter": 0,
    "Gumdrops": 0,
    "Hard Wax": 0,
    "Honey": 0,
    "Honey Suckle": 0,
    "Invigorating Vial": 0,
    "Moon Charm": 0,
    "Motivating Vial": 0,
    "Nectar Shower Vial": 0,
    "Oil": 0,
    "Petals": 0,
    "Purple Potion": 0,
    "Red Extract": 0,
    "Refreshing Vial": 0,
    "Royal Jelly": 0,
    "Satisfying Vial": 0,
    "Soft wax": 0,
    "Star Jelly": 0,
    "Super Smootie": 0,
    "Swirled Wax": 0,
    "Tropical Drink": 0,
    "Turpentine": 0,
    "Whites": 0,
}


# CALCULATE PROGRESS

def calculate_progress(recipe, inventory):
    results = []
    for mat, needed in recipe.items():
        have = inventory.get(mat, 0)
        remaining = max(0, needed - have)
        percent = min(100, (have / needed) * 100)
        results.append((mat, have, needed, remaining, percent))
    return results


# GUI CLASS

class BeeSwarmGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Bee Swarm Progress Calculator v0.2")
        self.root.geometry("1000x750")

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill="both")

        # Tabs (Credits added last)
        self.build_search_tab()
        self.build_inventory_tab()
        self.build_stats_tab()
        self.build_ssa_tab()
        self.build_credits_tab()  # Last tab

        # Footer
        self.footer_text = tk.StringVar(value="Version 0.2")
        tk.Label(root, textvariable=self.footer_text, font=("Arial", 10)).pack(anchor="sw", padx=5, pady=5)

    
    # SEARCH TAB
    
    def build_search_tab(self):
        self.search_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.search_tab, text="Item Search")

        top_frame = ttk.Frame(self.search_tab)
        top_frame.pack(pady=15)

        ttk.Label(top_frame, text="Select Item:", font=("Arial", 16)).pack(side="left")

        self.search_var = tk.StringVar()
        self.search_combobox = ttk.Combobox(
            top_frame, textvariable=self.search_var, values=list(ITEM_DATA.keys()), width=40
        )
        self.search_combobox.pack(side="left", padx=10)
        self.search_combobox.bind("<KeyRelease>", self.filter_items)

        ttk.Button(top_frame, text="Search", command=self.search_item).pack(side="left")

        self.result_frame = tk.Frame(self.search_tab)
        self.result_frame.pack(pady=20, expand=True)

    def filter_items(self, event):
        typed = self.search_var.get().lower()
        filtered = [i for i in ITEM_DATA if typed in i.lower()]
        self.search_combobox['values'] = filtered

    def search_item(self):
        for w in self.result_frame.winfo_children():
            w.destroy()

        item = self.search_var.get()
        if item not in ITEM_DATA:
            tk.Label(self.result_frame, text="No item selected.", font=("Arial", 14)).pack(pady=10)
            return

        data = ITEM_DATA[item]

        frame = tk.Frame(self.result_frame)
        frame.pack()

        # Image
        img_path = data["image"]
        if os.path.exists(img_path):
            img = Image.open(img_path).resize((140, 140))
            img_tk = ImageTk.PhotoImage(img)
            lbl = tk.Label(frame, image=img_tk)
            lbl.image = img_tk
            lbl.pack(pady=5)
        else:
            tk.Label(frame, text="[Missing Image]", font=("Arial", 12)).pack(pady=5)

        ttk.Label(frame, text=item, font=("Arial", 20, "bold")).pack(pady=5)

        # Materials under each other
        results = calculate_progress(data["materials"], player_inventory)
        for mat, have, need, remaining, pct in results:
            ttk.Label(frame, text=f"{mat}: {have}/{need} | Remaining: {remaining} | {pct:.1f}%").pack(pady=2)

    
    # INVENTORY TAB
    
    def build_inventory_tab(self):
        self.inventory_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.inventory_tab, text="Inventory Editor")

        frame = ttk.Frame(self.inventory_tab)
        frame.pack(pady=10, padx=10, fill="both", expand=True)

        self.inventory_entries = {}
        columns = 3
        for i, mat in enumerate(sorted(player_inventory.keys())):
            row = i // columns * 2
            col = i % columns
            tk.Label(frame, text=f"{mat}:", font=("Arial", 12)).grid(row=row, column=col, sticky="w", padx=10, pady=2)
            var = tk.StringVar(value=str(player_inventory[mat]))
            tk.Entry(frame, textvariable=var, width=12).grid(row=row+1, column=col, padx=10, pady=2)
            self.inventory_entries[mat] = var

        tk.Button(frame, text="Save Inventory", command=self.save_inventory).grid(
            row=row+2, column=0, columnspan=columns, pady=10
        )

    def save_inventory(self):
        for mat, var in self.inventory_entries.items():
            try:
                player_inventory[mat] = int(var.get())
            except ValueError:
                pass
        messagebox.showinfo("Saved", "Inventory updated!")

    
    # STATS TAB
    
    def build_stats_tab(self):
        self.stats_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.stats_tab, text="Stats")

        ttk.Label(self.stats_tab, text="Player Stats", font=("Arial", 20, "bold")).pack(pady=15)

        default_stats = [
            "Honey Per Hour:",
            "Bee Count:",
            "Gifted Bees:",
            "Average Bee Level:",
            "Blue / Red / White Pollen %:",
            "Instant Conversion %:",
            "Critical Chance:",
            "Critical Power:",
        ]

        self.stat_inputs = {}
        for s in default_stats:
            row = ttk.Frame(self.stats_tab)
            row.pack(anchor="w", pady=5)
            ttk.Label(row, text=s, width=30).pack(side="left")
            var = tk.StringVar()
            ttk.Entry(row, textvariable=var, width=20).pack(side="left")
            self.stat_inputs[s] = var

    
    # SSA TAB
    
    def build_ssa_tab(self):
        self.ssa_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.ssa_tab, text="SSA Builds")

        ttk.Label(self.ssa_tab, text="Supreme Star Amulet Builds", font=("Arial", 20, "bold")).pack(pady=15)

        # Horizontal frame for hives
        hframe = ttk.Frame(self.ssa_tab)
        hframe.pack(pady=10)

        # Helper to add SSA
        def add_ssa(frame, title, img_path):
            sub = ttk.Frame(frame)
            sub.pack(side="left", padx=10)
            ttk.Label(sub, text=title, font=("Arial", 16, "bold")).pack(pady=5)
            if os.path.exists(img_path):
                img = Image.open(img_path).resize((60, 60))
                img_tk = ImageTk.PhotoImage(img)
                lbl = tk.Label(sub, image=img_tk)
                lbl.image = img_tk
                lbl.pack()

        add_ssa(hframe, "White Hive", "images/White_SSA.png")
        add_ssa(hframe, "Blue Hive", "images/blue_hive.png")
        add_ssa(hframe, "Red Hive", "images/red_hive.png")

    
    # CREDITS TAB (added last)
    
    def build_credits_tab(self):
        self.credits_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.credits_tab, text="Credits")

        frame = ttk.Frame(self.credits_tab)
        frame.pack(pady=50)

        tk.Label(frame, text="Bee Swarm Progress Calculator v0.2", font=("Arial", 20, "bold")).pack(pady=10)
        tk.Label(frame, text="Created by recasted", font=("Arial", 14)).pack(pady=5)

        ttk.Button(frame, text="Discord", command=lambda: webbrowser.open("https://discord.gg/bxpjpWdmsr")).pack(pady=5)
        ttk.Button(frame, text="GitHub", command=lambda: webbrowser.open("https://github.com/Recasted")).pack(pady=5)



# Run GUI

if __name__ == "__main__":
    root = tk.Tk()
    app = BeeSwarmGUI(root)
    root.mainloop()
