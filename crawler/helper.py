import csv
from datetime import datetime
import os

# print('\\result\\' + str(datetime.now()) + '.csv')


def save_data_to_csv(visited_urls):
  file_name = "crawler/result/" + datetime.now().strftime("%Y_%m_%d_%H%M%S") + '.csv'

  with open(file_name, 'w') as fptr:
    fieldname = ['url', 'status_code', 'response_time', 'response_statement']
    
    csv_writer = csv.DictWriter(fptr, fieldnames=fieldname)

    csv_writer.writeheader()

    for url, detail in visited_urls.items():
      detail['url'] = url
      csv_writer.writerow(detail)