import os
from forecast_utils import *

def main():
    shape_file_parsed()
    disposable_extensions = (".shp", ".shx", ".dbf", ".prj", ".zip")

    for file in os.listdir():
        if file.endswith(disposable_extensions):
            os.remove(file)

if __name__ == "__main__":
    main()