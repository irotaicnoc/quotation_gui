import customtkinter as ctk

# 1. Setup the modern theme
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


class ExcelCruncherApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window configuration
        self.title("Data Transcription Tool")
        self.geometry("600x600")

        # This list will hold dictionaries containing our input widgets
        # so we can easily loop through them when crunching the numbers.
        self.rows = []

        # --- UI Layout ---

        # Title Label
        self.title_label = ctk.CTkLabel(self, text="Image Data Entry", font=ctk.CTkFont(size=20, weight="bold"))
        self.title_label.pack(pady=(20, 10))

        # The Scrollable Frame (This acts as our dynamic viewport)
        self.scroll_frame = ctk.CTkScrollableFrame(self, width=500, height=300)
        self.scroll_frame.pack(pady=10, padx=20, fill="both", expand=True)

        # Add Row Button
        self.add_btn = ctk.CTkButton(self, text="+ Add New Row", command=self.add_row)
        self.add_btn.pack(pady=10)

        # Action Button (The "Crunch" trigger)
        self.run_btn = ctk.CTkButton(self, text="Process Data", command=self.process_data, fg_color="green", hover_color="darkgreen")
        self.run_btn.pack(pady=10)

        # Output Text Box
        self.output_box = ctk.CTkTextbox(self, height=120, width=500)
        self.output_box.pack(pady=(10, 20), padx=20)

        # Automatically add the first row on startup
        self.add_row()

    # --- Event Functions ---

    def add_row(self):
        # Create a transparent container frame for this specific row
        row_frame = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
        row_frame.pack(fill="x", pady=5)

        # Input 1
        entry1 = ctk.CTkEntry(row_frame, placeholder_text="First Value", width=180)
        entry1.pack(side="left", padx=10)

        # Input 2
        entry2 = ctk.CTkEntry(row_frame, placeholder_text="Second Value", width=180)
        entry2.pack(side="left", padx=10)

        # Delete Button (Uses a lambda to pass the specific row's widgets to the delete function)
        del_btn = ctk.CTkButton(
            row_frame, text="X", width=30, fg_color="#d9534f", hover_color="#c9302c",
            command=lambda f=row_frame: self.delete_row(f)
        )
        del_btn.pack(side="right", padx=10)

        # Store the frame and entries so we can access them later
        self.rows.append({
            "frame": row_frame,
            "entry1": entry1,
            "entry2": entry2
        })

    def delete_row(self, frame_to_delete):
        # 1. Remove the dictionary from our Python list
        self.rows = [row for row in self.rows if row["frame"] != frame_to_delete]
        # 2. Destroy the tkinter frame (this removes it from the screen instantly)
        frame_to_delete.destroy()

    def process_data(self):
        self.output_box.delete("0.0", "end")

        extracted_data = []

        # Iterate through the stored entry widgets and extract their text using .get()
        for i, row in enumerate(self.rows):
            val1 = row["entry1"].get()
            val2 = row["entry2"].get()

            # Skip completely empty rows gracefully
            if not val1 and not val2:
                continue

            try:
                # Assuming numerical data for this example
                num1 = float(val1)
                num2 = float(val2)
                extracted_data.append((num1, num2))
            except ValueError:
                self.output_box.insert("end", f"Error in Row {i+1}: Please enter valid numbers.\n")
                return

        if not extracted_data:
            self.output_box.insert("0.0", "No valid data to process.\n")
            return

        # --- The actual Python logic goes here ---
        self.output_box.insert("end", f"Successfully extracted {len(extracted_data)} rows of data.\n")
        self.output_box.insert("end", "-" * 30 + "\n")

        # Example calculation: Sum of all (Value 1 * Value 2)
        total = sum(v1 * v2 for v1, v2 in extracted_data)
        self.output_box.insert("end", f"Calculated Total: {total}\n")


if __name__ == "__main__":
    app = ExcelCruncherApp()
    app.mainloop()
