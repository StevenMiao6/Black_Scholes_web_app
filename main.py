import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

from scipy.stats import norm

import math

def black_scholes(S, K, T, r, sigma, option='call'):
    d1 = (math.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - (sigma * math.sqrt(T))

    if option == 'call':
        return S * norm.cdf(d1) - K * math.exp(-r * T) * norm.cdf(d2)
    if option == 'put':
        return K * math.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)

# use the entire page width
st.set_page_config(page_title='Home', layout='wide',)

st.title('Black-Scholes model')
data = pd.read_csv('BSM input.csv')

if 'S' not in st.session_state:
    st.session_state['S'] = data.iloc[0, 0]
if 'K' not in st.session_state:
    st.session_state['K'] = data.iloc[0, 1]
if 'T' not in st.session_state:
    st.session_state['T'] = data.iloc[0, 2]
if 'sigma' not in st.session_state:
    st.session_state['sigma'] = data.iloc[0, 3]
if 'r' not in st.session_state:
    st.session_state['r'] = data.iloc[0, 4]
if 'min_spot' not in st.session_state:
    st.session_state['min_spot'] = st.session_state['S'] - 20
if 'max_spot' not in st.session_state:
    st.session_state['max_spot'] = st.session_state['S'] + 20
if 'min_sigma' not in st.session_state:
    st.session_state['min_sigma'] = 0.01
if 'max_sigma' not in st.session_state:
    st.session_state['max_sigma'] = 0.01

# parameter input for BS model on the sidebar
with st.sidebar:
    st.header('Black-Scholes Parameters', divider='red')
    st.session_state['S'] = st.number_input("Current price of underlying ($S_{t}$)", value=st.session_state['S'])
    st.session_state['K'] = st.number_input("Strike price ($K$)", value=st.session_state['K'])
    st.session_state['T'] = st.number_input("Time to maturity (Years)", value=st.session_state['T'])
    st.session_state['sigma'] = st.number_input("Volatility", value=st.session_state['sigma'])
    st.session_state['r'] = st.number_input("Risk-free interest rate ($r$)", value=st.session_state['r'])

# update dataframe accordingly after changes in the sidebar
data.iloc[0, 0] = st.session_state['S']
data.iloc[0, 1] = st.session_state['K']
data.iloc[0, 2] = st.session_state['T']
data.iloc[0, 3] = st.session_state['sigma']
data.iloc[0, 4] = st.session_state['r']

# display updated dataframe
st.dataframe(data, width=2000)

