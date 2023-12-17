import datetime
from tkcalendar import DateEntry
from tkinter import *
import tkinter.ttk as ttk
import tkinter as tk
import requests

expenses = []

def convert_to_usd(amount, from_currency):
    if from_currency == 'USD':
        return amount
    else:
        api_key = '9710bd3b15fc3293b82f795b'
        base_url = 'https://api.exchangerate-api.com/v4/latest/{}'.format(from_currency)

        try:
            response = requests.get(base_url)
            data = response.json()
            usd_rate = data['rates']['USD']
            usd_amount = amount * usd_rate

            
            if usd_amount is not None:
                return usd_amount
            else:
                print("Error converting to USD: Conversion rate is not available.")
                return None

        except requests.exceptions.RequestException as e:
            print(f"Error fetching currency conversion data: {e}")
            return None



def list_all_expenses():
    for i in table.get_children():
        table.delete(i)

    for expense in expenses:
        amount_before = expense['amount_before']
        amount_after = convert_to_usd(amount_before, expense['currency']) if expense['currency'] != 'USD' else amount_before
        table.insert('', 'end', values=(amount_after, 'USD', expense['category'], expense['payment_method']))
    update_total_amount()


def add_another_expense():
    category_value = cate.get()
    currency_value = curr.get()
    amount_before = amnt.get()
    payment_method_value = Mop.get()

    amount_after = convert_to_usd(amount_before, currency_value) if currency_value != 'USD' else amount_before

    expense = {
        'category': category_value,
        'currency': currency_value,
        'amount_before': amount_before,
        'amount_after': amount_after,
        'payment_method': payment_method_value
    }

    expenses.append(expense)

    cate.set('')
    curr.set('')
    amnt.set('')
    Mop.set('Cash')
    date.set_date(datetime.datetime.now().date())

    list_expenses()


def list_expenses():
    for i in table.get_children():
        table.delete(i)

    for expense in expenses:
        amount_before = expense['amount_before']
        table.insert('', 'end', text='', values=(amount_before, expense['currency'], expense['category'], expense['payment_method']))

    update_total_amount()



def update_total_amount():
    total_amount_after = sum(expense['amount_after'] for expense in expenses)

    total_label.config(text=f'Total Amount: {total_amount_after:.2f} USD')


def delete_selected_expense():
    selected_item = table.selection()
    if selected_item:
        index = table.index(selected_item)
        del expenses[index]
        list_expenses()


def clear_all_expenses():
    expenses.clear()
    list_expenses()


def sort_expenses_by_price():
    expenses.sort(key=lambda expense: expense['amount_before'], reverse=True)
    list_expenses()

def sort_expenses_by_price_low_to_high():
    expenses.sort(key=lambda expense: expense['amount_before'])
    list_expenses()



dataentery_frame_bg = 'pale turquoise'
buttons_frame_bg = 'lemon chiffon'
hlb_btn_bg = 'snow'

lbl_font = ('Tahoma', 12)
entry_font = 'Geneva'
btn_font = ('Franklin Gothic', 10)

root = Tk()
root.title('EXPENSE TRACKER')
root.geometry('1200x600')
root.resizable(0, 0)


Label(root, text='EXPENSE TRACKER', font=('Noto Sans CJK TC', 10, 'bold'), bg=hlb_btn_bg).pack(side=TOP, fill=X)

cate = StringVar()
curr = StringVar()
amnt = DoubleVar()
Mop = StringVar(value='Cash')

data_entry_frame = Frame(root, bg=dataentery_frame_bg)
data_entry_frame.place(x=0.5, y=30, relheight=2, relwidth=1)

buttons_frame = Frame(root, bg=buttons_frame_bg)
buttons_frame.place(relx=0.25, rely=0.05, relwidth=0.75, relheight=0.25)

tree_frame = Frame(root)
tree_frame.place(relx=0.25, rely=0.10, relwidth=0.75, relheight=0.90)

Label(data_entry_frame, text='Date:', font=lbl_font, bg=dataentery_frame_bg).place(x=10, y=10)
date = DateEntry(data_entry_frame, date=datetime.datetime.now().date(), font=entry_font)
date.place(x=100, y=10)

Label(data_entry_frame, text='Category:', font=lbl_font, bg=dataentery_frame_bg).place(x=10, y=60)
Entry(data_entry_frame, font=entry_font, width=20, text=cate).place(x=100, y=60)

Label(data_entry_frame, text='Currency:', font=lbl_font, bg=dataentery_frame_bg).place(x=10, y=110)
dd1 = OptionMenu(data_entry_frame, curr, *['USD','EGP','EUR','AUD','BRL','GBP','XCD','XOF','NZD','XAF','ZAR','XPF','RUB','DKK','JOD','TRY','CAD'])
dd1.place(x=100, y=110)     ;     dd1.configure(width=10, font=entry_font)

Label(data_entry_frame, text='Amount:', font=lbl_font, bg=dataentery_frame_bg).place(x=10, y=160)
Entry(data_entry_frame, font=entry_font, width=10, text=amnt).place(x=100, y=160)

Label(data_entry_frame, text='Payment Method:', font=lbl_font, bg=dataentery_frame_bg).place(x=10, y=210)
dd2 = OptionMenu(data_entry_frame, Mop, *['Cash', 'Credit Card', 'Paypal','Instapay','Vodafon Cash'])
dd2.place(x=160, y=210)     ;     dd2.configure(width=10, font=entry_font)

Button(data_entry_frame, text='Add Expense', command=add_another_expense, font=btn_font, width=25,
    bg=hlb_btn_bg).place(x=50, y=280)

Button(data_entry_frame, text='Delete Expense', command=delete_selected_expense, font=btn_font, width=25,
    bg=hlb_btn_bg).place(x=50, y=320)

Button(data_entry_frame, text='Delete All Expenses', command=clear_all_expenses, font=btn_font, width=25,
    bg=hlb_btn_bg).place(x=50, y=360)

Button(data_entry_frame, text='Sort by Price (High to Low)', command=sort_expenses_by_price, font=btn_font, width=25,
    bg=hlb_btn_bg).place(x=50, y=400)

Button(data_entry_frame, text='Sort by Price (Low to High)', command=sort_expenses_by_price_low_to_high, font=btn_font, width=25,
    bg=hlb_btn_bg).place(x=50, y=440)


table = ttk.Treeview(tree_frame, selectmode=BROWSE, columns=('Amount','Currency','Category','Payment Method'))

X_Scroller = Scrollbar(table, orient=HORIZONTAL, command=table.xview)
Y_Scroller = Scrollbar(table, orient=VERTICAL, command=table.yview)
X_Scroller.pack(side=BOTTOM, fill=X)
Y_Scroller.pack(side=RIGHT, fill=Y)

table.config(yscrollcommand=Y_Scroller.set, xscrollcommand=X_Scroller.set)

table.heading('Currency', text='Currency', anchor=CENTER)
table.heading('Category', text='Category', anchor=CENTER)
table.heading('Amount', text='Amount', anchor=CENTER)
table.heading('Payment Method', text='Payment Method', anchor=CENTER)

table.column('#0', width=0, stretch=NO)
table.column('#1', width=100, stretch=YES)
table.column('#2', width=100, stretch=YES)  
table.column('#3', width=100, stretch=YES)

table.place(relx=0, y=1, relheight=0.8, relwidth=1)

total_label = Label(tree_frame, text='Total Amount: ', font=lbl_font, bg=dataentery_frame_bg)
total_label.place(relx=0.01, rely=0.85)

list_all_expenses()

root.update()
root.mainloop()
