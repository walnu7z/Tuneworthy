import sys
from src.Minero import *
from src.TuneworthyPlayer import *

def main():
    app = TuneworthyPlayer(application_id="com.github.walnu7z.Tuneworthy")
    app.run(sys.argv)
    

if __name__ == "__main__":
    main()
