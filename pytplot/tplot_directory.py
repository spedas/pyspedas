from . import tplot_common

def tplot_directory():
    import tkinter
    from tkinter import filedialog
    import os 
    
    #root = tkinter.Tk()
    download_path = filedialog.askdirectory()
    #root.destroy()
    
    #Put path into preferences file
    full_path=os.path.realpath(__file__)
    path, _ = os.path.split(full_path)
    f = open(os.path.join(path, 'pytplot_prefs.txt'), 'w')
    f.write("'; Location to save html files: '\n")
    f.write('tplot_save_dir: ' + download_path)
    
    return

def get_tplot_directory():
    import os
    full_path=os.path.realpath(__file__)
    path, filename = os.path.split(full_path)
    if (not os.path.exists(os.path.join(path, 'pytplot_prefs.txt'))):
        tplot_directory()
    f = open(os.path.join(path, 'pytplot_prefs.txt'), 'r')
    f.readline()
    s = f.readline().rstrip()
    #Get rid of first space
    s = s.split(' ')
    nothing = ' '
    
    return nothing.join(s[1:])
