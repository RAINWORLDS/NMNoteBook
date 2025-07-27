from .note import Note

class Notebook:
    def __init__(self, encryptor=None):
        self.notes = []
        self.encryptor = encryptor

    def add_note(self, title, content):
        if self.encryptor:
            encrypted_content = self.encryptor.encrypt(content)
            note = Note(title, encrypted_content, encrypted=True)
        else:
            note = Note(title, content, encrypted=False)
        self.notes.append(note)

    def get_all_notes(self):
        return self.notes

    def search_notes(self, keyword):
        results = []
        for note in self.notes:
            if keyword.lower() in note.title.lower():
                results.append(note)
                continue
            content = note.content
            if note.encrypted and self.encryptor:
                try:
                    content = self.encryptor.decrypt(note.content)
                except:
                    pass
            if keyword.lower() in content.lower():
                results.append(note)
        return results

    def delete_note_by_id(self, note_id):
        for i, note in enumerate(self.notes):
            if note.id == note_id:
                del self.notes[i]
                return True
        return False

    def to_data(self):
        return [note.to_dict() for note in self.notes]

    def load_from_data(self, data_list):
        self.notes = [Note.from_dict(d) for d in data_list]
