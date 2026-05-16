# Deployment Guide

## Options for Deploying Drowsiness Detection

### Option 1: Streamlit Cloud (Easiest)
1. Push your code to GitHub
2. Go to [Streamlit Cloud](https://share.streamlit.io/)
3. Click "New app"
4. Connect your GitHub repository
5. Select the branch and file (`app.py` or `app1.py`)
6. Deploy!

**Note:** Streamlit Cloud doesn't support webcam access directly. The app will work for local testing only.

### Option 2: Docker (Recommended for Production)

#### Build locally:
```bash
docker build -t drowsiness-detection .
docker run -p 8501:8501 drowsiness-detection
```

Access at `http://localhost:8501`

#### Deploy to Docker Hub:
```bash
docker login
docker tag drowsiness-detection:latest yourusername/drowsiness-detection:latest
docker push yourusername/drowsiness-detection:latest
```

### Option 3: GitHub Pages + GitHub Actions
This workflow includes CI/CD pipeline that:
- Runs tests on every push
- Validates Python syntax
- Checks all dependencies
- Builds Docker image

Check `.github/workflows/ci-cd.yml` for details.

### Option 4: Cloud Platforms

#### AWS EC2:
1. Launch EC2 instance with Ubuntu
2. SSH into the instance
3. Clone your repository
4. Install dependencies and run the app

#### Google Cloud Run:
```bash
gcloud run deploy drowsiness-detection \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

#### Heroku (Legacy - deprecated):
```bash
heroku create drowsiness-detection
git push heroku main
```

### Option 5: Local Deployment with systemd Service

Create `/etc/systemd/system/drowsiness-detection.service`:
```
[Unit]
Description=Drowsiness Detection App
After=network.target

[Service]
Type=simple
User=your-username
WorkingDirectory=/path/to/project
ExecStart=/path/to/venv/bin/streamlit run app.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable drowsiness-detection
sudo systemctl start drowsiness-detection
```

## Important Notes

1. **Webcam Access**: The app requires webcam access. Cloud deployments may not support this without modifications.
2. **Model Size**: Ensure your model file (`drowsiness_model.keras`) is included in the repository.
3. **Performance**: For production, consider using GPU-enabled instances for faster inference.
4. **Security**: Add authentication if deploying to a public URL.

## Monitoring

Set up monitoring with:
- GitHub Actions logs
- Application logs via `streamlit logs`
- Health checks (Docker/systemd)

## Troubleshooting

- **Model loading fails**: Ensure `drowsiness_model.keras` is in the correct directory
- **Webcam not working**: Check permissions and camera device availability
- **Memory issues**: Reduce model complexity or increase available memory
