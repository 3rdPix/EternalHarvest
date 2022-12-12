from harvest import EternalHarvest
import sys

if __name__ == '__main__':
    def hook(type, value, traceback):
        print(type)
        print(traceback)
    sys.__excepthook__ = hook

    app = EternalHarvest(sys.argv)
    sys.exit(app.exec())