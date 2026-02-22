import os
from PIL import Image
from pathlib import Path
import customtkinter as ctk
from tkinter import filedialog

import config
import processor

ctk.set_appearance_mode(config.ui_theme)
ctk.set_default_color_theme(config.color_theme)


class ExcelCruncherApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title(config.window_title)
        self.geometry(config.window_geometry)

        self.rows = []
        self.selected_files = []
        self.file_names = ['No files loaded']
        self.file_data = {}  # Maps 'filename.xlsx' -> ['Item 1', 'Item 2', ...]

        # --- Load the Icon (Modern Pathlib approach) ---
        try:
            light_icon_path = Path(config.assets_path) / config.excel_icon_name_light
            dark_icon_path = Path(config.assets_path) / config.excel_icon_name_dark

            self.excel_icon = ctk.CTkImage(
                light_image=Image.open(light_icon_path),
                dark_image=Image.open(dark_icon_path),
                size=(20, 20)
            )
        except FileNotFoundError:
            self.excel_icon = None

        # --- UI Layout ---

        self.title_label = ctk.CTkLabel(self, text='Data Entry Workflow', font=ctk.CTkFont(size=20, weight='bold'))
        self.title_label.pack(pady=(20, 10))

        # 1. The File Browser Section
        self.file_frame = ctk.CTkFrame(self, fg_color='transparent')
        self.file_frame.pack(pady=5, padx=20, fill='x')

        self.browse_btn = ctk.CTkButton(
            self.file_frame,
            text='📁 Click to Browse for Excel Files\n(You can select multiple files)',
            height=70,
            font=ctk.CTkFont(size=14),
            fg_color='#2b2b2b',
            hover_color='#3b3b3b',
            border_width=2,
            border_color='#555555',
            command=self.select_files
        )
        self.browse_btn.pack(fill='x', expand=True)

        self.attachment_frame = ctk.CTkScrollableFrame(self.file_frame, height=80, fg_color='#1e1e1e')
        self.attachment_frame.pack(fill='x', pady=(10, 0))

        self.empty_label = ctk.CTkLabel(self.attachment_frame, text='No files attached yet.', text_color='gray')
        self.empty_label.pack(pady=20)

        # 2. The Scrollable Frame (For manual data entry)
        self.scroll_frame = ctk.CTkScrollableFrame(self, height=250)
        self.scroll_frame.pack(pady=10, padx=20, fill='both', expand=True)

        self.add_btn = ctk.CTkButton(
            self,
            text='+ Add New Row',
            command=self.add_row,
            fg_color='#4a4a4a',
            hover_color='#5a5a5a',
        )
        self.add_btn.pack(pady=5)

        # 3. Action Button
        self.run_btn = ctk.CTkButton(
            self,
            text='Process Data',
            command=self.process_data,
            fg_color='green',
            hover_color='darkgreen',
            height=40,
        )
        self.run_btn.pack(pady=10)

        # 4. Output Text Box
        self.output_box = ctk.CTkTextbox(self, height=120)
        self.output_box.pack(pady=(0, 20), padx=20, fill='x')

        self.add_row()

    # --- File Management Functions ---
    def select_files(self):
        new_file_paths = filedialog.askopenfilenames(
            title='Select Excel Files',
            filetypes=[('Excel files', '*.xlsx *.xls')]
        )

        if new_file_paths:
            for path in new_file_paths:
                if path not in self.selected_files:
                    self.selected_files.append(path)

                    # Extract and cache the {name: price} dictionary
                    filename = os.path.basename(path)
                    extracted_dict = processor.extract_data_from_file(path)
                    self.file_data[filename] = extracted_dict

            self.update_file_state()

    def remove_file(self, file_path_to_remove):
        if file_path_to_remove in self.selected_files:
            self.selected_files.remove(file_path_to_remove)
            self.update_file_state()

    def update_file_state(self):
        if self.selected_files:
            self.file_names = [os.path.basename(f) for f in self.selected_files]
        else:
            self.file_names = ['No files loaded']

        for widget in self.attachment_frame.winfo_children():
            widget.destroy()

        if not self.selected_files:
            self.empty_label = ctk.CTkLabel(self.attachment_frame, text='No files attached yet.', text_color='gray')
            self.empty_label.pack(pady=20)
        else:
            for file_path in self.selected_files:
                filename = os.path.basename(file_path)

                item_frame = ctk.CTkFrame(self.attachment_frame, fg_color='#2b2b2b', corner_radius=5)
                item_frame.pack(fill='x', pady=2, padx=5)

                if self.excel_icon:
                    lbl = ctk.CTkLabel(
                        item_frame,
                        text=f'  {filename}',
                        image=self.excel_icon,
                        compound='left',
                        anchor='w',
                    )
                else:
                    lbl = ctk.CTkLabel(item_frame, text=f'📄 {filename}', anchor='w')

                lbl.pack(side='left', padx=10, pady=5)

                remove_btn = ctk.CTkButton(
                    item_frame,
                    text='Remove',
                    width=50,
                    height=24,
                    fg_color='#d9534f',
                    hover_color='#c9302c',
                    command=lambda f=file_path: self.remove_file(f)
                )
                remove_btn.pack(side='right', padx=10, pady=5)

        for row in self.rows:
            dropdown = row['dropdown']
            current_selection = dropdown.get()
            dropdown.configure(values=self.file_names)
            if current_selection not in self.file_names:
                dropdown.set(self.file_names[0])

    # --- Row Management Functions ---
    def add_row(self):
        row_frame = ctk.CTkFrame(self.scroll_frame, fg_color='transparent')
        row_frame.pack(fill='x', pady=5)

        # --- Helper: Auto-Calculate Total ---
        def update_total(*args):
            try:
                # Grab the current price and quantity
                price = float(price_entry.get())
                qty = float(qty_entry.get())
                total = price * qty

                # Update the Total cell
                total_entry.configure(state='normal')
                total_entry.delete(0, 'end')
                total_entry.insert(0, f'{total:.2f}')
                total_entry.configure(state='readonly')
            except ValueError:
                # If quantity is empty or invalid, clear the total
                total_entry.configure(state='normal')
                total_entry.delete(0, 'end')
                total_entry.configure(state='readonly')

        # --- CELL 1: Target File ---
        def on_target_file_changed(selected_filename):
            file_dict = self.file_data.get(selected_filename, {})
            available_names = list(file_dict.keys())

            name_combo.configure(values=available_names)
            name_combo.set('')

            price_entry.configure(state='normal')
            price_entry.delete(0, 'end')
            price_entry.configure(state='readonly')
            update_total()

        file_dropdown = ctk.CTkOptionMenu(
            row_frame, values=self.file_names, width=150,
            dynamic_resizing=False, command=on_target_file_changed
        )
        file_dropdown.pack(side='left', padx=(5, 5))

        # --- CELL 2: Searchable Name ---
        def on_name_selected(choice):
            # Find the price for the selected name
            selected_filename = file_dropdown.get()
            file_dict = self.file_data.get(selected_filename, {})
            price = file_dict.get(choice, 0.0)

            # Push the price to Cell 3
            price_entry.configure(state='normal')
            price_entry.delete(0, 'end')
            price_entry.insert(0, str(price))
            price_entry.configure(state='readonly')

            # Automatically calculate the total
            update_total()

        name_combo = ctk.CTkComboBox(row_frame, values=[''], width=150, command=on_name_selected)
        name_combo.pack(side='left', padx=5)

        def filter_names(event):
            typed_text = name_combo.get()
            selected_filename = file_dropdown.get()
            file_dict = self.file_data.get(selected_filename, {})
            all_names = list(file_dict.keys())

            if not typed_text:
                name_combo.configure(values=all_names)
            else:
                filtered = [n for n in all_names if typed_text.lower() in n.lower()]
                name_combo.configure(values=filtered)

        name_combo.bind('<KeyRelease>', filter_names)

        # --- CELL 3: Price (Read-Only) ---
        price_entry = ctk.CTkEntry(row_frame, width=80, state='readonly', text_color='gray')
        price_entry.pack(side='left', padx=5)

        # --- CELL 4: Quantity ---
        qty_entry = ctk.CTkEntry(row_frame, placeholder_text='Qty', width=60)
        qty_entry.pack(side='left', padx=5)
        # Bind typing in the quantity box to trigger the total calculation
        qty_entry.bind('<KeyRelease>', update_total)

        # --- CELL 5: Total (Read-Only) ---
        total_entry = ctk.CTkEntry(row_frame, width=90, state='readonly', text_color='lightgreen')
        total_entry.pack(side='left', padx=5)

        # --- Delete Button ---
        del_btn = ctk.CTkButton(
            row_frame, text='X', width=30, fg_color='#d9534f', hover_color='#c9302c',
            command=lambda f=row_frame: self.delete_row(f)
        )
        del_btn.pack(side='right', padx=10)

        # Store references
        self.rows.append({
            'frame': row_frame,
            'dropdown': file_dropdown,
            'name_combo': name_combo,
            'price': price_entry,
            'qty': qty_entry,
            'total': total_entry
        })

    def delete_row(self, frame_to_delete):
        self.rows = [row for row in self.rows if row['frame'] != frame_to_delete]
        frame_to_delete.destroy()

    # --- Processing Function ---
    def process_data(self):
        self.output_box.delete('0.0', 'end')

        if not self.selected_files:
            self.output_box.insert('end', 'Error: Please attach at least one Excel file first.\n')
            return

        extracted_data = []

        for i, row in enumerate(self.rows):
            selected_target_file = row['dropdown'].get()
            val1 = row['entry1'].get()
            val2 = row['entry2'].get()

            if not val1 and not val2:
                continue

            try:
                extracted_data.append((selected_target_file, float(val1), float(val2)))
            except ValueError:
                self.output_box.insert('end', f'Error in Row {i+1}: Please enter valid numbers.\n')
                return

        if not extracted_data:
            self.output_box.insert('0.0', 'Error: No valid manual data to process.\n')
            return

        # NEW: Hand off to processor.py
        try:
            self.output_box.insert('end', 'Processing...\n')

            # Call the pipeline and get the formatted result string
            final_output = processor.run_pipeline(extracted_data)

            # Print the results back to the UI
            self.output_box.delete('0.0', 'end')
            self.output_box.insert('end', final_output)

        except Exception as e:
            self.output_box.insert('end', f'\nCRITICAL ERROR: {e}')


if __name__ == '__main__':
    app = ExcelCruncherApp()
    app.mainloop()
