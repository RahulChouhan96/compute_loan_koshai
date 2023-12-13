from pandasql import sqldf
import pandas as pd
import tabula


def gen_csv():
    pdf_path = "/data/test.pdf"

    tables = tabula.read_pdf(pdf_path, pages='all', multiple_tables=True)
    print(tables)

    for i, table in enumerate(tables):
        print(f"Table {i + 1}:\n{table}\n")

    col_names = ["App ID", "Xref", "Settlement Date", "Broker", "Sub Broker", "Borrower Name", "Description", "Total Loan Amount", "Comm Rate", "Upfront", "Upfront Incl GST"]
    for i, table in enumerate(tables):
        if i == 1:
            col_names = col_names[:9]
        table.columns = col_names
        table.to_csv(f"/data/table_{i + 1}.csv", index=False, header=True)


def combine_all_csv_pages():
    df1 = pd.read_csv("/data/table_1.csv")
    df2 = pd.read_csv("/data/table_2.csv")
    df = pd.concat([df1, df2], ignore_index=True)
    return df


def fetch_loan_amt_by_broker_date(df):
    query = """
        SELECT broker, "Settlement Date", GROUP_CONCAT("Total Loan Amount", ", ") as total_loan_amount
        FROM (
            SELECT
                broker,
                "Settlement Date",
                "Total Loan Amount"
            FROM df
            ORDER BY "Total Loan Amount" DESC
        )
        GROUP BY broker, "Settlement Date"
    """

    result11 = sqldf(query, locals())
    print("1.1", result11)
    result11.to_csv("/results/loan_amt_by_broker_date_1_1.csv", index=False)


def fetch_loan_amt_by_broker_month(df):
    query = """
        SELECT
            broker,
            strftime('%m/%Y', "Settlement Date") AS month_year,
            GROUP_CONCAT("Total Loan Amount", ", ") as loan_amount_list
        FROM (
            SELECT
                broker,
                "Settlement Date",
                "Total Loan Amount"
            FROM df
            ORDER BY "Total Loan Amount" DESC
        )
        GROUP BY broker, month_year
        ORDER BY broker, month_year, SUM("Total Loan Amount") DESC
    """

    result12 = sqldf(query, locals())
    print("1.2", result12)
    result12.to_csv("/results/loan_amt_by_broker_month_1_2.csv", index=False)


def fetch_loan_amt_by_broker_week(df):
    query = """
        SELECT
            broker,
            strftime('%W/%Y', "Settlement Date") AS week_year,
            GROUP_CONCAT("Total Loan Amount", ', ') as loan_amount_list
        FROM (
            SELECT
                broker,
                "Settlement Date",
                "Total Loan Amount"
            FROM df
            ORDER BY "Total Loan Amount" DESC
        )
        GROUP BY broker, week_year
    """

    result13 = sqldf(query, locals())
    print("1.3", result13)
    result13.to_csv("/results/loan_amt_by_broker_week_1_3.csv", index=False)


def fetch_loan_amt_by_date(df):
    query = """
        SELECT
            "Settlement Date",
            GROUP_CONCAT("Total Loan Amount") as loan_amount_list
        FROM df
        GROUP BY "Settlement Date"
    """

    result21 = sqldf(query, locals())
    print("2.1", result21)
    result21.to_csv("/results/loan_amt_by_date_2_1.csv", index=False)


def fetch_loan_count_by_tiers(df):
    df['Total Loan Amount'] = df['Total Loan Amount'].replace('[\$,]', '', regex=True).astype(float)
    query = """
        SELECT
            CASE
                WHEN "Total Loan Amount" > 100000 THEN 'Tier 1' 
                WHEN "Total Loan Amount" > 50000 AND "Total Loan Amount" <= 100000 THEN 'Tier 2'
                WHEN "Total Loan Amount" > 10000 AND "Total Loan Amount" <= 50000 THEN 'Tier 3'
                ELSE 'Tier 4'
            END AS loan_tier,
            "Settlement Date",
            COUNT(*) as count_in_tier
        FROM df
        GROUP BY loan_tier, "Settlement Date"
    """

    result4 = sqldf(query, locals())
    print("4", result4)
    result4.to_csv("/results/loan_count_by_tiers_4.csv", index=False)


def compute_results_by_data():
    df = combine_all_csv_pages()
    
    # Deduplicate based on "xref" and "loan amount" columns
    df = df.drop_duplicates(subset=["Xref", "Total Loan Amount"])
    df['Settlement Date'] = pd.to_datetime(df['Settlement Date'], format='%d/%m/%Y')

    fetch_loan_amt_by_broker_date(df)
    fetch_loan_amt_by_broker_month(df)
    fetch_loan_amt_by_broker_week(df)
    fetch_loan_amt_by_date(df)
    fetch_loan_count_by_tiers(df)


if __name__ == "__main__":
    # gen_csv()   # Run only once in the start
    compute_results_by_data()
