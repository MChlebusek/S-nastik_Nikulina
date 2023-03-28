import random
from re import I
from tkinter import*   
from tkinter import messagebox

import tkinter as tk  



# Определите пути к текстовым файлам, содержащим слова
EST_FILE = "est.txt"
RUS_FILE = "rus.txt" 



idioms={}
# слова транзакции вызова функции. Принимает слова в качестве аргумента и возвращает перевод
# на другом языке. Работает, открывая два файла
# Он одновременно читает слово из обоих файлов, используя zip()
# и сравнивает каждое слово с даннным словомю Если совпадение найдено, возвращается
# соответствующее слово из другого файла.
def translate_idiom(idiom):
    with open(EST_FILE, 'r', encoding='utf-8') as est:
        with open(RUS_FILE, 'r', encoding='utf-8') as rus:
            for est_line, rus_line in zip(est, rus):
                if est_line.strip() == idiom:
                    return rus_line.strip()
                elif rus_line.strip() == idiom:
                    return est_line.strip()
    return "Sõna ei leitud"

# Создадим функцию для кнопки
def on_translate():
    idiom = entry.get().strip()
    translation = translate_idiom(idiom)
    result_label.config(text=translation)

root = Tk()
root.geometry('200x600')
root.title("Eesti-VEne sõnastik")

# Создайте поле ввода
entry = Entry(root)
entry.pack()

# Создайте кнопку перевода
translate_button = Button(root, text="Tõlgi",bg='#f7ee97', command=on_translate)
translate_button.pack()

# Создайте метку для результата перевода
result_label = Label(root, text="", font='Italic 15')
result_label.pack() 

results_label = tk.Label(root, text="", font='Italic 15')
results_label.pack()

# Создайте метку для записи добавления
add_label = tk.Label(root, text="Lisage uus idioom:")
add_label.pack()
# Создайте поля ввода для эстонских и русских слов
est_lbl = tk.Label(root, text="Est",bg='#8aeb8d', padx=5, pady=5)
est_lbl.pack(padx=10, pady=5, fill="both")
est_entry = Entry(root)
est_entry.pack()
rus_lbl = tk.Label(root, text="Rus",bg='#8aeb8d', padx=5, pady=5)
rus_lbl.pack(padx=10, pady=5, fill="both")
rus_entry = Entry(root)
rus_entry.pack()
# Определите функцию для обработки добавления нового слова
def add_idiom():
    # Получить новые слова из записей
    new_est_idiom = est_entry.get().strip()
    new_rus_idiom = rus_entry.get().strip()

    #Добавьте новые слова в словарь и текстовые файлы
    if new_est_idiom and new_rus_idiom:
        idioms[new_est_idiom.lower()] = new_rus_idiom.lower()
        with open(EST_FILE, "a", encoding="utf-8-sig") as f_eng, open(RUS_FILE, "a", encoding="utf-8-sig") as f_rus:
            f_eng.write(new_est_idiom.lower() + "\n")
            f_rus.write(new_rus_idiom.lower() + "\n")

        # Очистите записи и покажите сообщение об успешном завершении
        est_entry.delete(0, tk.END)
        rus_entry.delete(0, tk.END)
        results_label.config(text="Sõna lisamine õnnestus!")
    else:
        results_label.config(text="Lisamiseks sisestage sõna mõlemas keeles.")
        
def quiz():
    with open('est.txt', encoding='utf-8-sig') as f:
        est = [line.strip() for line in f.readlines()]
    with open('rus.txt', encoding='utf-8-sig') as f:
        rus = [line.strip() for line in f.readlines()]
    words = dict(zip(est, rus))
    random_idioms = random.sample(est, 4)
    score = 0

    def check_answer(entry, word):
        nonlocal score
        answer = entry.get().strip()
        expected_answer = words[word]
        if answer == expected_answer:
            result_lbl=tk.Label(root, text='Õige!', fg='Green', font='Times 25')
            result_lbl.pack(side='bottom')
            
            score += 1
        else:
            result_lbl1=tk.Label(root, text='Vale!',fg='Red',font='Cmabria 25')
            result_lbl1.pack(side='bottom')
        messagebox.showinfo("Oodatud vastus:",f" {expected_answer}")
        print(f"Your answer: {answer}")
        if len(random_idioms) > 0:
            ask_question()
        else:
            print(f'Sa lõid värava {score}')
    
    def ask_question():
        word = random_idioms.pop()
        label = Label(root, text=f'Mis on sõna "{word}" vene keeles?: ')
        label.pack()
        entry = Entry(root)
        entry.pack()
        button = Button(root, text='Esita', command=lambda: check_answer(entry, word))
        button.pack()
        
    for i, idiom in enumerate(random_idioms): 
        ask_question()

add_button = tk.Button(root, text="Lisama",bg='#f7ee97', command=add_idiom)
add_button.pack()
quiz_button = Button(root, text='Alusta viktoriini',bg='#f7ee97', command=quiz)
quiz_button.pack()

root.mainloop()
