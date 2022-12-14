import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
from sklearn.preprocessing import StandardScaler
from sklearn.manifold import TSNE
from feature_engine.outliers import Winsorizer
from sklearn.cluster import KMeans
import seaborn as sns
import base64
from io import BytesIO
print("IMPORTS DONE")

class kmeanPrediction:
    def __init__(self,dataset):
        self.df = dataset        
    
    def cleanData(self):            
        self.df  = self.df[self.df.Country == "United Kingdom"]
        self.df =  self.df[self.df.Quantity > 0]
        self.df['InvoiceDate'] = pd.to_datetime(self.df['InvoiceDate'])
        self.df['InvoiceYearMonth'] = self.df['InvoiceDate'].map(lambda date: 100*date.year + date.month)
        self.df['Date'] = self.df['InvoiceDate'].dt.strftime('%Y-%m')

    def plot_img_graph(self):

        buffer = BytesIO()
        plt.savefig(buffer, format="png", dpi = 300) 
        graph = base64.b64encode(buffer.getvalue()).decode("utf-8").replace("\n", "")
        buffer.close()

        return graph

    def plot_purchases(self):
        df_agg= self.df.groupby("Date").Quantity.sum()
        df_agg=pd.DataFrame(df_agg).reset_index()
        x=df_agg.Date
        y=df_agg.Quantity
        plt.switch_backend("AGG")
        plt.figure(figsize=(10,5), dpi=100)
        plt.gca().set(title="AMOUNT OF PRODUCTS SOLD PER MONTH", xlabel="Date", ylabel="Quantity")
        plt.plot(x, y, color='tab:Blue', marker='o')
        plt.tight_layout()
        graph = self.plot_img_graph()
        return graph

    def create_RFM_TABLE(self):
        NOW = dt.date(2011,12,9) 
        self.df['Date'] = pd.DatetimeIndex(self.df.InvoiceDate).date    
        df_recency = self.df.groupby(['CustomerID'],as_index=False)['Date'].max()
        df_recency.columns = ['CustomerID','Last_Purchase_Date']
        df_recency['Recency'] = df_recency.Last_Purchase_Date.apply(lambda x:(NOW - x).days)
        df_recency.drop(columns=['Last_Purchase_Date'],inplace=True)
        self.df['Revenue'] = self.df['Quantity']*self.df['UnitPrice']
        FM_Table = self.df.groupby('CustomerID').agg({'InvoiceNo'   : lambda x:len(x),
                                                'Revenue'  : lambda x:x.sum()})
        FM_Table.rename(columns = {'InvoiceNo' :'Frequency',
                                'Revenue':'Monetary'},inplace= True)
        RFM_Table = df_recency.merge(FM_Table,left_on='CustomerID',right_on='CustomerID')

        return RFM_Table

    def RScore(self,x,p,d):
        if x <= d[p][0.25]:
            return 1
        elif x <= d[p][0.50]:
            return 2
        elif x <= d[p][0.75]: 
            return 3
        else:
            return 4
    
    def FMScore(self,x,p,d):
        if x <= d[p][0.25]:
            return 4
        elif x <= d[p][0.50]:
            return 3
        elif x <= d[p][0.75]: 
            return 2
        else:
            return 1

    def create_RFM_Quantiles(self):
        self.RFM_Table = self.create_RFM_TABLE()  
        quantiles = self.RFM_Table.quantile(q=[0.25,0.50,0.75])
        quantiles = quantiles.to_dict()
        segmented_rfm = self.RFM_Table.copy()    
        segmented_rfm['R_quartile'] = segmented_rfm['Recency'].apply(self.RScore, args=('Recency',quantiles))
        segmented_rfm['F_quartile'] = segmented_rfm['Frequency'].apply(self.FMScore, args=('Frequency',quantiles))
        segmented_rfm['M_quartile'] = segmented_rfm['Monetary'].apply(self.FMScore, args=('Monetary',quantiles))
        segmented_rfm['RFM_Segment'] = segmented_rfm.R_quartile.map(str)+segmented_rfm.F_quartile.map(str)+segmented_rfm.M_quartile.map(str)
        segmented_rfm['RFM_Score'] = segmented_rfm[['R_quartile','F_quartile','M_quartile']].sum(axis=1)
        purchase_data = []
        pData = {
            "Best_Customers": len(segmented_rfm[segmented_rfm['RFM_Segment']=='111']),
            "Loyal_Customers":len(segmented_rfm[segmented_rfm['F_quartile']==1]),
            "Big_Spender" : len(segmented_rfm[segmented_rfm['M_quartile']==1]),
            "Almost_Lost"  :  len(segmented_rfm[segmented_rfm['RFM_Segment']=='134']),
            "Lost_Customers" : len(segmented_rfm[segmented_rfm['RFM_Segment']=='344']),
            "Lost_Cheap_Customers"  : len(segmented_rfm[segmented_rfm['RFM_Segment']=='444'])
        }
        purchase_data.append(pData)
        return purchase_data

    def create_model(self):
        RFM_Table_New = self.RFM_Table.drop('CustomerID', axis=1)
        df_rfm_log = RFM_Table_New.copy()
        df_rfm_log = np.log(df_rfm_log+1)
        
        # New LINE TO UPDATE
        df_rfm_log.fillna(0, inplace= True)
        windsoriser = Winsorizer(tail='both',fold=2,variables=[ 'Recency', 'Frequency', 'Monetary'])
        windsoriser.fit(df_rfm_log)
        df_rfm_log = windsoriser.transform(df_rfm_log)
        scaler = StandardScaler()
        scaler.fit(df_rfm_log)
        RFM_Table_New_scaled = scaler.transform(df_rfm_log)
        RFM_Table_New_scaled = pd.DataFrame(RFM_Table_New_scaled, columns=RFM_Table_New.columns)
        return RFM_Table_New_scaled

    def kmeans(self, normalised_df_rfm, clusters_number, original_df_rfm):
        
        kmeans = KMeans(n_clusters = clusters_number, random_state = 1)
        kmeans.fit(normalised_df_rfm)
        cluster_labels = kmeans.labels_
            
        df_new = original_df_rfm.assign(Cluster = cluster_labels)
        
        model = TSNE(random_state=1)
        transformed = model.fit_transform(df_new)
        plt.title('Graph of {} Clusters'.format(clusters_number))
        sns.scatterplot(x=transformed[:,0], y=transformed[:,1], hue=cluster_labels, style=cluster_labels, palette="Set1")

        clusters_graph = self.plot_img_graph()
        df_new.drop(columns = ["Recency","Frequency","Monetary"], inplace =True)
        df_new.head()
        df_new  = df_new.to_json()
        return clusters_graph, df_new
    
    def plot_clusters(self):   
        RFM_Table_New_scaled = self.create_model()
        plt.figure(figsize=(10, 10))
        plt.subplot(3, 1, 2)
        clusters_graph, df_rfm_k5 = self.kmeans(RFM_Table_New_scaled, 5, self.RFM_Table)
      
        return clusters_graph, df_rfm_k5
#mudzingwa1