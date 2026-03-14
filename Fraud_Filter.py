import pandas as pd
df = pd.read_excel("transactions_custom.xlsx")
print(df.dtypes)

df['timestamp'] = pd.to_datetime(df['timestamp'])
print(df.dtypes)

df = df.sort_values(by=['user_id', 'timestamp'])
fraud_status = []

for index in range(len(df)):
    current_transaction = df.iloc[index]
    
    # previous transactions of same users
    previous_transactions = df[
        (df['user_id'] == current_transaction['user_id']) &
        (df['timestamp'] < current_transaction['timestamp'])
    ].tail(3)
    
    # Rule 1: Amount > 1,00,000
    rule1 = current_transaction['amount'] > 100000
    
    # Rule 2: Location different from last 3
    if len(previous_transactions) == 3:
        rule2 = all(
            current_transaction['location'] != loc
            for loc in previous_transactions['location']
        )
    else:
        rule2 = False
    
    # Rule 3: Time between 2 AM – 4 AM
    hour = current_transaction['timestamp'].hour
    rule3 = (hour >= 2) and (hour <= 4)
    
    decision = "Legitimate"

    # conditional criteria for the transaction to be fraudulent 
    if (rule1 and rule2 and rule3) or \
       (rule1 and rule2) or \
       (rule1 and rule3) or \
       (rule2 and rule3) or \
       (rule2):
        decision = "Fraudulent"

    fraud_status.append(decision)

df['fraud_status'] = fraud_status
print(df)
 
fraudulent_transactions = df[df['fraud_status'] == "Fraudulent"]
print("Fraudulent Transactions:\n")
print(fraudulent_transactions)


