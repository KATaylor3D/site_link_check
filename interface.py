from tkinter import *

window = Tk()
window.title('Site_Link_Check')
window.iconbitmap('obviously your own path to the .ico file')

header = Label(text = 'Site_Link_Check Tool', width = 80)
scrollbar = Scrollbar(window)

def set_Listbox(text):
    lb = Listbox(window, width = 90, yscrollcommand = scrollbar.set)
    if type(text) == type(''):
        lb.insert(END, text)
    else:
        for line in text:
            lb.insert(END, line)
    return lb

info_listbox = set_Listbox('')
scrollbar.config( command = info_listbox.yview )
info_label = Label(text = 'Info', width = 40)
info_message = Label(text = '', relief = 'sunken', bd = 1, width = 77)
website_entry = Entry(window, bd = 6, width = 54, relief = 'flat')
scan_button = Button(window, padx = 16, text = "Scan", command = None)
visit_button = Button(window, padx = 16, text = "Visit", state = 'disabled',  command = None)
close_button = Button(window, padx = 14, text = "Close", command = window.quit)


header.pack()
scrollbar.pack(side = 'right', fill = 'y')
info_listbox.pack()
info_label.pack()
info_message.pack()
website_entry.pack(side = 'left', expand = 1)
scan_button.pack(side = 'left', expand = 1)
visit_button.pack(side = 'right', expand = 1)
close_button.pack()


mainloop()