# KoshAI Project

## Introduction
I've made the project using Python, SQL, VS code, etc. It involves all the calculations which are asked. All the output is generated in form of csv files so that it is easily readable.


## Directory Structure Description
1. `data` folder - It has `test.pdf` file which has all the data. Also, after converting this data into csv, I have stored both the pages of data in same folder.
2. `results` folder - After finishing all the computations, I've stored the results with proper names into this folder.
3. `script.py` file - This file has all the code which is used to parse and compute data. I've written code in functional style so that it is easy to understand.


## Project Setup
1. Clone the Github project.
2. Open project in VS Code.
3. Install following libraries using command: `pip install tabula-py pandas pandasql`.
4. Uncomment line 144 in `script.py` or you can search the line by `gen_csv()`. It will generate csv files from given pdf data.
5. Run the file `script.py` (As shown in SS).<img width="960" alt="image" src="https://github.com/RahulChouhan96/compute_loan_koshai/assets/42366136/99b8abc4-04e7-4a55-9c84-8068718479a1">

6. Input data and output results will be generated in the directories mentioned above in csv files.


## Implementation
### Converting data from pdf to csv
1. As there are multiple pages in pdf, I converted each page into a separate csv file.
2. The library to do this ie, `tabula` did some mistakes while reading such as it didn't read the headers, some columns were not separated properly etc. So, I had to manually correct them.
3. Function is `gen_csv`.

### Combine and get data from all csv files
As there were just 2 files, I didn't added any for-loop logic. I simply hardcoded and merged those 2 files into single object. Function is `combine_all_csv_pages`.

### Deduplication
As there were duplicate data, I removed them using `Xref` and `Total Loan Amount`.

### Data Computation
1. Grouped and sorted Total Loan Amount by broker and date with function `fetch_loan_amt_by_broker_date`.
2. Grouped and sorted Total Loan Amount by broker and month with function `fetch_loan_amt_by_broker_month`.
3. Grouped and sorted Total Loan Amount by broker and week with function `fetch_loan_amt_by_broker_week`.
4. Grouped Total Loan Amount by date with function `fetch_loan_amt_by_date`.
5. Grouped Total Loan Amount by tiers and date with function `fetch_loan_count_by_tiers`.
6. Please note that after computing all above, they are stored in a csv file.


## Future Improvements
1. Creating a `requirements.txt` file and keeping all the library names into it. So that when a new developer comes, they don't have to install all libraries one-by-one. They can simply do it using one command.
2. After converting data from pdf to csv, I had manually correct it as there were some inconsistencies. When there will be large dataset, this wouldn't be possible. Hence, we should figure out patterns in data inconsistencies and write scripts to remove them.
