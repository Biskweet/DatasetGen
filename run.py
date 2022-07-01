import sys
from src import Generator

if __name__ == "__main__":
    app = Generator(sys.argv)
    app.generate_image()
