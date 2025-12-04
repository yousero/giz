from copy import deepcopy
from datetime import datetime
from typing import Dict, Any, Optional


class File:
  def __init__(self, name: str, data: Any = None):
    self.name = name
    self.data = data

  def __repr__(self):
    return f"File('{self.name}', data={'<binary>' if self.data else None})"


class Text:
  def __init__(self, name: str, text: str = ''):
    self.name = name
    self.content = text

  def edit(self, text: str):
    self.content = text

  def __repr__(self):
    return f"Text('{self.name}', {self.content!r})"


class Commit:
  def __init__(self, message: str, files: Dict[str, Any], timestamp: Optional[datetime] = None):
    self.message = message
    self.files = deepcopy(files)
    self.timestamp = timestamp or datetime.now()
    self.id = timestamp.strftime("%Y%m%d-%H%M%S") if timestamp else datetime.now().strftime("%Y%m%d-%H%M%S")

  def __repr__(self):
    return f"Commit({self.id}, '{self.message}', {len(self.files)} files)"


class History:
  def __init__(self, name: str):
    self.name = name
    self.commits: list[Commit] = []

  def add(self, files: Dict[str, Any], message: str = "Auto commit"):
    commit = Commit(message, files)
    self.commits.append(commit)
    print(f"[{commit.timestamp.strftime('%H:%M:%S')}] Commit: {message} ({len(files)} files)")

  def list(self):
    if not self.commits:
      print("no commits")
      return
    print(f"Log «{self.name}»:")
    for c in self.commits:
      print(f"  {c.id} | {c.message} | {len(c.files)} files | {c.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")

  def checkout(self, commit_id: str):
    for c in reversed(self.commits):
      if c.id.startswith(commit_id):
        print(f"Переход на коммит {c.id} — {c.message}")
        return deepcopy(c.files)
    raise ValueError(f"Коммит с id '{commit_id}' не найден")


class Giz:
  def __init__(self, name: str):
    self.name = name
    self.history = History(name)
    self.current_files: Dict[str, Any] = {}

  def add_file(self, obj: Any):
    self.current_files[obj.name] = obj
    print(f"Added/edited: {obj.name}")

    def commit(self, message: str = "Quick save"):
      if not self.current_files:
        print("No files")
        return
      self.history.add(self.current_files, message)

    def status(self):
        print(f"Project: {self.name} | Files in work directory: {len(self.current_files)}")
        for f in self.current_files.values():
            print(f"  • {f}")

  def log(self):
    self.history.list()

  def checkout(self, commit_id: str):
    old_files = self.current_files.copy()
    try:
      self.current_files = self.history.checkout(commit_id)
      print("Checkout successful!")
    except ValueError:
      self.current_files = old_files
      raise

  def edit_text(self, filename: str, new_text: str):
    if filename not in self.current_files:
      raise FileNotFoundError(f"File {filename} not found")
    if not isinstance(self.current_files[filename], Text):
      raise TypeError(f"{filename} — not text file")
    self.current_files[filename].edit(new_text)
    print(f"Edited: {filename}")


if __name__ == '__main__':
  giz = Giz("my cool project")

  img = File("photo.jpg", b"<binary data>")
  txt = Text("readme.txt", "Hi, this is first version")

  giz.add_file(img)
  giz.add_file(txt)
  giz.commit("Initial commit")

  giz.status()

  giz.edit_text("readme.txt", "I have here new information.")
  giz.commit("update readme")

  txt2 = Text("notes.txt", "Notes")
  giz.add_file(txt2)
  giz.commit("add notes.txt")

  giz.log()

  giz.checkout("202")
  giz.status()
