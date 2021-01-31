from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter.ttk import Treeview
# -*- coding: utf-8 -*-
import mysql.connector
from tkinter import messagebox
from smsapi.client import SmsApiPlClient
from smsapi.exception import SmsApiException
import os

#połączenie z MySQL
mydb = mysql.connector.connect(host="localhost", user="root", passwd="Savakiran03", database="bazasm")
cursor = mydb.cursor()

#definicje funkcji
options=[]
sql = "SELECT idTresc, naglowekTresc, tekstTresc FROM tresc"
cursor.execute(sql)
ids = cursor.fetchall()
for i in ids:
    options.append(str(i[0])+" - " +i[1])

def chooseText(event):
    option = mycombo.get()
    cid = option.split(" - ")[0]
    query = "SELECT * FROM tresc WHERE idTresc = %s"
    cursor.execute(query, (cid,))
    rows = cursor.fetchall()
    for i in rows:
        idTresc.set(i[0])
        naglowekTresc.set(i[1])
        # tekstTresc.set(i[2])
        ent7.insert(1.0, i[2])

def getrow(event):
    rowid = trv.identify_row(event.y)
    item = trv.item(trv.focus())
    t1.set(item['values'][0])
    t2.set(item['values'][1])
    t3.set(item['values'][2])
    t4.set(item['values'][3])
    t5.set(item['values'][4])
    t6.set(item['values'][5])
    t8.set(item['values'][6])

def update(rows):
    trv.delete(*trv.get_children())
    for i in rows:
        trv.insert('', 'end', values=i)

def clear():
    query = "SELECT idBudynek, SymbolBudynku, SymbolOsiedla, KodPocztowy, Ulica, SymbolNieruchomosci FROM blok"
    cursor.execute(query)
    rows = cursor.fetchall()
    update(rows)
    ent1.delete(0, END)
    ent2.delete(0, END)
    ent3.delete(0, END)
    ent4.delete(0, END)
    ent5.delete(0, END)
    ent6.delete(0, END)
    ent8.delete(0, END)
    entSearch.delete(0, END)

def clearText():
    ent7.delete("1.0", END)

def search():
    try:
        q2 = str(q.get())
        query = "SELECT idBudynek, SymbolBudynku, SymbolOsiedla, KodPocztowy, Ulica, SymbolNieruchomosci, Numery FROM blok WHERE SymbolBudynku LIKE '%"+q2+"%' "
        cursor.execute(query)
        rows = cursor.fetchall()
        update(rows)
    except TclError:
        messagebox.showerror("Uwaga", "Musisz podać 4 cyfry")

def sendSMS():
    try:
        result = ent7.get("1.0", "end")
        ent8.info = str(ent8.get())
        token = "rM5DsJlOvDkbGnYnHAn9f9GmpphT0ovOywqPaiLL"
        client = SmsApiPlClient(access_token=token)
        send_results = client.sms.send(to=ent8.info, message=result, from_="SMBUDOWLANI")
        for result in send_results:
            print(result.id, result.points, result.error)
    except SmsApiException:
        messagebox.showerror("Uwaga", "Wypełnij pole Telefony aby wysłać wiadomość")

root = Tk()

q = IntVar()
t1 = StringVar()
t2 = StringVar()
t3 = StringVar()
t4 = StringVar()
t5 = StringVar()
t6 = StringVar()
t7 = StringVar()
t8 = StringVar()
opts=StringVar()
idTresc = StringVar()
naglowekTresc = StringVar()
tekstTresc = StringVar()

#okna główne
window1 = LabelFrame(root, text="Blok",font=("bold", 12))
window2 = LabelFrame(root, text="Szukaj",font=("bold", 12))
window3 = LabelFrame(root, text="Szczegóły",font=("bold", 12))

window1.pack(fill="both", expand="yes", padx=20, pady=10)
window2.pack(fill="both", expand="yes", padx=20, pady=10)
window3.pack(fill="both", expand="yes", padx=20, pady=10)

#sekcja wyświetl wszystko w 1 oknie
trv = Treeview(window1, columns=(1,2,3,4,5,6), show="headings", height="10")
trv.pack()
#trv.pack(side=RIGHT)
# trv.place(x=0, y=0)
trv.heading(1, text= "ID Budynek")
trv.heading(2, text= "Symbol Budynku")
trv.heading(3, text= "Symbol Osiedla")
trv.heading(4, text= "Kod Pocztowy")
trv.heading(5, text= "Ulica")
trv.heading(6, text= "Symbol Nieruchomości")
trv.bind('<Double 1>', getrow)

