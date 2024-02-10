from flask import Flask, render_template, request
import pandas as pd
from io import StringIO
import numpy as np

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        uploaded_file = request.files['file']

        if uploaded_file:
            csv_data = uploaded_file.read().decode('utf-8')
            df = pd.read_csv(StringIO(csv_data))
            table_html = df.to_html(classes='table table-striped')
            print(df)
            df = df.drop(df.columns[0], axis=1)
            A = df.values
            print(A)
            global IA 
            global n
            global m
            AA=[]
            IA=[]
            m,  n = A.shape
            for i in range(m):
                non_zero_indices = np.nonzero(A[i])[0]
                IA.extend(non_zero_indices + 1 + i * n)
            IA = np.array(IA)
            print("IA:", IA)
            return render_template('index.html', table_html=table_html)

    return render_template('index.html', table_html=None)

def find_service(row_index, col_index, num_columns):
    single_index = (row_index * num_columns) + col_index +1
    if single_index in IA:
      ind=np.where(IA== single_index)[0]
      return 1
    else:
      return -1
  
def find_all_service_for_pincode(col_index, num_columns, num_rows):         
    index_arr = []
    row_index_arr = []
    for i in range(num_rows+1):
        ind = (col_index) + i*num_columns
        index_arr.append(ind)
    for single_index in index_arr:
        if single_index in IA:
            ind=np.where(IA == single_index)[0]
            row_index_arr.append((single_index//num_columns)+1)
    return row_index_arr



@app.route('/search_pincode', methods=['POST'])
def search_pincode():
    pincode_to_search = request.form.get('pincode')
    merchant_id_search = request.form.get('Merchant')
    if pincode_to_search and  merchant_id_search:
        col_index = int(pincode_to_search)-1
        row_index = int(merchant_id_search)-1
        num_columns = n 
        result = find_service(row_index, col_index, num_columns)
        if result==1:
            result = 'found'
        else:
            result = ''
        return render_template('status.html', result=result)
    elif pincode_to_search:
        pincode_to_search=int(pincode_to_search)
        pincode_list=find_all_service_for_pincode(pincode_to_search, n, m)
        print(pincode_list)
        return render_template('status.html', result=pincode_list)
        
        

if __name__ == '__main__':
    app.run(debug=True)
