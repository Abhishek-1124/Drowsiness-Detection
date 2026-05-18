# Streamlit Deployment Guide for Drowsiness Detection

## Option 1: Streamlit Cloud (Easiest & Free)

### Steps:
1. **Go to** https://streamlit.io/cloud
2. **Sign up** with your GitHub account
3. **Click** "New app" 
4. **Select**:
   - Repository: `Abhishek-1124/Drowsiness-Detection`
   - Branch: `main`
   - Main file path: `app.py`
5. **Advanced settings** (if needed):
   - Python version: 3.10
   - Set any environment variables if needed
6. **Click "Deploy"** - Done!

**Result:** Your app will be live at: `https://<your-username>-drowsiness-detection.streamlit.app`

**Pros:**
-  Free tier available
-  Auto-deploys on GitHub push
-  Custom domain support ($5/month)
-  Built-in HTTPS

**Cons:**
-  Limited compute resources (free tier)
-  No GPU (free tier)

---

## Option 2: Docker + Cloud Run (Google Cloud)

### Prerequisites:
- Google Cloud account with billing enabled
- Docker installed locally

### Steps:

1. **Build Docker image locally:**
```bash
docker build -t drowsiness-detection: latest.
```

2. **Push to Google Container Registry:**
```bash
docker tag drowsiness-detection: latest gcr.io/YOUR-PROJECT-ID/drowsiness-detection
docker push gcr.io/YOUR-PROJECT-ID/drowsiness-detection
```

3. **Deploy to Cloud Run:**
```bash
gcloud run deploy drowsiness-detection \
  --image gcr.io/YOUR-PROJECT-ID/drowsiness-detection \
  --platform managed \
  --region us-central1 \
  --port 8501 \
  --memory 2Gi \
  --timeout 3600
```

**Result:** App deployed at: `https://drowsiness-detection-xxxxx.run.app`

**Pros:**
-  Generous free tier (2 million requests/month)
-  Auto-scales
-  Custom domains

**Cons:**
-  Requires Docker
-  Cold starts ~30 seconds

---

## Option 3: AWS (EC2 or Lightsail)

### Using EC2:

1. **Launch Ubuntu 22.04 instance** (t2.micro free tier)

2. **SSH into instance:**
```bash
ssh -i your-key.pem ubuntu@your-instance-ip
```

3. **Install dependencies:**
```bash
sudo apt update && sudo apt install -y python3.10 python3-pip git
```

4. **Clone repository:**
```bash
git clone https://github.com/Abhishek-1124/Drowsiness-Detection.git
cd Drowsiness-Detection
```

5. **Install requirements:**
```bash
pip install -r requirements.txt
```

6. **Run Streamlit with systemd service:**

Create `/etc/systemd/system/streamlit.service`:
```ini
[Unit]
Description=Streamlit Drowsiness Detection
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/Drowsiness-Detection
ExecStart=/usr/local/bin/streamlit run app.py --server.port 8501 --server. address 0.0.0.0
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable streamlit
sudo systemctl start streamlit
```

7. **Configure Security Group:**
   - Allow inbound traffic on port 8501 from anywhere (0.0.0.0/0)

8. **Access:** `http://your-instance-ip:8501`

---

## Option 4: Heroku (Deprecated - Use Render instead)

### Using Render.com (Better Alternative):

1. **Create account** at https://render.com
2. **Connect GitHub repository**
3. **Create Web Service:**
   - Choose Python 3.10
   - Build command: `pip install -r requirements.txt`
   - Start command: `streamlit run app.py --server.port 10000 --server.address 0.0.0.0`
4. **Deploy** - Done!

**Pros:**
-  Free tier available
-  Simple GitHub integration

---

## Option 5: DigitalOcean App Platform

1. **Create account** at https://digitalocean.com
2. **Create App** → Connect GitHub
3. **Select repository:** `Drowsiness-Detection`
4. **Choose Python component**
5. **Set commands:**
   - Build: `pip install -r requirements.txt`
   - Run: `streamlit run app.py --server. port 8080 --server.address 0.0.0.0`
6. **Deploy**

**Result:** `https://drowsiness-detection-xxxxx.ondigitalocean.app`

---

## Recommended Setup for Best Experience

### Local Development (Your Machine):
```bash
# Terminal 1: Run the app
cd ~/Drowsiness-Detection
streamlit run app.py

# Access at: http://localhost:8501
```

### Production Deployment:
**Use: Streamlit Cloud (easiest) or Docker + Cloud Run (more control)**

---

## Streamlit Configuration Tips

Edit `.streamlit/config.toml` for customization:

```toml
[theme]
primaryColor = "#FF6B6B"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"

[browser]
gatherUsageStats = false

[server]
headless = true
runOnSave = true
maxUploadSize = 200
```

---

## Environment Variables Setup

For cloud deployment, set these environment variables:

```bash
# Cloud Run / EC2 / Render
TF_CPP_MIN_LOG_LEVEL=2  # Suppress TensorFlow logs
```

---

## Troubleshooting

### App won't start on the cloud:
- Check if the port is 8501 or the assigned port
- Verify requirements.txt installs without errors
- Check the model file exists in the repo

### Model loading fails:
- Ensure `drowsiness_model.keras` is in repo root
- Verify TensorFlow/Keras versions match

### Memory issues:
- Upgrade to a larger instance (t2.small, t3.medium)
- Use model quantization or pruning

---

## Cost Estimate

| Option | Cost |
|--------|------|
| **Streamlit Cloud** | Free ($10/month for pro) |
| **Google Cloud Run** | ~$0-5/month |
| **AWS EC2 (t2.micro)** | Free (12 months), then ~$8-15/month |
| **Render** | Free tier available |
| **DigitalOcean** | $5/month minimum |

**Recommendation:** Start with **Streamlit Cloud** for free hosting with auto-deployment from GitHub!
