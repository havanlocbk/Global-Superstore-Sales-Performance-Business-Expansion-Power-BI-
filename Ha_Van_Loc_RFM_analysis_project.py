import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
#python test.py

# IMPORT DATA
main_data = pd.read_excel(r"G:\Other computers\Current Use 2025\Google Drive - havanloc\Learning path\UniGap\Python\Final_project_RFM\ecommerce retail.xlsx", sheet_name="ecommerce retail")
print(main_data.head())  
#-------------------------------
# EXPLORE DATA
# Check null values & data type
print(main_data.info())

# Get summary statistics
print(main_data.describe())

#Check for null values
print(main_data.isnull().sum())
#-------------------------------
#CORRECT DATA TYPES 
#Change type CustomerID from float64 into int64
main_data['CustomerID'] = main_data['CustomerID'].astype('Int64')
print(main_data['CustomerID'].dtype)

#Change InvoiceDate to datetime64[ns] format 
main_data['InvoiceDate'] = pd.to_datetime(main_data['InvoiceDate'], errors='coerce')
#-------------------------------
#AND HANDLE NULL VALUES

#Handle NULL value in CustomerID - delete rows with null CustomerID
main_data = main_data[main_data['CustomerID'].notnull()]

#-------------------------------
#FILTER DATA

#Filter delivered trainsactions: nquantity > 0 ad UnitPrice > 0
main_data = main_data[(main_data['Quantity'] > 0) & (main_data['UnitPrice'] > 0)]

#Filter Filter StockCode within 4 to 7 letter and Eliminate Description within this list: postage, bank charges, Carriage, Manual
main_data = main_data[main_data['StockCode'].str.match(r'^[A-Za-z0-9]{4,7}$') & \
                      main_data['Description'].str.contains('POSTAGE|Bank Charges|CARRIAGE|Next Day Carriage|Manual', case=False, na=False)] 

#-------------------------------
# DOUBLE CHECK DATANBASE AFTER CLEANING
# Check null values & data type
print(main_data.info())

# Get summary statistics
print(main_data.describe())

#Check for null values
print(main_data.isnull().sum())

#-------------------------------
#CALCULATE RFM METRICS
#Add TotalPrice column
main_data['TotalPrice'] = main_data['Quantity'] * main_data['UnitPrice']

# Calculate Recency - Calculate the number of days since 31/12/2011
snapshot_date = pd.to_datetime('2011-12-31')
recency = main_data.groupby('CustomerID')['InvoiceDate'].max().reset_index()
recency['Recency'] = (snapshot_date - recency['InvoiceDate']).dt.days

#Calculate Frequency - Calculate the number of orders for each customer
frequency = main_data.groupby('CustomerID')['InvoiceNo'].nunique().reset_index()
frequency.columns = ['CustomerID', 'Frequency']

#Moneytary - Calculate sum of purchase amount for each customer
monetary = main_data.groupby('CustomerID')['TotalPrice'].sum().reset_index()
monetary.columns = ['CustomerID', 'Monetary']

# Combine Recency, Frequency, Monetary
rfm = recency[['CustomerID', 'Recency']].merge(frequency, on='CustomerID').merge(monetary, on='CustomerID')
print(rfm)

#RFM Score Calculation
rfm['R_Score'] = pd.qcut(rfm['Recency'], 5, labels=[5,4,3,2,1]) # Higher recency means lower score
rfm['F_Score'] = pd.qcut(rfm['Frequency'].rank(method='first'), 5, labels=[1,2,3,4,5]) # Higher frequency means higher score #duplicates='drop'
rfm['M_Score'] = pd.qcut(rfm['Monetary'], 5, labels=[1,2,3,4,5]) # Higher monetary means higher score
rfm['RFM_Score'] = rfm['R_Score'].astype(str) + rfm['F_Score'].astype(str) + rfm['M_Score'].astype(str) # Concatenate R, F, M scores to create RFM score


