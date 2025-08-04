import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from greeks import compute_european_greeks, compute_american_greeks
from black_scholes import black_scholes
from binomial_tree import binomial_tree_price

st.set_page_config("wide")
st.title("Finance Options Pricing Project")
with st.sidebar:
    st.header("Created by Michael Matsuda")

    st.subheader('Black-Scholes Pricing')
    S = st.number_input("Current Asset Price ($)", value=100.00, step=0.01, min_value=0.00, format="%.2f")
    K = st.number_input("Strike Price ($)", value=100.00, step=0.01, min_value=0.00, format="%.2f")
    T = st.number_input("Time to Maturity (Years)", value=1.00, step=0.01, min_value=0.00, format="%.2f")
    sigma = st.number_input("Volatility (σ)", value= 0.02, step=0.01, min_value=0.00, format="%.2f")
    r = st.number_input("Risk-free interest rate (annualized)", value=0.05, step=0.01, min_value=0.00, format="%.2f")

    st.subheader('Binomial Tree Pricing')
    N = st.number_input("Number of Binomial Trees", value=100, step=1, min_value=1, format="%d")

    st.subheader('American Greeks Step values')
    epsilonS = st.number_input("Small step in Current Asset Price ($)", value = 0.01*S, step=0.01, min_value=0.00, format="%.3f")
    epsilonSigma = st.number_input("Small step in Volatility", value = 0.0001, step=0.0001, min_value=0.00, format="%.4f")
    epsilonT = st.number_input("1/365th of a year, as Standard Unit for Daily Decay", value = 1/365, step=0.01, min_value=0.00, format="%.4f")
    epsilonr = st.number_input("Small step in interest rate percentage",value = 0.0001, step=0.0001, min_value=0.00, format="%.4f")

    st.write("Connect with me on LinkedIn!")
    linkedin_badge_code = """<script src="https://platform.linkedin.com/badges/js/profile.js" async defer type="text/javascript"></script>
       <div class="badge-base LI-profile-badge" data-locale="en_US" data-size="medium" data-theme="light" data-type="VERTICAL" data-vanity="michaelmatsuda" data-version="v1"><a class="badge-base__link LI-simple-link" </a></div>
                 """
    st.components.v1.html(linkedin_badge_code, height=330, scrolling=False)

data1 = {
    'Current Asset Price': [S],
    'Strike Price': [K],
    'Time to Maturity': [T],
    'Volatility': [sigma],
    'Risk-free interest rate': [r],
}

st.title ("Black-Scholes Pricing")
st.write("Calculate the price of a European stock option using the Black-Scholes pricing method.")
df1 = pd.DataFrame(data1)
st.dataframe(df1,hide_index=True)
BScallPrice = black_scholes(S, K, T, sigma, r, 'call')
BSputPrice = black_scholes(S, K, T, sigma, r, 'put')

BScol1, BScol2, BScol3, BScol4 = st.columns(4)
with BScol1:
    st.subheader("Call Value:")
with BScol2:
    st.subheader(f"$ {BScallPrice:.2f}")
with BScol3:
    st.subheader("Put Value:")
with BScol4:
    st.subheader(f"$ {BSputPrice:.2f}")

st.title("Greeks")
st.write("Calculate the European stock options' Greek ratios based on the Black-Scholes pricing method.")
euro_call_greeks = compute_european_greeks(S, K, T, r, sigma)
df_euro_greeks_call = {key: [value] for key, value in euro_call_greeks.items()}
df_euro_greeks_call = pd.DataFrame(df_euro_greeks_call)

euro_put_greeks = compute_european_greeks(S, K, T, r, sigma, 'put')
df_euro_greeks_put = {key: [value] for key, value in euro_put_greeks.items()}
df_euro_greeks_put = pd.DataFrame(df_euro_greeks_put)

st.header("Call Greeks")
st.dataframe(df_euro_greeks_call, hide_index=True)

st.header("Put Greeks")
st.dataframe(df_euro_greeks_put, hide_index=True)

data2 = {
'Current Asset Price': [S],
    'Strike Price': [K],
    'Time to Maturity': [T],
    'Volatility': [sigma],
    'Number of Binomial Trees': [N],
    'Risk-free interest rate': [r],
}
st.title("Binomial Tree Pricing")
st.write("Calculate the price of an american stock option using the Binomial Tree Pricing method.")
df2 = pd.DataFrame(data2)
st.dataframe(df2, hide_index=True)

BTcallPrice = binomial_tree_price(S, K, T, sigma, r, N, 'call')
BTputPrice = binomial_tree_price(S, K, T, sigma, r, N, 'put')
BTcol1, BTcol2, BTcol3, BTcol4 = st.columns(4)
with BTcol1:
    st.subheader("Call Value:")
with BTcol2:
    st.subheader(f"$ {BTcallPrice:.2f}")
with BTcol3:
    st.subheader("Put Value:")
with BTcol4:
    st.subheader(f"$ {BTputPrice:.2f}")

st.title("American Option Greeks")
st.write("Calculate the Greeks of an american stock option using the standard central difference approximation.")

american_call_greeks = compute_american_greeks(S, K, T, r, sigma, N,'call', epsilonS, epsilonSigma, epsilonT, epsilonr)
df_american_call_greeks = {key: [value] for key, value in american_call_greeks.items()}
df_american_call_greeks = pd.DataFrame(df_american_call_greeks)

st.header("Call Greeks")
st.dataframe(df_american_call_greeks, hide_index=True)

american_put_greeks = compute_american_greeks(S, K, T, r, sigma, N,'put', epsilonS, epsilonSigma, epsilonT, epsilonr)
df_american_put_greeks = {key: [value] for key, value in american_put_greeks.items()}
df_american_put_greeks = pd.DataFrame(df_american_put_greeks)

st.header("Put Greeks")

st.dataframe(df_american_put_greeks, hide_index=True)

st.write("Created by Michael Matsuda, 2025")
