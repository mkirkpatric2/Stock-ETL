import pandas as pd
import seaborn as sns
from datetime import date
import matplotlib.pyplot as plt
import boto3


client = boto3.client('s3')
df = pd.read_csv("s3://stock-data-buck1/msft-daily-data.csv")
sns.set_theme()
df['date_ordinal'] = pd.to_datetime(df['date']).apply(lambda date: date.toordinal())

# Make first graph - historical open v. date.
graph = sns.lmplot(data=df, x='date_ordinal', y='open', fit_reg=False)
graph.set(xlabel='Date', ylabel='Open', title="Historical MSFT Open price data")
newlabels = [date.fromordinal(int(item)) for item in graph.axes[0, 0].get_xticks()]
graph.set(xticklabels=newlabels)
graph.axes[0, 0].set_xticklabels(graph.axes[0, 0].get_xticklabels(), rotation=30, horizontalalignment='right')

# Save graph. Push graph to bucket.
plt.savefig("plot1.png", dpi=900, bbox_inches='tight')
client.upload_file("./plot1.png", "stock-data-buck1", "plot1.png")

# Make second graph - historical open-close data. Save graph as image. push graph to bucket.
df['open_close_diff'] = df['open'] - df['close']
graph2 = sns.lmplot(data=df, x='date_ordinal', y='open_close_diff', fit_reg=False)
graph2.set(xlabel='Date', ylabel='Difference between Open and Close prices',
           title='Historical (Open - Close) MSFT data')
newlabels = [date.fromordinal(int(item)) for item in graph2.axes[0, 0].get_xticks()]
graph2.set(xticklabels=newlabels)
graph2.axes[0, 0].set_xticklabels(graph2.axes[0, 0].get_xticklabels(), rotation=30, horizontalalignment='right')

# Save graph. Push graph to bucket.
plt.savefig("plot2.png", dpi=900, bbox_inches='tight')
client.upload_file("./plot2.png", "stock-data-buck1", "plot2.png")

# Make third graph - 30day high data. Save graph as image. push graph to bucket.
df30 = df.head(30)
graph3 = sns.lmplot(data=df30, x='date_ordinal', y='high', fit_reg=True)
graph3.set(xlabel='Date', ylabel='Daily High', title='30-Day MSFT daily-highs')
newlabels = [date.fromordinal(int(item)) for item in graph3.axes[0, 0].get_xticks()]
graph3.set(xticklabels=newlabels)
graph3.axes[0, 0].set_xticklabels(graph3.axes[0, 0].get_xticklabels(), rotation=30, horizontalalignment='right')

# Save graph. Push graph to bucket.
plt.savefig("plot3.png", dpi=900, bbox_inches='tight')
client.upload_file("./plot3.png", "stock-data-buck1", "plot3.png")

# Make fourth graph - 30day high data. Save graph as image. push graph to bucket.
df30['high_low_diff'] = df30['high'] - df30['low']
graph4 = sns.lmplot(data=df30, x='date_ordinal', y='high_low_diff', fit_reg=True)
graph4.set(xlabel='Date', ylabel='Difference between daily high and daily low', title="30-Day (High-Low) MSFT Data")
newlabels = [date.fromordinal(int(item)) for item in graph4.axes[0, 0].get_xticks()]
graph4.set(xticklabels=newlabels)
graph4.axes[0, 0].set_xticklabels(graph4.axes[0, 0].get_xticklabels(), rotation=30, horizontalalignment='right')

# Save graph. Push graph to bucket.
plt.savefig("plot4.png", dpi=900, bbox_inches='tight')
client.upload_file("./plot4.png", "stock-data-buck1", "plot4.png")

exit()
