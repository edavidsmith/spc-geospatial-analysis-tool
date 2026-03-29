import sqlite3
import pandas as pd

#this module is kept to update or change the db if necessary

con = sqlite3.connect("tornado-data\\tornado-events.db")
tor_data = pd.read_csv("tornado-data\\1950-2024_all_tornadoes.csv")

tor_data.to_sql("tornadoes", con, if_exists="replace", index=False)

con.close()

