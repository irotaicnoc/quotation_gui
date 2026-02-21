import customtkinter as ctk
from tkinter import filedialog
import os

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class ExcelCruncherApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Data Transcription & Processing Tool")
        self.geometry("800x750") # Made the window slightly wider to fit the dropdown

        self.rows = []
        self.selected_files = []
        self.file_names = ["No files loaded"] # Default state for the dropdown

        # --- UI Layout ---

        self.title_label = ctk.CTkLabel(self, text="Data Entry Workflow", font=ctk.CTkFont(size=20, weight="bold"))
        self.title_label.pack(pady=(20, 10))

        # The File Browser
        self.file_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.file_frame.pack(pady=10, padx=20, fill="x")

        self.browse_btn = ctk.CTkButton(
            self.file_frame,
            text="📁 Click to Browse for Excel Files\n(You can select multiple files)",
            height=80,
            font=ctk.CTkFont(size=14),
            fg_color="#2b2b2b",
            hover_color="#3b3b3b",
            border_width=2,
            border_color="#555555",
            command=self.select_files
        )
        self.browse_btn.pack(fill="x", expand=True)

        self.file_label = ctk.CTkLabel(self.file_frame, text="No files selected", text_color="gray", justify="left")
        self.file_label.pack(pady=(5, 0), anchor="w")

        # The Scrollable Frame
        self.scroll_frame = ctk.CTkScrollableFrame(self, height=250)
        self.scroll_frame.pack(pady=10, padx=20, fill="both", expand=True)

        self.add_btn = ctk.CTkButton(self, text="+ Add New Row", command=self.add_row, fg_color="#4a4a4a", hover_color="#5a5a5a")
        self.add_btn.pack(pady=5)

        # Action Button
        self.run_btn = ctk.CTkButton(self, text="Process Data", command=self.process_data, fg_color="green", hover_color="darkgreen", height=40)
        self.run_btn.pack(pady=10)

        # Output Text Box
        self.output_box = ctk.CTkTextbox(self, height=120)
        self.output_box.pack(pady=(0, 20), padx=20, fill="x")

        # Automatically add the first row on startup
        self.add_row()

    # --- Event Functions ---

    def select_files(self):
        file_paths = filedialog.askopenfilenames(
            title="Select Excel Files",
            filetypes=[("Excel files", "*.xlsx *.xls")]
        )

        if file_paths:
            self.selected_files = list(file_paths)

            # Extract just the file names (not the full path) for the dropdown menu
            self.file_names = [os.path.basename(f) for f in self.selected_files]

            # Update the label
            if len(self.selected_files) == 1:
                self.file_label.configure(text=f"Selected: {self.file_names[0]}", text_color="white")
            else:
                self.file_label.configure(text=f"Selected {len(self.selected_files)} files.", text_color="white")

            # DYNAMIC UPDATE: Push the new file names to all existing dropdown menus
            for row in self.rows:
                row["dropdown"].configure(values=self.file_names)
                row["dropdown"].set(self.file_names[0]) # Automatically select the first file

            self.output_box.insert("end", f"Loaded {len(self.selected_files)} files. Dropdowns updated.\n")

    def add_row(self):
        row_frame = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
        row_frame.pack(fill="x", pady=5)

        # --- NEW: Dropdown Menu ---
        file_dropdown = ctk.CTkOptionMenu(
            row_frame,
            values=self.file_names,
            width=200,
            dynamic_resizing=False # Keeps the UI stable even if file names are long
        )
        file_dropdown.pack(side="left", padx=(10, 5))

        # Input 1
        entry1 = ctk.CTkEntry(row_frame, placeholder_text="First Value", width=140)
        entry1.pack(side="left", padx=5)

        # Input 2
        entry2 = ctk.CTkEntry(row_frame, placeholder_text="Second Value", width=140)
        entry2.pack(side="left", padx=5)

        # Delete Button
        del_btn = ctk.CTkButton(
            row_frame, text="X", width=30, fg_color="#d9534f", hover_color="#c9302c",
            command=lambda f=row_frame: self.delete_row(f)
        )
        del_btn.pack(side="right", padx=10)

        # Store the dropdown reference alongside the entries
        self.rows.append({
            "frame": row_frame,
            "dropdown": file_dropdown,
            "entry1": entry1,
            "entry2": entry2
        })

    def delete_row(self, frame_to_delete):
        self.rows = [row for row in self.rows if row["frame"] != frame_to_delete]
        frame_to_delete.destroy()

    def process_data(self):
        self.output_box.delete("0.0", "end")

        if not self.selected_files:
            self.output_box.insert("end", "Error: Please select at least one Excel file first.\n")
            return

        extracted_data = []

        for i, row in enumerate(self.rows):
            selected_target_file = row["dropdown"].get()
            val1 = row["entry1"].get()
            val2 = row["entry2"].get()

            if not val1 and not val2:
                continue

            try:
                # We now store a tuple of (Target File, Value 1, Value 2)
                extracted_data.append((selected_target_file, float(val1), float(val2)))
            except ValueError:
                self.output_box.insert("end", f"Error in Row {i+1}: Please enter valid numbers.\n")
                return

        if not extracted_data:
            self.output_box.insert("0.0", "Error: No valid manual data to process.\n")
            return

        self.output_box.insert("end", "Extraction Successful:\n")
        self.output_box.insert("end", "-" * 30 + "\n")

        # Display the mapping to prove it works
        for target, v1, v2 in extracted_data:
            self.output_box.insert("end", f"File: {target} | Vals: {v1}, {v2}\n")

if __name__ == "__main__":
    app = ExcelCruncherApp()
    app.mainloop()