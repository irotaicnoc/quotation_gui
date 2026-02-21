import customtkinter as ctk
from tkinter import filedialog
import os

# 1. Set up the modern theme
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


class ExcelCruncherApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window configuration
        self.title("Data Transcription & Processing Tool")
        self.geometry("650x750")

        self.rows = []
        self.selected_files = []  # Store a list of multiple file paths

        # --- UI Layout ---

        # 1. Title Label
        self.title_label = ctk.CTkLabel(self, text="Data Entry Workflow", font=ctk.CTkFont(size=20, weight="bold"))
        self.title_label.pack(pady=(20, 10))

        # 2. The "Drop Zone" / File Browser
        self.file_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.file_frame.pack(pady=10, padx=20, fill="x")

        # We style this button to look like a modern drop zone (dashed borders
        # aren't native, so we use a thick border and distinct color)
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

        # Label to show what was selected
        self.file_label = ctk.CTkLabel(self.file_frame, text="No files selected", text_color="gray", justify="left")
        self.file_label.pack(pady=(5, 0), anchor="w")

        # 3. The Scrollable Frame (For manual data entry)
        self.scroll_frame = ctk.CTkScrollableFrame(self, height=250)
        self.scroll_frame.pack(pady=10, padx=20, fill="both", expand=True)

        # Add Row Button
        self.add_btn = ctk.CTkButton(
            self,
            text="+ Add New Row",
            command=self.add_row,
            fg_color="#4a4a4a",
            hover_color="#5a5a5a",
        )
        self.add_btn.pack(pady=5)

        # 4. Action Button (The "Crunch" trigger)
        self.run_btn = ctk.CTkButton(
            self,
            text="Process Data",
            command=self.process_data,
            fg_color="green",
            hover_color="darkgreen",
            height=40,
        )
        self.run_btn.pack(pady=10)

        # 5. Output Text Box
        self.output_box = ctk.CTkTextbox(self, height=120)
        self.output_box.pack(pady=(0, 20), padx=20, fill="x")

        # Automatically add the first row on startup
        self.add_row()

    # --- Event Functions ---

    def select_files(self):
        # askopenfilenames (plural) allows selecting multiple files
        file_paths = filedialog.askopenfilenames(
            title="Select Excel Files",
            filetypes=[("Excel files", "*.xlsx *.xls")]
        )

        if file_paths:
            self.selected_files = list(file_paths)

            # Update the label to show the user what they selected
            if len(self.selected_files) == 1:
                filename = os.path.basename(self.selected_files[0])
                self.file_label.configure(text=f"Selected: {filename}", text_color="white")
            else:
                self.file_label.configure(text=f"Selected {len(self.selected_files)} files.", text_color="white")

            # Optional: Print to output box for feedback
            self.output_box.insert("end", f"Loaded {len(self.selected_files)} files into queue.\n")

    def add_row(self):
        row_frame = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
        row_frame.pack(fill="x", pady=5)

        entry1 = ctk.CTkEntry(row_frame, placeholder_text="First Value", width=180)
        entry1.pack(side="left", padx=10)

        entry2 = ctk.CTkEntry(row_frame, placeholder_text="Second Value", width=180)
        entry2.pack(side="left", padx=10)

        del_btn = ctk.CTkButton(
            row_frame,
            text="X",
            width=30,
            fg_color="#d9534f",
            hover_color="#c9302c",
            command=lambda f=row_frame: self.delete_row(f)
        )
        del_btn.pack(side="right", padx=10)

        self.rows.append({"frame": row_frame, "entry1": entry1, "entry2": entry2})

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
            val1 = row["entry1"].get()
            val2 = row["entry2"].get()

            if not val1 and not val2:
                continue

            try:
                extracted_data.append((float(val1), float(val2)))
            except ValueError:
                self.output_box.insert("end", f"Error in Row {i+1}: Please enter valid numbers.\n")
                return

        if not extracted_data:
            self.output_box.insert("0.0", "Error: No valid manual data to process.\n")
            return

        self.output_box.insert(
            "end",
            f"Processing {len(self.selected_files)} files against {len(extracted_data)} manual rows...\n",
        )
        self.output_box.insert("end", "-" * 30 + "\n")

        # Example output to show it's working
        self.output_box.insert("end", "Done! (Placeholder for actual pandas logic)\n")


if __name__ == "__main__":
    app = ExcelCruncherApp()
    app.mainloop()