# custom CSS to style the boxes and center the text
st.markdown("""
    <style>
    .price-box {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: flex-start;
        height: 80px;  /* Adjusted height to accommodate both text and price */
        color: black;
        font-size: 15px;
        font-weight: normal;
        border-radius: 10px;
        margin: 10px 0;
        padding-top: 10px;  /* Added padding to create space from the top */
    }
    .call-price {
        background-color: #93e4c1;
    }
    .put-price {
        background-color: #ffcbcb;
    }
    .price-value {
        margin-top: auto;
        padding-bottom: 10px;  /* Added padding to create space from the bottom */
        font-size: 24px;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

call_display, put_display = st.columns(2)

call_price = black_scholes(S=st.session_state['S'], K=st.session_state['K'], T=st.session_state['T'], r=st.session_state['r'], sigma=st.session_state['sigma'], option='call')
put_price = black_scholes(S=st.session_state['S'], K=st.session_state['K'], T=st.session_state['T'], r=st.session_state['r'], sigma=st.session_state['sigma'], option='put')

call_price_format = '${:.2f}'.format(call_price)
put_price_format = '${:.2f}'.format(put_price)

with call_display:
    st.markdown(f'<div class="price-box call-price"><div>CALL price</div><div class="price-value">{call_price_format}</div></div>', unsafe_allow_html=True)

with put_display:
    st.markdown(f'<div class="price-box put-price"><div>PUT price</div><div class="price-value">{put_price_format}</div></div>', unsafe_allow_html=True)

st.title('Options Price - Interactive Heatmap')

# parameter input for heatmap
with st.sidebar:
    st.divider()
    st.header('Heatmap Parameters', divider='green')
    st.session_state['min_spot'] = st.number_input("Min spot price", min_value=0.01, value= st.session_state['min_spot'])
    st.session_state['max_spot'] = st.number_input("Max spot price", min_value=0.01, value= st.session_state['max_spot'])
    st.session_state['min_sigma'] = st.slider("Min volatility for Heatmap", min_value=0.01, max_value=1.00, step=0.01, value=st.session_state['min_sigma'])
    st.session_state['max_sigma'] = st.slider("Max volatility for Heatmap", min_value=0.01, max_value=1.00, step=0.01,  value=st.session_state['max_sigma'])

call_heatmap, put_heatmap = st.columns(2)

x = np.linspace(st.session_state['min_spot'], st.session_state['max_spot'], 10)
y = np.linspace(st.session_state['min_sigma'], st.session_state['max_sigma'], 10)

# calculate option prices for the heatmap
call_prices_heatmap = np.zeros((len(y), len(x)))
put_prices_heatmap = np.zeros((len(y), len(x)))
for i, vol in enumerate(y):
    for j, spot in enumerate(x):
        call_prices_heatmap[i, j] = black_scholes(S=spot, K=st.session_state['K'], T=st.session_state['T'], r=st.session_state['r'], sigma=vol, option='call')
        put_prices_heatmap[i, j] = black_scholes(S=spot, K=st.session_state['K'], T=st.session_state['T'], r=st.session_state['r'], sigma=vol, option='put')
        
df_call_heatmap = pd.DataFrame(call_prices_heatmap, index=np.round(y, 2), columns=np.round(x, 2))
df_put_heatmap = pd.DataFrame(put_prices_heatmap, index=np.round(y, 2), columns=np.round(x, 2))

# Plot the heatmap for call
with call_heatmap:
    plt.figure(figsize=(10, 8))
    sns.heatmap(df_call_heatmap, annot=True, cmap='RdYlGn', fmt='.2f')
    plt.title('CALL Prices')
    plt.xlabel('Underlying Price')
    plt.ylabel('Volatility')
    st.pyplot(plt)

with put_heatmap:
    plt.figure(figsize=(10, 8))
    sns.heatmap(df_put_heatmap, annot=True, cmap='RdYlGn', fmt='.2f')
    plt.title('PUT Prices')
    plt.xlabel('Underlying Price')
    plt.ylabel('Volatility')
    st.pyplot(plt)

st.title('P&L Calculator')

# parameter input for P&L
with st.sidebar:
    st.divider()
    st.header('P&L parameters', divider='blue')
    call_purchase = st.number_input("CALL purchase price", min_value=0.01, value=call_price, key='call_purchase')
    put_purchase = st.number_input("PUT purchase price", min_value=0.01, value=put_price, key='put_purchase')

call_pnl = call_purchase - call_price
put_pnl = put_purchase - put_price

call_pnl_format = '${:.2f}'.format(call_pnl)
put_pnl_format = '${:.2f}'.format(put_pnl)

call_pnl_color = 'price-box call-price' if call_pnl>=0 else 'price-box put-price'
put_pnl_color = 'price-box call-price' if put_pnl>=0 else 'price-box put-price'

call_pnl_display, put_pnl_display = st.columns(2)

with call_pnl_display:
    st.markdown(f'<div class="{call_pnl_color}"><div>CALL P&L</div><div class="price-value">{call_pnl_format}</div></div>', unsafe_allow_html=True)

with put_pnl_display:
    st.markdown(f'<div class="{put_pnl_color}"><div>PUT P&L</div><div class="price-value">{put_pnl_format}</div></div>', unsafe_allow_html=True)
