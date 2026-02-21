import customtkinter as ctk
from tkinter import filedialog
import os

# 1. Setup the modern theme
ctk.set_appearance_mode("System")  # Automatically matches your OS dark/light mode
ctk.set_default_color_theme("blue")  # The accent color for buttons and switches


# 2. Define the Application Class
class ExcelCruncherApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window configuration
        self.title("Excel Data Cruncher")
        self.geometry("500x450")
        self.file_path = None

        # --- UI Layout ---

        # Title Label
        self.title_label = ctk.CTkLabel(self, text="Task Automation Tool", font=ctk.CTkFont(size=20, weight="bold"))
        self.title_label.pack(pady=(20, 10)) # pady adds vertical padding (top, bottom)

        # File Selection Button
        self.file_btn = ctk.CTkButton(self, text="Select Excel File", command=self.select_file)
        self.file_btn.pack(pady=10)

        # Label to show selected file name
        self.file_label = ctk.CTkLabel(self, text="No file selected", text_color="gray")
        self.file_label.pack(pady=5)

        # Parameter Input (Entry Widget)
        self.param_entry = ctk.CTkEntry(self, placeholder_text="Enter a multiplier (e.g., 1.5)", width=200)
        self.param_entry.pack(pady=20)

        # Action Button (The "Crunch" trigger)
        self.run_btn = ctk.CTkButton(self, text="Crunch Numbers", command=self.process_data, fg_color="green", hover_color="darkgreen")
        self.run_btn.pack(pady=10)

        # Output Text Box
        self.output_box = ctk.CTkTextbox(self, height=120, width=400)
        self.output_box.pack(pady=10)
        self.output_box.insert("0.0", "Awaiting input...")

    # --- Event Functions ---

    def select_file(self):
        # Opens your operating system's native file picker
        self.file_path = filedialog.askopenfilename(
            title="Select Excel File",
            filetypes=[("Excel files", "*.xlsx *.xls")]
        )
        if self.file_path:
            filename = os.path.basename(self.file_path)
            self.file_label.configure(text=f"Selected: {filename}", text_color="white") # Update label

    def process_data(self):
        # Clear previous text from the output box
        self.output_box.delete("0.0", "end")

        # 1. Basic Validation
        if not self.file_path:
            self.output_box.insert("0.0", "Error: Please select an Excel file first!\n")
            return

        try:
            multiplier = float(self.param_entry.get())
        except ValueError:
            self.output_box.insert("0.0", "Error: Please enter a valid number for the multiplier!\n")
            return

        # 2. The actual Python logic
        try:
            # Here is where you would do: df = pd.read_excel(self.file_path)
            # For this demo, we will simulate the crunching:
            self.output_box.insert("end", f"Loading {os.path.basename(self.file_path)}...\n")
            self.output_box.insert("end", f"Applying multiplier: {multiplier}\n")
            self.output_box.insert("end", "-" * 30 + "\n")

            # Simulated result
            simulated_base_value = 1042
            final_result = simulated_base_value * multiplier

            self.output_box.insert("end", f"Calculation successful!\nFinal Value: {final_result}")

        except Exception as e:
            self.output_box.insert("end", f"A fatal error occurred:\n{e}")


# Run the app
if __name__ == "__main__":
    app = ExcelCruncherApp()
    app.mainloop()  # This starts the infinite event loop that keeps the window open
