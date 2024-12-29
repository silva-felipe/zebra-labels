import requests
import shutil
import time
import pdb

def generate_pdf(batch_files, now):

    batch_files_pdf = []

    for file_path in batch_files:
        time.sleep(1)
        with open(file_path, 'r') as f:
            zpl = f.read()

        # adjust print density (8dpmm), label width (4 inches), label height (6 inches), and label index (0) as necessary
        url = 'http://api.labelary.com/v1/printers/8dpmm/labels/4x6/'
        files = {'file' : zpl}
        headers = {'Accept' : 'application/pdf'} # omit this line to get PNG images back
        response = requests.post(url, headers = headers, files = files, stream = True)

        file_path = file_path.replace('.txt', '.pdf')
        file_path = file_path.replace('queue/', 'zebras_pdf/')

        if response.status_code == 200:
            response.raw.decode_content = True
            with open(f'{file_path}', 'wb') as out_file:
                shutil.copyfileobj(response.raw, out_file)

            batch_files_pdf.append(file_path)
        else:
            print('Error: ' + response.text)

    return batch_files_pdf, now