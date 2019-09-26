import plotly.express as px
import pandas as pd


prx = 30
l_rate = 200
p = 1

df = pd.read_csv('3d_Merged_Repaired_no_dups_mfcc_tsne_prx_' + str(prx) + '_l-rate_' + str(l_rate) + '_try_' + str(p) +'_v2stdscale.csv')

fig = px.scatter_3d(df, x='f1', y='f2', z='f3', color='color', text='Name')
fig.show()