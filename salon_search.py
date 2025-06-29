#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import streamlit as st
import plotly.express as px


# In[2]:


#merged.csvを読み込む
merged_df = pd.read_csv('merged.csv')


# In[3]:


#streamlitの部品設定
st.title('サロンサーチ')

#フィルタ設定
price_limit = st.slider('最低カット価格の上限', 2000, 8500, 200, 6000)
score_limit = st.slider('大人気スコアの作成下限', 0.0, 35.0, 2.0, 5.0)


# In[7]:


#フィルタ処理
filtered_df = merged_df[
    (merged_df['price'] <= price_limit) &
    (merged_df['pop_score'] >= score_limit)
]


# In[11]:


#散布図の作成
fig = px.scatter(
    filtered_df,
    x = 'pop_score',
    y = 'price',
    hover_data = ['name_salon', 'access', 'star', 'review'],
    title = '人気スコアと最低カット価格の散布図'
)

st.plotly_chart(fig)


# In[12]:


# 詳細リンクの表示
selected_salon = st.selectbox('気になるサロンを選んで詳細を確認', filtered_df['name_salon'])

if selected_salon:
    url = filtered_df[filtered_df['name_salon'] == selected_salon]['link_detail'].values[0]
    st.markdown(f"[{selected_salon}のページへ移動]({url})", unsafe_allow_html=True)


# In[13]:


sort_key = st.selectbox(
    "ランキング基準を選んでください",
    ("star", "pop_score", "review", "price", "seats")
)

ascending = True if sort_key == "price" else False


# In[14]:


st.subheader(f"{sort_key}によるサロンランキング（上位10件）")

ranking_df = filtered_df.sort_values(by=sort_key, ascending=ascending).head(10)

# 必要な列だけ表示
st.dataframe(ranking_df[["name_salon", "price", "pop_score", "star", "review", "seats", "access"]])


# In[ ]:




