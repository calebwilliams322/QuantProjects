FROM python:3.11-slim

WORKDIR /imp_vol_surface

# Copy and install requirements explicitly
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy all your app files explicitly
COPY . .

# Expose Streamlit default port
EXPOSE 8501

# Run your Streamlit app explicitly
ENTRYPOINT ["streamlit", "run"]
CMD ["app.py", "--server.port=8501", "--server.address=0.0.0.0"]
