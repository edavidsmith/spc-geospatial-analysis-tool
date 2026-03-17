import os
from forecast_utils import *

def main():
    disposable_extensions = (".shp", ".shx", ".dbf", ".prj", ".zip")
    cont_forecasting = ("yes", "no")
    user_response = cont_forecasting[0]
    
    while(user_response != cont_forecasting[1]):
        shape_file_parsing()
        for file in os.listdir():
            if file.endswith(disposable_extensions):
                os.remove(file)
        
        user_response = input("Do you wish to see another forecast? (Yes/No) ").strip().lower()
        while(user_response not in cont_forecasting):
            user_response = input("Invalid input. Select yes or no. ").strip().lower()

if __name__ == "__main__":
    main()