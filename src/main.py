import sys
from src.Minero import *

if __name__ == "__main__":
    print("Hello, World!")
    minero = Minero()
    
    pros = Prospector()
    files = pros.find_mp3_files()

    print(files[-1])