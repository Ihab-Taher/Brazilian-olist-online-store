import pandas as pd
import matplotlib.pyplot as plt

# Read the dataset
dataset_path = 'D:\\Career\\Data Analysis projects\\Brazilian olist online store\\Datasets\\olist_customers_dataset.csv'
df = pd.read_csv(dataset_path)

# Show info. about the dataset such as how many non null values and data type for each field (attribute)
print(df.info())

# Show first n rows of the dataset
n = 10
print('\nFirst {} row(s) of the dataset\n'.format(n), df.head(n))

# Make sure there are no duplicated records in the dataset
duplicate_rec_ser = df.duplicated().value_counts()
print('\nDuplicte records check:')
if (True in list(duplicate_rec_ser.index)):
    print('No. of duplicated records is : ', duplicate_rec_ser.loc[True])
else:
    print('No duplicated records in the dataset')

# Create a new attribute
df['customer_city_state'] = df['customer_city'] + ', ' + df['customer_state']

#print(df[df['customer_unique_id'].duplicated() == True])
#print(df[df['customer_unique_id'] == 'b6c083700ca8c135ba9f0f132930d4e8'])

'''
 We discovered that there is duplication in customer_unique_id which suggests that same customer may duplicate but with different customer_id which will reference
  the order in other datasets.
'''

df = df[['customer_unique_id', 'customer_zip_code_prefix', 'customer_city', 'customer_state', 'customer_city_state']]
df.drop_duplicates(inplace=True)

df_cust_cnt_by_city_state = df.groupby('customer_city_state').count()['customer_unique_id'].rename({'customer_unique_id': 'Customer Count'}).copy()
df_cust_cnt_by_city_state.sort_values(ascending=False, inplace=True)

top_n_city_state = 7

fig = plt.figure(num=1, figsize = (8, 5))
plt.bar(df_cust_cnt_by_city_state.iloc[0:top_n_city_state].index, df_cust_cnt_by_city_state.iloc[0:top_n_city_state].values)
plt.xlabel('City, State')
plt.ylabel('No. of customers')
plt.title('No. of customers per city and state for the top {}'.format(top_n_city_state))
plt.xticks(rotation=20, fontsize=6)
plt.show()
