from PIL import Image
import pathlib, configparser, os, sys, datetime, keyring, subprocess
from pystray import Icon as icon, Menu as menu, MenuItem as item
import pystray
import PIL

class config_file:
    def __init__(self, filepath):
        self.filepath = filepath
        if not os.path.exists(self.filepath):
            open(self.filepath, 'a').close()
        self.config = configparser.ConfigParser()
        self.config.read(filepath)

    def read(self, section, parameter):
        if not self.config.has_option(section, parameter):
            return None
        else:
            return self.config[section][parameter]

    def write(self, section, parameter, value):
        if not self.config.has_section(section):
            self.config.add_section(section)
        self.config.set(section, parameter, value)
        with open(self.filepath, 'w') as configfile:
            self.config.write(configfile)


def set_state(v):
    def inner(icon, item):
        global state
        state = v
        config.write('Settings', 'interval', state_dict[v])
    return inner

from tkinter import *
def get_state(v):
    def inner(item):
        #return state == v
        return config.read('Settings', 'interval') == state_dict[v]
    return inner


def pop_up():
    app = Tk()
    app.title("CanvasSync Password")
    label = Label(app, text="Please enter the CanvasSync Password:")
    label.grid()
    pwd = StringVar()
    e1 = Entry(app, width=40, textvariable=pwd)
    btn = Button(app, text="Ok", command=app.destroy)
    btn.grid(row=2)
    e1.grid(row=1)

    app.mainloop()
    return pwd.get()


def savepassword():
    response = str(pop_up())
    keyring.set_password('CanvasSync', 'xkcd', response)

def runSync():
    print('sync')

    # Import Canvas Module
    path = str(pathlib.Path(__file__).parent.parent.parent) + "/bin/"
    sys.path.insert(0, path)
    import canvas

    settings = canvas.Settings()
    password = keyring.get_password('CanvasSync', 'xkcd')
    canvas.do_sync(settings, password)
    config.write('Last run', 'time', str(datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")))

def preferences():
    pass

def quit_icon():
    #ToDo: Quit App does not work at the moment.
    icon.stop()

dir_path = os.path.dirname(os.path.realpath(__file__))

if __name__ == '__main__':
    image = PIL.Image.open('canvas_logo.png')

    state = 0
    state_dict = {
        1: 'hourly',
        2: 'every 6 hours',
        3: 'daily',
        4: 'Do not sync'
    }

    if keyring.get_password('CanvasSync', 'xkcd') is None:
        savepassword()

    # Run Scheduler as independent subprocess
    path = str(os.path.abspath(os.path.join(os.path.join(os.path.abspath(__file__), '..'), '..'))) + '\\scheduler\\scheduler.py'
    subprocess.Popen(["python", path])

    config = config_file(str(os.path.abspath(os.path.join(os.path.join(os.path.abspath(__file__), '..'), '..'))) + "\\scheduler\\scheduler.ini")
    icon('test', image, menu=menu(
        item('Sync now', runSync),
        item(
            'Automatic sync',
            menu(
                item(
                    'hourly',
                    set_state(1),
                    checked=get_state(1),
                    radio=True),
                item(
                    'every 6 hours',
                    set_state(2),
                    checked=get_state(2),
                    radio=True),
                item(
                    'daily',
                    set_state(3),
                    checked=get_state(3),
                    radio=True),
                item(
                    'Do not sync',
                    set_state(4),
                    checked=get_state(4),
                    radio=True))),
        item('Preferences', preferences),
        item('Quit now', quit_icon)
        )).run()