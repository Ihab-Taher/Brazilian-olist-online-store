import pandas as pd

# Paths of datasets
orders_items_dataset_path = 'D:\\Career\\Data Analysis projects\\Brazilian olist online store\\Datasets\\olist_order_items_dataset.csv'
products_dataset_path = 'D:\\Career\\Data Analysis projects\\Brazilian olist online store\\Datasets\\olist_products_dataset.csv'
orders_dataset_path = 'D:\\Career\\Data Analysis projects\\Brazilian olist online store\\Datasets\\olist_orders_dataset.csv'
customers_dataset_path = 'D:\\Career\\Data Analysis projects\\Brazilian olist online store\\Datasets\\olist_customers_dataset.csv'

df_orders_items = pd.read_csv(orders_items_dataset_path)
df_products = pd.read_csv(products_dataset_path)
df_orders = pd.read_csv(orders_dataset_path)
df_customers = pd.read_csv(customers_dataset_path)

# Is order_id the primary key in this dataset
#print('\nChecking if order_id alone is the primary key of order items dataset:\n', df_orders_items['order_id'].duplicated().value_counts())

# After running the previous line the order_id has duplicates.

# Is the combination of order_id and order_item_id the primary key in this dataset
#print('\nChecking if the combiation of order_id and order_item_id is the primary key of order items dataset:\n', df_orders_items[['order_id', 'order_item_id']].duplicated().value_counts())

# Yes, we did it. The combination of order_id and order_item_id is the primary key of this dataset.

# slicing the dataset to get only attributes of interest
df_orders_items = df_orders_items[['order_id', 'order_item_id', 'product_id']]

# Is product_id the primary key of the products dataset
#print(\nChecking if product_id alone is the primary key of products dataset:\n', df_products['product_id'].duplicated().value_counts())

# Yes, product_id is the primary key of the products dataset

df_products = df_products[['product_id', 'product_category_name']].set_index('product_id')

df_orders_items_products = df_orders_items.join(df_products, on='product_id')

df_orders = df_orders[(df_orders['order_status'] == 'delivered') | (df_orders['order_status'] == 'invoiced')]
df_orders = df_orders[['order_id', 'customer_id']].set_index('order_id')

df_orders_items_products_customers = df_orders_items_products.join(df_orders, on='order_id') # New dataset

df_customers['customer_city_state'] = df_customers['customer_city'] + ', ' + df_customers['customer_state']
df_customers = df_customers[['customer_id', 'customer_city_state']].set_index('customer_id')

# Final dataset
df_orders_items_products_customers = df_orders_items_products_customers.join(df_customers, on='customer_id')
df_orders_items_products_customers = df_orders_items_products_customers[['order_id', 'product_category_name', 'customer_city_state']]
df_orders_items_products_customers.drop_duplicates(inplace=True)

df_orders_items_products_customers['product_category_name'].fillna(' ', inplace=True)
df_orders_items_products_customers['customer_city_state'].fillna(' ', inplace=True)

df_orders_items_products_customers_final = df_orders_items_products_customers[['product_category_name', 'customer_city_state']].drop_duplicates(ignore_index=True)
df_orders_items_products_customers_final['p_product_given_city_state_in_percentage'] = 0.0
df_orders_items_products_customers_final['p_city_state_given_product_in_percentage'] = 0.0
df_orders_items_products_customers_final['orders_num'] = 0

# No. of orders
orders_num = len(list(df_orders_items_products_customers['order_id'].unique()))

df_1 = df_orders_items_products_customers.groupby('product_category_name').count()['order_id'].to_frame().rename(columns={'order_id':'orders_num'})
df_1['p_product'] = df_1['orders_num'] / orders_num

df_2 = df_orders_items_products_customers.groupby('customer_city_state').count()['order_id'].to_frame().rename(columns={'order_id':'orders_num'})
df_2['p_city_state'] = df_2['orders_num'] / orders_num

for i in range(df_orders_items_products_customers_final.shape[0]):
    test_product = df_orders_items_products_customers_final.iloc[i]['product_category_name']
    test_city_state = df_orders_items_products_customers_final.iloc[i]['customer_city_state']

    numerator = df_orders_items_products_customers[(df_orders_items_products_customers['product_category_name'] == test_product) & (df_orders_items_products_customers['customer_city_state'] == test_city_state)].shape[0] / orders_num

    denominator1 = df_1.loc[test_product]['p_product']
    denominator2 = df_2.loc[test_city_state]['p_city_state']
    
    df_orders_items_products_customers_final.loc[i, 'p_city_state_given_product_in_percentage'] = numerator / denominator1 * 100.0
    df_orders_items_products_customers_final.loc[i, 'p_product_given_city_state_in_percentage'] = numerator / denominator2 * 100.0
    df_orders_items_products_customers_final.loc[i, 'orders_num'] = df_orders_items_products_customers[(df_orders_items_products_customers['product_category_name'] == test_product) & (df_orders_items_products_customers['customer_city_state'] == test_city_state)].shape[0]

df_orders_items_products_customers_final.to_excel('conditional probability statistics.xlsx', index=False)
