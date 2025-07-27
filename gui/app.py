import sys
import os
import tkinter as tk
from tkinter import messagebox, simpledialog, scrolledtext

# 添加项目根路径，确保模块能正确导入
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from core.notebook import Notebook
from storage.json_storage import JSONStorage
from security.encryption import Encryptor
from security.key_manager import KeyManager

DATA_FILE = "data/notes.json"
KEY_FILE = "key/secret.key"  # 注意你的目录叫 key，不是 keys

class NotebookApp:
    def __init__(self, root):
        self.root = root
        self.root.title("记事本 - GUI 加密版")
        self.root.geometry("700x500")

        self.encryptor = self.setup_encryptor()
        self.storage = JSONStorage(DATA_FILE)
        self.notebook = Notebook(self.encryptor)
        self.notebook.load_from_data(self.storage.load())

        self.text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=20)
        self.text_area.pack(pady=10)

        button_frame = tk.Frame(root)
        button_frame.pack()

        tk.Button(button_frame, text="添加笔记", command=self.add_note).grid(row=0, column=0, padx=10)
        tk.Button(button_frame, text="查看全部", command=self.view_notes).grid(row=0, column=1, padx=10)
        tk.Button(button_frame, text="搜索笔记", command=self.search_note).grid(row=0, column=2, padx=10)
        tk.Button(button_frame, text="删除笔记", command=self.delete_note).grid(row=0, column=3, padx=10)

    def setup_encryptor(self):
        os.makedirs("key", exist_ok=True)
        if not os.path.exists(KEY_FILE):
            encryptor = Encryptor()
            KeyManager.save_key(KEY_FILE, encryptor.get_key())
        else:
            key = KeyManager.load_key(KEY_FILE)
            encryptor = Encryptor(key)
        return encryptor

    def add_note(self):
        title = simpledialog.askstring("标题", "请输入笔记标题：")
        content = simpledialog.askstring("内容", "请输入笔记内容：")
        if title and content:
            self.notebook.add_note(title, content)
            self.storage.save(self.notebook.to_data())
            messagebox.showinfo("成功", "笔记已添加！")

    def view_notes(self):
        self.text_area.delete(1.0, tk.END)
        notes = self.notebook.get_all_notes()
        if not notes:
            self.text_area.insert(tk.END, "📭 没有任何笔记\n")
            return
        for note in notes:
            try:
                if note.encrypted:
                    content = self.encryptor.decrypt(note.content)
                else:
                    content = note.content
            except Exception as e:
                content = f"<解密失败: {e}>"
            self.text_area.insert(tk.END, f"\n📝 {note.title}\n{content}\n时间: {note.timestamp}\nID: {note.id}\n{'-'*60}\n")

    def search_note(self):
        keyword = simpledialog.askstring("搜索", "请输入关键词：")
        if keyword:
            results = self.notebook.search_notes(keyword)
            self.text_area.delete(1.0, tk.END)
            if not results:
                self.text_area.insert(tk.END, "🔍 未找到匹配的笔记\n")
                return
            for note in results:
                try:
                    if note.encrypted:
                        content = self.encryptor.decrypt(note.content)
                    else:
                        content = note.content
                except Exception as e:
                    content = f"<解密失败: {e}>"
                self.text_area.insert(tk.END, f"\n📝 {note.title}\n{content}\n时间: {note.timestamp}\nID: {note.id}\n{'-'*60}\n")

    def delete_note(self):
        note_id = simpledialog.askstring("删除", "请输入笔记ID：")
        if note_id:
            result = self.notebook.delete_note_by_id(note_id)
            if result:
                self.storage.save(self.notebook.to_data())
                messagebox.showinfo("成功", "笔记已删除")
            else:
                messagebox.showerror("错误", "未找到该笔记")

def run():
    root = tk.Tk()
    app = NotebookApp(root)
    root.mainloop()

if __name__ == "__main__":
    run()