#Scrollbary
# yscrollbar = ttk.Scrollbar(window1, orient="vertical", command = trv.yview)
# yscrollbar.pack(side=RIGHT, fill="y")

query = "SELECT idBudynek, SymbolBudynku, SymbolOsiedla, KodPocztowy, Ulica, SymbolNieruchomosci, Numery FROM blok"
cursor.execute(query)
rows = cursor.fetchall()

#sekcja szukaj
lblSearch = Label(window2, text="Szukaj",font=("bold", 12))
lblSearch.pack(side=tk.LEFT, padx=10)
entSearch = Entry(window2, textvariable=q,font=("bold", 12))
entSearch.pack(side=tk.LEFT, padx=6)
entSearch.delete(0, END)
btnSearch = Button(window2, text="Szukaj", command=search,font=("bold", 12), activebackground="yellow")
btnSearch.pack(side=tk.LEFT, padx=6)
btnClear = Button(window2, text="Wyczyść", command=clear,font=("bold", 12), activebackground="yellow")
btnClear.pack(side=tk.LEFT, padx=6)

#sekcja szczegóły pierwsza kolumna
lbl1 = Label(window3, text="Id Budynku:",font=("bold", 12))
lbl1.grid(row=0, column=0, padx=5, pady=3)
ent1 = Entry(window3, textvariable=t1,font=("bold", 12))
ent1.grid(row=0, column=1, padx=5, pady=3, sticky=W)

lbl2 = Label(window3, text="Symbol Budynku:",font=("bold", 12))
lbl2.grid(row=1, column=0, padx=5, pady=3)
ent2 = Entry(window3, textvariable=t2,font=("bold", 12))
ent2.grid(row=1, column=1, padx=5, pady=3, sticky=W)

lbl3 = Label(window3, text="Symbol Osiedla:",font=("bold", 12))
lbl3.grid(row=2, column=0, padx=5, pady=3)
ent3 = Entry(window3, textvariable=t3,font=("bold", 12))
ent3.grid(row=2, column=1, padx=5, pady=3, sticky=W)

lbl4 = Label(window3, text="Kod pocztowy:",font=("bold", 12))
lbl4.grid(row=3, column=0, padx=5, pady=3)
ent4 = Entry(window3, textvariable=t4,font=("bold", 12))
ent4.grid(row=3, column=1, padx=5, pady=3, sticky=W)

lbl5 = Label(window3, text="Ulica:",font=("bold", 12))
lbl5.grid(row=4, column=0, padx=5, pady=3)
ent5 = Entry(window3, textvariable=t5,font=("bold", 12))
ent5.grid(row=4, column=1, padx=5, pady=3, sticky=W)

lbl6 = Label(window3, text="Symbol nieruchomości:",font=("bold", 12))
lbl6.grid(row=4, column=0, padx=5, pady=3)
ent6 = Entry(window3, textvariable=t6,font=("bold", 12))
ent6.grid(row=4, column=1, padx=5, pady=3, sticky=W)

lbl8 = Label(window3, text="Telefony :",font=("bold", 12))
lbl8.grid(row=5, column=0, padx=5, pady=3)
ent8 = Entry(window3, textvariable=t8,font=("bold", 12))
ent8.grid(row=5, column=1, padx=5, pady=3, sticky=W)

lbl9 = Label(window3, text="Wybierz treść",font=("bold", 12))
lbl9.grid(row=6, column=0, padx=5, pady=3)

mycombo = ttk.Combobox(window3, textvariable=opts, width=60, font=("bold", 12))
mycombo['values'] = options
mycombo.grid(row=6, column=1, padx=5, pady=3, sticky=W)
mycombo.current(0)
mycombo.bind("<<ComboboxSelected>>", chooseText)

lbl7 = Label(window3, text="Wiadomość SMS:",font=("bold", 12))
lbl7.grid(row=7, column=0, padx=5, pady=3)
ent7 = Text(window3, font=("bold", 12), width="30", height=2, wrap=WORD)
ent7.grid(row=7, rowspan=2, column=1, padx=5, pady=3, ipady=80, ipadx=40, sticky=NSEW)

#sekcja szczegóły buttony
btnSMS = Button(window3, text="Wyślij", command=sendSMS,font=("bold", 12), activebackground="yellow")
btnSMS.grid(row=9, column=1, padx=5, pady=3, sticky=E)

btnClearSMS = Button(window3, text="Wyczyść treść", command=clearText, font=("bold", 12), activebackground="yellow")
btnClearSMS.grid(row=9, column=1, padx=5, pady=3)

update(rows)
root.title("System SMS SM Budowlani")
root.geometry("1500x920")
root.resizable(0, 0)
root.mainloop()