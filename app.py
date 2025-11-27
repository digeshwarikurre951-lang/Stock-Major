import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Your data and models from previous steps (df, rf_model, rmse_rf)

def ai_stock_chatbot(query, df, rf_model=None):
    """Complete AI Stock Chatbot - No external dependencies"""
    query = query.lower()
    
    # Latest data
    latest_price = df['Close'].iloc[-1]
    latest_date = df['Date'].iloc[-1].strftime('%Y-%m-%d')
    latest_rsi = df['RSI'].iloc[-1]
    avg_sentiment = df['Sentiment'].mean()
    
    responses = {
        "price": f"**Latest Apple closing price: ${latest_price:.2f}** (as of {latest_date})",
        "current price": f"**Latest Apple closing price: ${latest_price:.2f}** (as of {latest_date})",
        "prediction": f"**Model RMSE: {rmse_rf:.2f}**. Random Forest predicts next day price using Close, MA, RSI, Sentiment features.",
        "forecast": f"**Model RMSE: {rmse_rf:.2f}**. Random Forest predicts next day price using Close, MA, RSI, Sentiment features.",
        "sentiment": f"**Average sentiment: {avg_sentiment:.3f}** (range: {df['Sentiment'].min():.3f} to {df['Sentiment'].max():.3f})",
        "rsi": f"**Latest RSI: {latest_rsi:.1f}** - {'🔴 Overbought (>70)' if latest_rsi > 70 else '🟢 Oversold (<30)' if latest_rsi < 30 else '🟡 Neutral'}",
        "trend": f"**20-day MA: ${df['MA_20'].iloc[-1]:.2f}** vs Current: ${latest_price:.2f} {'📈 Above MA' if latest_price > df['MA_20'].iloc[-1] else '📉 Below MA'}",
        "performance": f"**Random Forest RMSE: {rmse_rf:.2f}** - Lower is better for price prediction accuracy.",
        "data": f"**Dataset: {len(df)} days** of Apple stock data with technical indicators and sentiment analysis."
    }
    
    for key, response in responses.items():
        if key in query:
            return response
    
    return "🤖 I can answer about **price**, **prediction**, **sentiment**, **RSI**, **trend**, or **performance**. Ask me anything about Apple stock!"

# Streamlit Chat Interface
st.title("🎯 AI Stock Dashboard + Chatbot")
st.markdown("---")

# Quick Stats Cards
col1, col2, col3, col4 = st.columns(4)
col1.metric("Latest Price", f"${df['Close'].iloc[-1]:.2f}")
col2.metric("RSI", f"{df['RSI'].iloc[-1]:.1f}", f"{df['RSI'].iloc[-1] - df['RSI'].iloc[-2]:+.1f}")
col3.metric("Sentiment", f"{df['Sentiment'].mean():.3f}")
col4.metric("Model RMSE", f"{rmse_rf:.2f}")

# Price Chart
st.header("📈 Price Chart")
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(df['Date'], df['Close'], label='Close Price', linewidth=2)
ax.plot(df['Date'], df['MA_20'], label='20-day MA', alpha=0.7)
ax.set_title('Apple Stock Price & Moving Average')
ax.legend()
ax.grid(True, alpha=0.3)
st.pyplot(fig)

# AI CHATBOT
st.header("🤖 AI Stock Analyst")
st.markdown("Ask about price, predictions, sentiment, RSI, trends...")

# Chat messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Type your question about Apple stock..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Generate response
    with st.chat_message("assistant"):
        response = ai_stock_chatbot(prompt, df)
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

# Instructions
with st.expander("💡 Quick Questions to Try"):
    st.code("""
    "What's the current price?"
    "What is the prediction accuracy?"
    "How is the sentiment?"
    "What is RSI status?"
    "What is the trend?"
    """)
