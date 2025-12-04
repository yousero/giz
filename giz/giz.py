

class File:
  def __init__(self, name, data):
    self.name = name
    self.data = data


class Text:
  def __init__(self, name, text=''):
    self.name = name
    self.content = text

  def edit(self, text):
    self.content = text


class History:
  def __init__(self, name):
    self.name = name
    self.history = []
  
  def add(self, version):
    self.history.append(version)


class Giz:
  def __init__(self, name):
    self.name = name
  # todo: tracking files

if __name__ == '__main__':
  # todo: history process
  h = History('example')
  h.add({
    'file.jpg': File('image.jpg', None),
    'text.txt': Text('text.txt', 'new data')
  })
