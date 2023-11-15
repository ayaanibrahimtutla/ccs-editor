import tkinter as tk
import os
from tkinter import filedialog, messagebox,PhotoImage
from threading import Thread
import time

class CCS_TextEditor:
    def __init__(self, root):
        try:
            self.root = root
            self.root.title("CCS Text Editor")




            bg_color = "#2E2E2E"
            fg_color = "white"
            menu_bg_color = "#3A3A3A"
            menu_fg_color = "white"

            self.root.configure(bg=bg_color)

            self.text_widget = tk.Text(root, wrap='word', undo=True, bg=bg_color, fg=fg_color)
            self.text_widget.pack(expand="yes", fill="both")

            self.menu_bar = tk.Menu(root, bg=menu_bg_color, fg=menu_fg_color)
            
            file_menu = tk.Menu(self.menu_bar, tearoff=0, bg=menu_bg_color, fg=menu_fg_color)
            file_menu.add_command(label="Save", command=self.save_file)
            file_menu.add_command(label="Save As", command=self.save_as_file)
            file_menu.add_command(label="Open", command=self.open_file)
            self.menu_bar.add_cascade(label="File", menu=file_menu)


            edit_menu = tk.Menu(self.menu_bar, tearoff=0, bg=menu_bg_color, fg=menu_fg_color)
            edit_menu.add_command(label="Cut", command=self.cut_text)
            edit_menu.add_command(label="Copy", command=self.copy_text)
            edit_menu.add_command(label="Paste", command=self.paste_text)
            self.menu_bar.add_cascade(label="Edit", menu=edit_menu)


            #run_menu = tk.Menu(self.menu_bar, tearoff=0, bg=menu_bg_color, fg=menu_fg_color)
            #run_menu.add_command(label="Run in Minecraft", command=self.run_in_minecraft)
            #self.menu_bar.add_cascade(label="Run", menu=run_menu)


            self.keyword_colors = self.configure_keyword_highlighting()


            self.text_widget.bind("<KeyRelease>", self.highlight_keywords)


            root.config(menu=self.menu_bar)
        except Exception as e:
            print(e)
            messagebox.showerror("BUILD ERROR", "You haven't build the file properly please refer to (ERROR:1) https://github.com/ayaanibrahimtutla/ccs-editor")

    def configure_keyword_highlighting(self):

        self.text_widget.tag_configure("string_highlight", foreground="green")
        self.text_widget.tag_configure("number_highlight", foreground="pink")

        keyword_colors = {
            "yellow": ["exit", "print", "throw", "execute", "loop", "module", "description", "on", "switch",
                       "say", "input", "wait", "if", "if_not", "send", "swap", "turn_to", "loop_period"],
            "red": ["left_click", "right_click", "middle_click", "left_release", "right_release", "middle_release",
                    "break_block", "place_block", "interact_block", "punch_block", "tick", "item_use", "item_consume",
                    "totem_pop", "module_enable", "module_disable", "move_pos", "move_look", "key_press", "key_release",
                    "damage", "death"],
            "orange": ["inventory_has", "hotbar_has", "target_block", "target_entity", "holding", "block_in_range",
                       "entity_in_range", "off_holding", "input_active", "attack_progress", "armor", "health", "pos_x",
                       "pos_y", "pos_z"],
            "purple": ["custom-module", "new-module", "description"]
        }

        for color, keywords in keyword_colors.items():
            for keyword in keywords:
                self.text_widget.tag_configure(f"{keyword}_highlight", foreground=color)

        return keyword_colors

    def save_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".ccs", filetypes=[("CCS files", "*.ccs"), ("All files", "*.*")])
        if file_path:
            with open(file_path, "w") as file:
                file.write(self.text_widget.get("1.0", tk.END))
            messagebox.showinfo("Saved", "File saved successfully!")

    def save_as_file(self):
        default_dir = os.path.expanduser(os.path.join("~", ".minecraft", "ClickCrystalsClient", "scripts"))
        file_path = filedialog.asksaveasfilename(defaultextension=".ccs", initialdir=default_dir, filetypes=[("CCS files", "*.ccs"), ("All files", "*.*")])

        if file_path:

            if not os.path.exists(file_path):
                messagebox.showerror("Install CC","Install: (ERROR:2) https://modrinth.com/mod/clickcrystals")
            script_dir = os.path.dirname(file_path)
            if not os.path.exists(script_dir):
                    messagebox.showerror("Update CC", "Update ClickCrystals! (ERROR:3) (Version 1.1.0 Reccomended)")
                    return
                    return


            with open(file_path, "w") as file:
                file.write(self.text_widget.get("1.0", tk.END))

            messagebox.showinfo("Saved", "File saved successfully!")

    def cut_text(self):
        self.text_widget.event_generate("<<Cut>>")

    def copy_text(self):
        self.text_widget.event_generate("<<Copy>>")

    def paste_text(self):
        self.text_widget.event_generate("<<Paste>>")
    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("CCS files", "*.ccs"), ("All files", "*.*")])
        if file_path:
            with open(file_path, "r") as file:
                content = file.read()
                self.text_widget.delete("1.0", tk.END)
                self.text_widget.insert("1.0", content)

    def run_in_minecraft(self):
        messagebox.showinfo("Run", "Running in Minecraft (Not implemented)")
        print("bro really tried getting 500 girlfriends an hour")
        

    def highlight_keywords(self, event):
        for color, keywords in self.keyword_colors.items():
            for keyword in keywords:
                self.highlight_keyword(keyword, color)

    def highlight_keyword(self, keyword, color):
        self.text_widget.tag_remove(f"{keyword}_highlight", "1.0", tk.END)

        content = self.text_widget.get("1.0", tk.END)
        start_index = "1.0"
        while True:
            start_index = self.text_widget.search(keyword, start_index, tk.END, nocase=1)
            if not start_index:
                break
            end_index = f"{start_index}+{len(keyword)}c"
            self.text_widget.tag_add(f"{keyword}_highlight", start_index, end_index)
            start_index = end_index

if __name__ == "__main__":
    root = tk.Tk()
    editor = CCS_TextEditor(root)
    root.mainloop()
