import datetime

class Log:
    def __init__(self, file, clear = True):
        self.file = file
        if clear:
          f = open(self.file, "w")
          f.close()

    def info(self, msg):
        with open(self.file, "a+") as f:
            f.write(f"[INFO] {datetime.datetime.now().strftime('%c')} | {msg}\n")

    def warn(self, msg):
        with open(self.file, "a+") as f:
            f.write(f"[WARNING] {datetime.datetime.now().strftime('%c')} | {msg}\n")
    
    def error(self, msg):
        with open(self.file, "a+") as f:
            f.write(f"[ERROR] {datetime.datetime.now().strftime('%c')} | {msg}\n")

    def handlederror(self, msg):
        with open(self.file, "a+") as f:
            f.write(f"[HANDLED] {datetime.datetime.now().strftime('%c')} | {msg}\n")

# Testing
if __name__ == "__main__":
    log = Log("src/testLog.log")
    log.info("test")
    log.warn("test")
    log.error("test")
    log.handlederror("test")