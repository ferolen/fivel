from random import choice
import tkinter as tk

wnd = tk.Tk()

grid_size = 64
border = 5
field_width = 5 * grid_size + 8 * border
abc_size = (field_width - border) // 11
field_height = 4 * grid_size + 8 * border + 3 * abc_size
abc = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'

wnd.geometry(f'{field_width}x{field_height}')

def openfromvoc(filename):
  voc = list(open(filename, 'r', encoding = 'utf-8'))
  wordes = dict()
  for s in voc:
    s = s.split()
    wordes[s[0]] = int(s[1])
  return(wordes)
#print(wordes['слово'])

def save2voc(wordes,filename):
  with open(filename, 'w', encoding = 'utf-8') as f:
    for s in wordes:
      f.write(f'{s} {wordes[s]}\n')

def start_game():
  global guessed
  if btn_start['text'] == 'новая':
    gulist = []
    for s in wordes:
      if wordes[s] > 1:
        gulist.append(s)
    guessed = choice(list(gulist))
    for i in range(5):
      word[i]['text'] = '*'
    btn_start['text'] = 'сдаюсь'
    btn_dk['state'] = 'normal'
    word_entry['state'] = 'normal'
    word_entry.delete(0, tk.END)
    for i in range(33):
      abc_wnd[i]['bg'] = 'white'
  else:
    console['text'] = f'было загадано\nслово "{guessed}"'
    btn_start['text'] = 'новая'
    btn_dk['state'] = 'disable'
    word_entry.delete(0, tk.END)
    word_entry['state'] = 'disable'
    for i in range(5):
      word[i]['text'] = guessed[i].upper()
      word[i]['bg'] = 'teal'
    with open('voc.txt', 'w', encoding = 'utf-8') as f:
      for c in wordes:
        f.write(f'{c} {wordes[c]}\n')

def go(event):
  check()

def check():
  global wordes
  w = word_entry.get()
  if len(w) != 5:
    console['text'] = 'в слове не 5 букв'
  elif w == guessed:
    console['text'] = 'отгадал!'
    btn_start['text'] = 'новая'
    btn_dk['state'] = 'disable'
    word_entry.delete(0, tk.END)
    word_entry['state'] = 'disable'
    for i in range(5):
      word[i]['text'] = w[i].upper()
      word[i]['bg'] = 'teal'
    with open('voc.txt', 'w', encoding = 'utf-8') as f:
      for c in wordes:
        f.write(f'{c} {wordes[c]}\n')
  elif w in wordes:
    console['text'] = f''
    for i in range(5):
      abc_num = abc.find(w[i])
      if w[i] == guessed[i]:
        word[i]['bg'] = 'teal'
        abc_wnd[abc_num]['bg'] = 'teal'
      elif w[i] in guessed:
        word[i]['bg'] = 'olive'
        abc_wnd[abc_num]['bg'] = 'teal'
      else:
        word[i]['bg'] = 'gray'
        abc_wnd[abc_num]['bg'] = 'gray'
      word[i]['text'] = w[i].upper()
    wordes[w] += 1
  else:
    console['text'] = f'"{w}" нет в словаре'
    with open('new.txt', 'a', encoding = 'utf-8') as f:
      f.write(f'{w} 1\n')
  word_entry.delete(0, tk.END)
  
word = []
#guessed = choice(list(wordes.keys()))
wordes = openfromvoc('voc.txt')
guessed = '*****'

for i in range(5):
  word.append(tk.Label(text = guessed[i].upper(),font=f"Courier {int(grid_size//2)}",bg = 'silver'))
  word[i].place(x = 2 * border + i * (grid_size + border),
                y = 2 * border, width = grid_size, height = grid_size)
word_entry = tk.Entry(font=f"Courier {int(grid_size/1.5)}", justify = 'center')
word_entry['state'] = 'disable'
word_entry.place(x = 2 * border, y = 3 * border + grid_size,
                 width = 5 * grid_size + 4 * border,
                 height = grid_size)
half_width = (field_width - 5 * border)//2
btn_start = tk.Button(text = 'новая', font=f"Courier {int(grid_size/2)}",
                      command = start_game)
btn_start.place(x = 2 * border, y = 4 * border + 2 * grid_size,
                 width = half_width,
                 height = grid_size)

btn_dk = tk.Button(text = 'ввести', font=f"Courier {int(grid_size/2)}",
                   command = check)
btn_dk['state'] = 'disable'
btn_dk.place(x = 3 * border + half_width, y = 4 * border + 2 * grid_size,
                 width = half_width,
                 height = grid_size)

console = tk.Label(text = 'для начала игры\nнажмите "новая"', font=f"Courier {int(grid_size/4)}",
                   fg = 'red')
console.place(x = 2 * border, y = 5 * border + 3 * grid_size,
                 width = field_width,
                 height = grid_size)

word_entry.bind('<Return>', go)
abc_wnd = []
abc_left = (field_width - 11 * abc_size)//2
for i in range(33):
  abc_wnd.append(tk.Label(text = abc[i].upper(),
                          font=f"Courier {int(abc_size/2)}",
                          bg = 'white'))
  abc_wnd[i].place(x = abc_left + (i % 11) * abc_size,
                   y = 6 * border + 4 * grid_size + abc_size * (i // 11),
                   width = abc_size,
                   height = abc_size)
wnd.mainloop()
