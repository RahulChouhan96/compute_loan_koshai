1. 
    1. Group all rows with broker.
    2. Group by timeline
        1. Daily: Group rows with date.
        2. Weekly: Get week no for each date and create a new field with `date_weekNo`. Group with this field.
        3. Monthly: Get aprtial date and group with it.
    3. For each group in 2nd, sort rows with loan amount in decreasing order.

2. 