import os
import threading
from PIL import Image
from pathlib import Path
import customtkinter as ctk
from tkinter import filedialog
from CTkScrollableDropdown import CTkScrollableDropdown

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
            text='📁 Browse for Excel Files',
            height=40,
            font=ctk.CTkFont(size=14),
            fg_color='#2b2b2b',
            hover_color='#3b3b3b',
            border_width=2,
            border_color='#555555',
            command=self.select_files
        )
        self.browse_btn.pack(fill='x', pady=5)

        # Progress bar (Hidden by default, shown during loading)
        self.progress_bar = ctk.CTkProgressBar(self.file_frame, mode='determinate')
        self.progress_bar.set(0)

        self.attachment_frame = ctk.CTkScrollableFrame(self.file_frame, height=80, fg_color='#1e1e1e')
        self.attachment_frame.pack(fill='x', pady=(10, 0))

        self.empty_label = ctk.CTkLabel(self.attachment_frame, text='No files attached yet.', text_color='gray')
        self.empty_label.pack(pady=20)

        # 2. The Scrollable Frame (For manual data entry)
        self.scroll_frame = ctk.CTkScrollableFrame(self, height=250)
        self.scroll_frame.pack(pady=10, padx=20, fill='both', expand=True)

        # Changed parent to scroll_frame. We don't pack it here, add_row will handle packing.
        self.add_btn = ctk.CTkButton(
            self.scroll_frame,
            text='+ Add New Row',
            command=self.add_row,
            fg_color='#4a4a4a',
            hover_color='#5a5a5a',
        )

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
            # Filter out files that are already loaded
            files_to_load = [path for path in new_file_paths if path not in self.selected_files]

            if not files_to_load:
                return

            # Disable the button and show the progress bar
            self.browse_btn.configure(state='disabled', text='⏳ Loading Files...')
            self.progress_bar.pack(fill='x', pady=(0, 5))
            self.progress_bar.set(0)

            # Run extraction in a separate thread to prevent GUI freezing
            threading.Thread(target=self._load_files_thread, args=(files_to_load,), daemon=True).start()

    def _load_files_thread(self, files_to_load):
        total_files = len(files_to_load)

        for i, path in enumerate(files_to_load):
            filename = os.path.basename(path)
            # Extract data from the file (This is the blocking operation)
            extracted_dict = processor.extract_data_from_file(path)

            self.selected_files.append(path)
            self.file_data[filename] = extracted_dict

            # Update the progress bar safely from the background thread
            progress = (i + 1) / total_files
            self.after(0, self._update_progress, progress)

        # Re-enable UI once loading is finished
        self.after(0, self._on_files_loaded)

    def _update_progress(self, value):
        self.progress_bar.set(value)

    def _on_files_loaded(self):
        # Hide the progress bar, restore the button, and refresh the UI state
        self.progress_bar.pack_forget()
        self.browse_btn.configure(state='normal', text='📁 Browse for Excel Files')
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
        # Temporarily hide the add button so the new row is placed above it
        if hasattr(self, 'add_btn'):
            self.add_btn.pack_forget()

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

            if not available_names:
                available_names = ['']

            # Update the custom dropdown attached to the combobox
            name_dropdown.configure(values=available_names)

            # Clear out the combobox text when switching files
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
            # 1. Visually update the text in the combobox
            name_combo.set(choice)

            # 2. Find the price for the selected name
            selected_filename = file_dropdown.get()
            file_dict = self.file_data.get(selected_filename, {})
            price = file_dict.get(choice, 0.0)

            # 3. Push the price to Cell 3
            price_entry.configure(state='normal')
            price_entry.delete(0, 'end')
            price_entry.insert(0, str(price))
            price_entry.configure(state='readonly')

            # 4. Automatically calculate the total
            update_total()

        # Switch back to CTkComboBox for better Click & Type behavior
        name_combo = ctk.CTkComboBox(row_frame, width=150)
        name_combo.pack(side='left', padx=5)

        # Attach the autocomplete scrollable dropdown directly to the combobox
        name_dropdown = CTkScrollableDropdown(
            name_combo,
            values=[''],
            command=on_name_selected,
            autocomplete=True  # Automatically handles the filtering logic
        )

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
            'name_dropdown': name_dropdown,
            'price': price_entry,
            'qty': qty_entry,
            'total': total_entry
        })

        # Repack the add button so it consistently appears below the newest row
        if hasattr(self, 'add_btn'):
            self.add_btn.pack(pady=(10, 5))

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

            val1 = row['price'].get()
            val2 = row['qty'].get()

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

        # Hand off to processor.py
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