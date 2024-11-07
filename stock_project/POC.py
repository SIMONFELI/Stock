from datetime import datetime

import pandas as pd
import requests
import datetime as dt
pd.set_option('display.max_columns', None)

# import pandas as pd
github_api_url = "https://api.github.com/repos/squareshift/stock_analysis/contents/"
response = requests.get(github_api_url)
# print(response)
a = response.json()
# print(a)
a = response.text
# print(a)
#
# r =[{'a':5,'b':6,'c':7}][{'d':8,'e':9}]
# print((r[0]))
b = response.json()
csv_files = [file['download_url']for file in b if file['name'].endswith('csv')]
# print(len(csv_files))
# print(csv_files)
a = csv_files[0]
# print(a)
csv_file = csv_files.pop()
# print(csv_file)
# print(type(csv_file))
d = pd.read_csv(csv_file)
# print(d)
dataframes=[]
file_names=[]
for url in csv_files:
    # print(csv_file)
    file_name = url.split("/")[-1].replace(".csv","")
    # print(file_name)
    df = pd.read_csv(url)
    df['Symbol'] = file_name
    # print(df)
    dataframes.append(df)
    file_names.append(file_name)
# print(file_names)
# print(dataframes)
combined_df = pd.concat(dataframes,)
# print("Hello:",combined_df)
o_df = pd.merge(combined_df,d,on='Symbol',how='left')
result = o_df.groupby("Sector").agg({'open':'mean','close':'mean','high':'max','low':'min','volume':'mean'}).reset_index()
# print(o_df.columns)
# print(o_df["timestamp"])
# print(result)
o_df["timestamp"] = pd.to_datetime(o_df["timestamp"])
# print(o_df["timestamp"])
# print(o_df.dtypes)
# print(o_df)
filtered_df = o_df[(o_df['timestamp'] >= "2021-01-01") & (o_df['timestamp'] <= "2021-05-26")]
# print(filtered_df)
result_time = filtered_df.groupby("Sector").agg({'open':'mean','close':'mean','high':'max','low':'min','volume':'mean'}).reset_index()
list_sector = ["TECHNOLOGY","FINANCE"]
result_time = result_time[result_time["Sector"].isin(list_sector)].reset_index(drop=True)
# print(result_time)
path=r"stock_data.csv"
result_time.to_csv(path,header=True)
print("data has been written successfully")


