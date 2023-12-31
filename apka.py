import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import filedialog

class IncidenceListReader:
    def __init__(self):
        self.incidents_data = []

    def read_incidents_from_text_widget(self, text_widget):
        text_content = text_widget.get("1.0", tk.END)
        incidents = [line.strip().split(':') for line in text_content.splitlines() if line]
        self.incidents_data = [(left.strip(), [element.strip() for element in right.split(',')]) for left, right in incidents]

    def get_incidents_data(self):
        return self.incidents_data

def update_graph_and_matrix():
    incidence_list_reader.read_incidents_from_text_widget(incidence_text)

    # Update DataFrame
    df = pd.DataFrame(incidence_list_reader.get_incidents_data(), columns=['source', 'target'])

    # Update directed graph from data
    G.clear()
    G.add_edges_from([(row.source, target) for row in df.itertuples(index=False) for target in row.target if target])

    # Update Matplotlib plot
    pos = nx.spring_layout(G)
    ax.clear()
    nx.draw(G, pos, with_labels=True, arrowsize=20, node_size=700, node_color="skyblue",
            font_size=10, font_color="black", font_weight="bold", font_family="sans-serif")
    plt.title("Graph based on DataFrame")
    canvas.draw()

    # Update Text widget with adjacency matrix
    adjacency_matrix = nx.linalg.graphmatrix.adjacency_matrix(G).todense()
    adjacency_text.delete(1.0, tk.END)
    adjacency_text.insert(tk.END, str(adjacency_matrix))

# Function to update graph and matrix when the text widget is edited
def on_text_edit(event):
    update_graph_and_matrix()

# Create directed graph
G = nx.DiGraph()

# Create Tkinter window
root = tk.Tk()
root.title("Graph and Adjacency Matrix Viewer")
root.geometry("1200x600")

# Create Tkinter widgets
incidence_text = tk.Text(root, height=5, width=50)
incidence_text.grid(row=0, column=0, padx=10, pady=10)

update_button = tk.Button(root, text="Update Graph and Matrix", command=update_graph_and_matrix)
update_button.grid(row=1, column=0, pady=10)

# Embed Matplotlib plot in Tkinter window
fig, ax = plt.subplots()
canvas = FigureCanvasTkAgg(fig, master=root)
canvas_widget = canvas.get_tk_widget()
canvas_widget.grid(row=2, column=0, padx=10, pady=10)

# Text widget for displaying and editing adjacency matrix
adjacency_text = tk.Text(root, height=20, width=40)
adjacency_text.grid(row=2, column=1, padx=10, pady=10)

# Create incidence list reader instance
incidence_list_reader = IncidenceListReader()

# Bind the on_text_edit function to the text widget's key release event
incidence_text.bind("<KeyRelease>", on_text_edit)

# Start the main event loop
root.mainloop()