#Segment customers based on RFM score
segment_map = {
    'Champions': ['555', '554', '544', '545', '454', '455', '445'],
    'Loyal': ['543', '444', '435', '355', '354', '345', '344', '335'],
    'Potential Loyalist': ['553', '551', '552', '541', '542', '533', '532', '531', '452', '451', '442', '441', '431', '453', '433', '432', '423', '353', '352', '351', '342', '341', '333', '323'],
    'New Customers': ['512', '511', '422', '421', '412', '411', '311'],
    'Promising': ['525', '524', '523', '522', '521', '515', '514', '513', '425', '424', '413', '414', '415', '315', '314', '313'],
    'Need Attention': ['535', '534', '443', '434', '343', '334', '325', '324'],
    'About To Sleep': ['331', '321', '312', '221', '213', '231', '241', '251'],
    'At Risk': ['255', '254', '245', '244', '253', '252', '243', '242', '235', '234', '225', '224', '153', '152', '145', '143', '142', '135', '134', '133', '125', '124'],
    'Cannot Lose Them': ['155', '154', '144', '214', '215', '115', '114', '113'],
    'Hibernating customers': ['332', '322', '233', '232', '223', '222', '132', '123', '122', '212', '211'],
}
def assign_segment(rfm_score):
    for segment, scores in segment_map.items():
        if rfm_score in scores:
            return segment
    return 'Lost customers'

rfm['Segment'] = rfm['RFM_Score'].apply(assign_segment)

print(rfm)
print(rfm.info())
print(rfm.describe())
#-------------------------------
#VISUALIZE RFM SEGMENTS
#Histogram: show distribution of each variable of the model
fig, ax = plt.subplots(figsize=(12, 3))
sns.histplot(rfm['Recency'], kde=True)
ax.set_title('Distribution of Recency')
plt.show()

fig, ax = plt.subplots(figsize=(12, 3))
sns.histplot(rfm['Frequency'], kde=True)
ax.set_title('Distribution of Frequency')
plt.show()

fig, ax = plt.subplots(figsize=(12, 3))
sns.histplot(rfm['Monetary'], kde=True)
ax.set_title('Distribution of Monetary')
plt.show()

#Treemap:
#Segment by customer:
temp_rfm = rfm.groupby('Segment')['CustomerID'].count().reset_index()
temp_rfm.columns = ['Segment', 'Cust_count']

temp_rfm['Count_share'] = temp_rfm['Cust_count'] / (temp_rfm['Cust_count'].sum())

import squarify

colors = ['#FF0000', '#00FFFF', '#FFFFAA', '#A52A2A', '#800080', '#00FF00', '#808000', '#FF0CB3', '#FFA500', '#FF00FF', '#736F6E']

fig, ax = plt.subplots(1, figsize = (15,8))

squarify.plot(sizes=temp_rfm['Cust_count'],
              label=temp_rfm['Segment'],
              value=[f'{x*100:.2f}%' for x in temp_rfm['Count_share']],
              alpha=.8,
              color=colors,
              bar_kwargs=dict(linewidth=1.5, edgecolor="White")
             )

plt.title('RFM Segments of Customer Count', fontsize=16)
plt.axis('off')
plt.show()

#Bar chart: show the number of customers in each segment
fig, ax = plt.subplots(figsize=(12, 6))
sns.countplot(data=rfm, x='Segment', order=rfm['Segment'].value_counts().index, palette='viridis')
plt.title('Number of Customers in Each Segment')
plt.xticks(rotation=45)
plt.xlabel('Segment')
plt.ylabel('Number of Customers')
plt.show()

# Box Plot of RFM metrics by Segment
fig, axes = plt.subplots(3, 1, figsize=(15, 18)) # 3 hàng, 1 cột cho R, F, M

# Box Plot cho Recency
sns.boxplot(x='Segment', y='Recency', data=rfm.sort_values('Segment'), palette='viridis', ax=axes[0])
axes[0].set_title('Recency Distribution by Customer Segment', fontsize=16)
axes[0].set_xlabel('Customer Segment')
axes[0].set_ylabel('Recency (Days)')
axes[0].tick_params(axis='x', rotation=45)

# Box Plot cho Frequency
sns.boxplot(x='Segment', y='Frequency', data=rfm.sort_values('Segment'), palette='viridis', ax=axes[1])
axes[1].set_title('Frequency Distribution by Customer Segment', fontsize=16)
axes[1].set_xlabel('Customer Segment')
axes[1].set_ylabel('Frequency (Number of Orders)')
axes[1].tick_params(axis='x', rotation=45)

# Box Plot cho Monetary
sns.boxplot(x='Segment', y='Monetary', data=rfm.sort_values('Segment'), palette='viridis', ax=axes[2])
axes[2].set_title('Monetary Distribution by Customer Segment', fontsize=16)
axes[2].set_xlabel('Customer Segment')
axes[2].set_ylabel('Monetary (Total Price)')
axes[2].tick_params(axis='x', rotation=45)

plt.tight_layout() # Điều chỉnh layout để tránh các biểu đồ chồng chéo
plt.show()
#-------------------------------