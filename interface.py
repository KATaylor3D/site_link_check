from tkinter import *
import os
import check_site_links as csl
import webbrowser

window = Tk()

url_entry = StringVar()
visit_listbox = StringVar()
info = StringVar()
info.set('Type url below and hit scan to start')
window.title('Site_Link_Check')


def get_ico():
    current_directory = os.getcwd()
    ico_directory = current_directory + '\\img\\broken_link.ico'
    return ico_directory


window.iconbitmap(get_ico())


def scan():
    url = website_entry.get()
    try:
        info.set('If this is the first time scanning. This could take a while')
        url_tups = csl.logic(url)
        problem_links = csl.get_problem_links(url_tups)
        broken_links = csl.get_broken_links(url_tups)
        for link in broken_links:
            link, parent, text, status_code = link
            info_listbox.insert(END, f'Broken link : {link}')
            info_listbox.insert(END, f'    Parent : {parent}')
            info_listbox.insert(END, f'    Link name : {text}')
            info_listbox.insert(END, f'    Status code : {status_code}')
        for link in problem_links:
            link, parent, text, status_code = link
            info_listbox.insert(END, f'Problem link : {link}')
            info_listbox.insert(END, f'    Parent : {parent}')
            info_listbox.insert(END, f'    Link name : {text}')
            info_listbox.insert(END, f'    Status code : {status_code}')
        info.set(f'There are {len(broken_links)} broken links and {len(problem_links)} problem links')
    except:
        info.set('Invalid entry try again')

def rescan():
    url = website_entry.get()
    if url:
        filename = csl.create_filename_from_url(url)
        os.remove(filename)
    else:
        try:
            info.set('Please wait while the full scan completes. This could take a while')
            url_tups = csl.logic(url)
            problem_links = csl.get_problem_links(url_tups)
            broken_links = csl.get_broken_links(url_tups)
            for link in broken_links:
                link, parent, text, status_code = link
                info_listbox.insert(END, f'Broken link : {link}')
                info_listbox.insert(END, f'    Parent : {parent}')
                info_listbox.insert(END, f'    Link name : {text}')
                info_listbox.insert(END, f'    Status code : {status_code}')
            for link in problem_links:
                link, parent, text, status_code = link
                info_listbox.insert(END, f'Problem link : {link}')
                info_listbox.insert(END, f'    Parent : {parent}')
                info_listbox.insert(END, f'    Link name : {text}')
                info_listbox.insert(END, f'    Status code : {status_code}')
            info.set(f'There are {len(broken_links)} broken links and {len(problem_links)} problem links')
        except:
            info.set('Invalid entry try again')

def visit():
    if info_listbox.curselection():
        selection = info_listbox.get(info_listbox.curselection())
        url = selection.split(" : ")[1]
        webbrowser.open(url)


header = Label(text = 'Site_Link_Check Tool', width = 80)
scrollbar = Scrollbar(window)
info_listbox = Listbox(window, justify = 'left', width = 110, yscrollcommand = scrollbar.set)
scrollbar.config( command = info_listbox.yview )
info_label = Label(text = 'Info', width = 40)
info_message = Label(textvariable = info, anchor = 'w', relief = 'sunken', bd = 1, width = 94)
website_entry = Entry(window, textvariable = url_entry, bd = 6, width = 58, relief = 'flat')
scan_button = Button(window, padx = 18, text = "Scan", command = scan)
rescan_button = Button(window, padx = 18, text = "Full Scan", command = rescan)
visit_button = Button(window, padx = 18, text = "Visit", command = visit)
close_button = Button(window, padx = 18, text = "Close", command = window.quit)


header.pack()
scrollbar.pack(side = 'right', fill = 'y')
info_listbox.pack()
info_label.pack()
info_message.pack()
website_entry.pack(side = 'left', expand = 1)
scan_button.pack(side = 'left', expand = 1)
rescan_button.pack(side = 'left', expand = 1)
visit_button.pack(side = 'right', expand = 1)
close_button.pack(side = 'right', expand = 1)

if __name__ == '__main__':
    mainloop()