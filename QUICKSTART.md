# 🚀 Quick Start Guide

Get your Cisco Network Topology Simulator running in **5 minutes**!

## ⚡ Instant Deployment (Streamlit Cloud)

### Option 1: One-Click Deploy

1. **Fork this repository** (click "Fork" button above)
2. **Go to [Streamlit Cloud](https://streamlit.io/cloud)**
3. **Sign in with GitHub**
4. **Click "New app"**
5. **Select:**
   - Repository: `your-username/cisco-network-topology-simulator`
   - Branch: `main`
   - Main file: `app.py`
6. **Click "Deploy"**
7. **Done!** Your app will be live in 2-3 minutes

**Your live URL:** `https://your-app-name.streamlit.app`

---

## 💻 Local Development

### Prerequisites
- Python 3.9 or higher
- pip (Python package manager)

### Installation (3 commands)

```bash
# 1. Clone repository
git clone https://github.com/Mangesh-Bhattacharya/cisco-network-topology-simulator.git
cd cisco-network-topology-simulator

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
streamlit run app.py
```

**Access at:** `http://localhost:8501`

---

## 🐳 Docker Deployment

### Quick Docker Run

```bash
# Pull and run (when published to Docker Hub)
docker run -p 8501:8501 mangeshbhattacharya/cisco-network-simulator

# Or build locally
docker build -t cisco-simulator .
docker run -p 8501:8501 cisco-simulator
```

**Access at:** `http://localhost:8501`

---

## 🎯 First Steps

### 1. Generate Your First Network

1. Click **"🔧 Topology Builder"** in sidebar
2. Select **"Enterprise"** network type
3. Set:
   - Routers: 5
   - Switches: 10
   - Hosts: 50
4. Click **"🚀 Generate Topology"**
5. View your network visualization!

### 2. Run Security Audit

1. Click **"🔒 Security Audit"**
2. Select audit types
3. Click **"🔍 Run Security Audit"**
4. Review vulnerabilities and compliance

### 3. Export to Packet Tracer

1. Click **"📥 Export"**
2. Select **"Cisco Packet Tracer (.pkt)"**
3. Click **"📥 Export"**
4. Download and open in Packet Tracer

---

## 🔧 Troubleshooting

### Common Issues

**Issue:** Import errors
```bash
# Solution: Reinstall dependencies
pip install --upgrade -r requirements.txt
```

**Issue:** Port 8501 already in use
```bash
# Solution: Use different port
streamlit run app.py --server.port=8502
```

**Issue:** Module not found
```bash
# Solution: Ensure you're in project directory
cd cisco-network-topology-simulator
python -m streamlit run app.py
```

---

## 📚 Next Steps

- ✅ Read [README.md](README.md) for full documentation
- ✅ Check [examples/](examples/) for code samples
- ✅ Review [docs/API.md](docs/API.md) for API reference
- ✅ See [PORTFOLIO.md](PORTFOLIO.md) for project showcase

---

## 🆘 Need Help?

- 📧 Email: mangesh.bhattacharya@ontariotechu.net
- 🐙 GitHub Issues: [Report a bug](https://github.com/Mangesh-Bhattacharya/cisco-network-topology-simulator/issues)
- 💬 Discussions: [Ask questions](https://github.com/Mangesh-Bhattacharya/cisco-network-topology-simulator/discussions)

---

## ⭐ Enjoying the project?

**Star this repository** to show your support!

**Share with your network** to help others learn!

---

*Last Updated: December 2024*
