
from tkinter import *
import bs4
import requests

from datetime import datetime

root = Tk()
root.title("Bitcoin Price Checker")
root.iconbitmap("bitcoin.png")
root.geometry("560x220")
root.config(bg="black")

global previous
previous = False
now = datetime.now()
current_time = now.strftime("%I:%M:%S %p")

frame1 = Frame(root, bg="black")
frame1.pack(pady=30)

logo = PhotoImage(file="bitcoin.png")
logo_label = Label(frame1, image=logo, bd=0)
logo_label.grid(row=0, column=0, rowspan=2)

bitcoin_label = Label(frame1, text="TEST",
                      font=("Helvetica", 45),
                      bg="black",
                      fg="green",
                      bd=0)

bitcoin_label.grid(row=0, column=1, padx=20, sticky="s")

latest_price = Label(frame1, text="move test",
                     font=("Helvetica", 10),
                     bg="black",
                     fg="grey")
latest_price.grid(row=1, column=1, sticky="n")


def Update():
    global previous

    page = requests.get("https://www.coindesk.com/price/bitcoin/")
    soup = bs4.BeautifulSoup(page.text, "lxml")
    price_l = soup.find("span", class_="currency-pricestyles__Price-sc-1rux8hj-0 jIzQOt").text

    bitcoin_label.config(text=f"$ {price_l}")

    root.after(30000, Update)

    now = datetime.now()
    current_time = now.strftime("%I:%M:%S %p")
    status_footer.config(text=f"Last Updated: {current_time}")

    current = price_l
    current = current.replace(",", "")
    if previous:
        if float(previous) > float(current):
            latest_price.config(text=f"Price Down $ {round(float(previous) - float(current), 2)}",
                                fg="red")
        elif float(previous) == float(current):
            latest_price.config(text="Price Unchanged",
                                fg="grey")
        else:
            latest_price.config(text=f"Price Up $ {round(float(current) - float(previous), 2)}",
                                fg="green")

    else:
        previous = current
        latest_price.config(text="Price Unchanged",
                            fg="grey")


status_footer = Label(root, text=f"Last Updated {current_time}   ",
                      bd=0,
                      anchor=E,
                      bg="black",
                      fg="grey")
status_footer.pack(fill=X, side=BOTTOM, ipady=10)
Update()

root.mainloop()
