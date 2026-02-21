import customtkinter as ctk
from tkinter import filedialog
import os
from PIL import Image

ctk.set_appearance_mode("System")
# ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")

class ExcelCruncherApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Data Transcription & Processing Tool")
        self.geometry("800x800") # Slightly taller to fit the attachments box

        self.rows = []
        self.selected_files = []
        self.file_names = ["No files loaded"]

        # --- Load the Icon ---
        try:
            # CTkImage handles High-DPI scaling automatically
            self.excel_icon = ctk.CTkImage(
                light_image=Image.open("images/excel_icon_light_2.png"),
                dark_image=Image.open("images/excel_icon_light_2.png"),
                size=(20, 20) # Forces the icon to a standard size
            )
        except FileNotFoundError:
            # Fallback if you haven't downloaded the image yet
            self.excel_icon = None

        # --- UI Layout ---

        self.title_label = ctk.CTkLabel(self, text="Data Entry Workflow", font=ctk.CTkFont(size=20, weight="bold"))
        self.title_label.pack(pady=(20, 10))

        # 1. The File Browser Section
        self.file_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.file_frame.pack(pady=5, padx=20, fill="x")

        self.browse_btn = ctk.CTkButton(
            self.file_frame,
            text="📁 Click to Browse for Excel Files\n(You can select multiple files)",
            height=70,
            font=ctk.CTkFont(size=14),
            fg_color="#2b2b2b",
            hover_color="#3b3b3b",
            border_width=2,
            border_color="#555555",
            command=self.select_files
        )
        self.browse_btn.pack(fill="x", expand=True)

        # NEW: The Attachment List (Scrollable frame for files)
        self.attachment_frame = ctk.CTkScrollableFrame(self.file_frame, height=80, fg_color="#1e1e1e")
        self.attachment_frame.pack(fill="x", pady=(10, 0))

        # Placeholder text when empty
        self.empty_label = ctk.CTkLabel(self.attachment_frame, text="No files attached yet.", text_color="gray")
        self.empty_label.pack(pady=20)

        # 2. The Scrollable Frame (For manual data entry)
        self.scroll_frame = ctk.CTkScrollableFrame(self, height=250)
        self.scroll_frame.pack(pady=10, padx=20, fill="both", expand=True)

        self.add_btn = ctk.CTkButton(self, text="+ Add New Row", command=self.add_row, fg_color="#4a4a4a", hover_color="#5a5a5a")
        self.add_btn.pack(pady=5)

        # 3. Action Button
        self.run_btn = ctk.CTkButton(self, text="Process Data", command=self.process_data, fg_color="green", hover_color="darkgreen", height=40)
        self.run_btn.pack(pady=10)

        # 4. Output Text Box
        self.output_box = ctk.CTkTextbox(self, height=120)
        self.output_box.pack(pady=(0, 20), padx=20, fill="x")

        self.add_row()

    # --- File Management Functions ---

    def select_files(self):
        new_file_paths = filedialog.askopenfilenames(
            title="Select Excel Files",
            filetypes=[("Excel files", "*.xlsx *.xls")]
        )

        if new_file_paths:
            # Append only new files to prevent duplicates
            for path in new_file_paths:
                if path not in self.selected_files:
                    self.selected_files.append(path)

            self.update_file_state()

    def remove_file(self, file_path_to_remove):
        if file_path_to_remove in self.selected_files:
            self.selected_files.remove(file_path_to_remove)
            self.update_file_state()

    def update_file_state(self):
        # 1. Update our internal list of base names
        if self.selected_files:
            self.file_names = [os.path.basename(f) for f in self.selected_files]
        else:
            self.file_names = ["No files loaded"]

        # 2. Redraw the attachment UI
        # First, destroy everything currently in the attachment frame
        for widget in self.attachment_frame.winfo_children():
            widget.destroy()

        if not self.selected_files:
            self.empty_label = ctk.CTkLabel(self.attachment_frame, text="No files attached yet.", text_color="gray")
            self.empty_label.pack(pady=20)
        else:
            # Rebuild the list of attachments
            for file_path in self.selected_files:
                filename = os.path.basename(file_path)

                # A mini-container for each file
                item_frame = ctk.CTkFrame(self.attachment_frame, fg_color="#2b2b2b", corner_radius=5)
                item_frame.pack(fill="x", pady=2, padx=5)

                # --- Apply the Icon ---
                if self.excel_icon:
                    lbl = ctk.CTkLabel(item_frame, text=f"  {filename}", image=self.excel_icon, compound="left", anchor="w")
                else:
                    # Fallback if image isn't found
                    lbl = ctk.CTkLabel(item_frame, text=f"📄 {filename}", anchor="w")

                lbl.pack(side="left", padx=10, pady=5)

                # The 'Remove' button for this specific file
                remove_btn = ctk.CTkButton(
                    item_frame, text="Remove", width=50, height=24,
                    fg_color="#d9534f", hover_color="#c9302c",
                    command=lambda f=file_path: self.remove_file(f)
                )
                remove_btn.pack(side="right", padx=10, pady=5)

        # 3. Synchronize all dropdowns in the manual entry rows
        for row in self.rows:
            dropdown = row["dropdown"]
            current_selection = dropdown.get()

            # Update the available options
            dropdown.configure(values=self.file_names)

            # If the currently selected file was deleted, default back to the first available option
            if current_selection not in self.file_names:
                dropdown.set(self.file_names[0])


    # --- Row Management Functions ---

    def add_row(self):
        row_frame = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
        row_frame.pack(fill="x", pady=5)

        file_dropdown = ctk.CTkOptionMenu(row_frame, values=self.file_names, width=200, dynamic_resizing=False)
        file_dropdown.pack(side="left", padx=(10, 5))

        entry1 = ctk.CTkEntry(row_frame, placeholder_text="First Value", width=140)
        entry1.pack(side="left", padx=5)

        entry2 = ctk.CTkEntry(row_frame, placeholder_text="Second Value", width=140)
        entry2.pack(side="left", padx=5)

        del_btn = ctk.CTkButton(
            row_frame, text="X", width=30, fg_color="#d9534f", hover_color="#c9302c",
            command=lambda f=row_frame: self.delete_row(f)
        )
        del_btn.pack(side="right", padx=10)

        self.rows.append({
            "frame": row_frame,
            "dropdown": file_dropdown,
            "entry1": entry1,
            "entry2": entry2
        })

    def delete_row(self, frame_to_delete):
        self.rows = [row for row in self.rows if row["frame"] != frame_to_delete]
        frame_to_delete.destroy()


    # --- Processing Function ---

    def process_data(self):
        self.output_box.delete("0.0", "end")

        if not self.selected_files:
            self.output_box.insert("end", "Error: Please attach at least one Excel file first.\n")
            return

        extracted_data = []

        for i, row in enumerate(self.rows):
            selected_target_file = row["dropdown"].get()
            val1 = row["entry1"].get()
            val2 = row["entry2"].get()

            if not val1 and not val2:
                continue

            try:
                extracted_data.append((selected_target_file, float(val1), float(val2)))
            except ValueError:
                self.output_box.insert("end", f"Error in Row {i+1}: Please enter valid numbers.\n")
                return

        if not extracted_data:
            self.output_box.insert("0.0", "Error: No valid manual data to process.\n")
            return

        self.output_box.insert("end", "Extraction Successful:\n")
        self.output_box.insert("end", "-" * 30 + "\n")

        for target, v1, v2 in extracted_data:
            self.output_box.insert("end", f"File: {target} | Vals: {v1}, {v2}\n")

if __name__ == "__main__":
    app = ExcelCruncherApp()
    app.mainloop()