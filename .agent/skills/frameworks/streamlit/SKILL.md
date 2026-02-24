---
name: streamlit
detect: ["streamlit", "st.title", "st.sidebar", "st.chat_input"]
version: "6.4.3"
category: frameworks
tier: 2
---

# Streamlit Patterns — DOMYH Awesome Code

> **Scope**: Data apps, ML model UIs, LLM chat interfaces
> **Framework**: Streamlit 1.30+
> **Deployment**: Streamlit Cloud, Docker, Cloud Run

---

## 🎯 When to Use This Skill

Use for: ML model demos, data dashboards, LLM chat UIs, quick prototypes.
**NOT for**: Production web apps (→ fastapi, nextjs), complex UIs (→ react).

---

## 📁 Project Structure

```
my-streamlit-app/
├── app.py                    # Main entry point
├── pages/                    # Multi-page app (auto-routed)
│   ├── 1_📊_Dashboard.py
│   ├── 2_🔮_Predict.py
│   └── 3_📈_Analytics.py
├── components/               # Custom components
│   └── sidebar.py
├── utils/                    # Helper functions
│   └── model_loader.py
├── .streamlit/
│   └── config.toml           # Theme & settings
├── Artifacts/                # ML models
│   ├── model.pkl
│   └── preprocessor.pkl
├── requirements.txt
├── Dockerfile
└── README.md
```

---

## 🧱 Core Patterns

### Basic App Structure

```python
# app.py
import streamlit as st

# ✅ Page config (must be first st call)
st.set_page_config(
    page_title="ML Predictor",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ✅ Title and description
st.title("🔮 ML Price Predictor")
st.markdown("Enter features below to get a prediction.")

# ✅ Sidebar
with st.sidebar:
    st.header("Settings")
    model_type = st.selectbox("Model", ["RandomForest", "GradientBoosting"])
    confidence = st.slider("Confidence Threshold", 0.0, 1.0, 0.8)

# ✅ Main content
col1, col2 = st.columns(2)
with col1:
    feature1 = st.number_input("Feature 1", min_value=0.0)
    feature2 = st.selectbox("Category", ["A", "B", "C"])
with col2:
    feature3 = st.slider("Feature 3", 0, 100, 50)
    feature4 = st.text_input("Name")

if st.button("🔮 Predict", type="primary"):
    with st.spinner("Predicting..."):
        prediction = model.predict(...)
        st.success(f"Prediction: **${prediction:,.2f}**")
        st.balloons()
```

### ML Model Serving UI

```python
# ✅ Load model with caching
import pickle

@st.cache_resource
def load_model():
    model = pickle.load(open("Artifacts/model.pkl", "rb"))
    preprocessor = pickle.load(open("Artifacts/preprocessor.pkl", "rb"))
    return model, preprocessor

model, preprocessor = load_model()

# ✅ Form-based input
with st.form("prediction_form"):
    st.subheader("Enter Features")
    
    carat = st.number_input("Carat", 0.1, 5.0, 1.0, step=0.1)
    cut = st.selectbox("Cut", ["Fair", "Good", "Very Good", "Premium", "Ideal"])
    color = st.selectbox("Color", ["D", "E", "F", "G", "H", "I", "J"])
    
    submitted = st.form_submit_button("Predict Price")
    
    if submitted:
        import pandas as pd
        input_df = pd.DataFrame([{
            "carat": carat, "cut": cut, "color": color,
        }])
        transformed = preprocessor.transform(input_df)
        prediction = model.predict(transformed)[0]
        
        st.metric("Predicted Price", f"${prediction:,.2f}")
```

### Chat Interface (LLM/Gemini)

```python
# ✅ Streamlit Chat UI (Gemini ChatBot pattern)
import streamlit as st
import google.generativeai as genai

st.title("💬 Gemini Chat")

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat" not in st.session_state:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel("gemini-pro")
    st.session_state.chat = model.start_chat(history=[])

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
if prompt := st.chat_input("Ask anything..."):
    # Display user message
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Get AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = st.session_state.chat.send_message(prompt)
            st.markdown(response.text)
    
    st.session_state.messages.append({
        "role": "assistant", "content": response.text,
    })
```

### File Upload and Processing

```python
# ✅ File upload (PDF, CSV, images)
uploaded_file = st.file_uploader(
    "Upload a file",
    type=["csv", "pdf", "png", "jpg"],
)

if uploaded_file is not None:
    if uploaded_file.type == "text/csv":
        import pandas as pd
        df = pd.read_csv(uploaded_file)
        st.dataframe(df)
        st.bar_chart(df.select_dtypes(include="number").iloc[:, :3])
    
    elif uploaded_file.type == "application/pdf":
        from PyPDF2 import PdfReader
        reader = PdfReader(uploaded_file)
        text = " ".join(page.extract_text() for page in reader.pages)
        st.text_area("PDF Content", text, height=300)
    
    elif uploaded_file.type.startswith("image"):
        st.image(uploaded_file, caption="Uploaded Image")
```

### Data Visualization

```python
# ✅ Built-in charts
st.line_chart(df[["col1", "col2"]])
st.bar_chart(df["category"].value_counts())
st.area_chart(df[["revenue", "cost"]])

# ✅ Metrics
col1, col2, col3 = st.columns(3)
col1.metric("Accuracy", "94.2%", "+1.2%")
col2.metric("F1 Score", "0.91", "+0.03")
col3.metric("Latency", "45ms", "-5ms")

# ✅ Matplotlib/Seaborn/Plotly
import matplotlib.pyplot as plt
fig, ax = plt.subplots()
ax.scatter(df["x"], df["y"])
st.pyplot(fig)

# ✅ Plotly (interactive)
import plotly.express as px
fig = px.scatter(df, x="carat", y="price", color="cut")
st.plotly_chart(fig, use_container_width=True)
```

---

## 🚀 Deployment

### Streamlit Cloud
```toml
# .streamlit/config.toml
[theme]
primaryColor = "#F63366"
backgroundColor = "#0E1117"
secondaryBackgroundColor = "#262730"
textColor = "#FAFAFA"

[server]
maxUploadSize = 200
```

### Docker
```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

---

## ✅ Streamlit Checklist

- [ ] `st.set_page_config()` as first call
- [ ] Session state for persistent data
- [ ] `@st.cache_resource` for models
- [ ] `@st.cache_data` for data loading
- [ ] Error handling with `st.error()`
- [ ] Loading indicators (`st.spinner()`)
- [ ] Responsive layout (`st.columns()`)

---

_DOMYH Awesome Code • Streamlit Patterns • v7.0_
