import time


class GameTime:  # Loome mänguaja objekti
    def __init__(self, lbl_time):
        self.__lbl_time = lbl_time
        self.__counter = 0
        self.__running = False

    @property
    def counter(self):  # Tagastame mänguaja
        return self.__counter

    def update(self):  # Kuvame mänguaja
        if self.__running:
            if self.__counter == 0:
                display = "00:00:00"
            else:
                display = time.strftime("%H:%M:%S", time.gmtime(self.__counter))

            self.__lbl_time["text"] = display
            self.__lbl_time.after(1000, self.update)  # Värskendame iga sekundi järel
            self.__counter += 1

    def start(self):  # Mänguaja käivitamine
        self.__running = True
        self.update()

    def stop(self):  # Mänguaja peatamine
        self.__running = False

    def reset(self):  # Mänguaja nullimine
        self.__counter = 0
        self.__lbl_time["text"] = "00:00:00"
