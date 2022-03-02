import csv
from datetime import datetime
import os

def save_data_to_csv(visited_urls):
  file_name = "/result/" + datetime.now().strftime("%Y_%m_%d_%H%M%S") + '.csv'
  file_path = os.path.join(os.getcwd(), file_name)

  print('[Preparing CSV] ......')

  with open(file_name, 'w') as fptr:
    fieldname = ['url', 'status_code', 'response_time', 'response_statement']
    
    csv_writer = csv.DictWriter(fptr, fieldnames=fieldname)

    csv_writer.writeheader()

    for url, detail in visited_urls.items():
      detail['url'] = url
      csv_writer.writerow(detail)

  print(f'[Complete]: successfully stored data in csv file')
  print(f'[File Location]: {file_path}')