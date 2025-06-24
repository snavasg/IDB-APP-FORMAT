# 📑 BID Template Generator

A ✨ **Streamlit** web-app that instantly transforms an Inter-American Development Bank (IDB) project workbook into the four official templates every team needs:

1. **C. Development Challenge**  
2. **D. Theory of Change**  
3. **E. Result Measurement**  
4. **F. Summary & Next Steps**

Upload ➜ Process ➜ Download — all in one click.

---

## 📋 Table of Contents
1. [Why?](#-why)  
2. [Features](#-features)  
3. [Requirements](#-requirements)  
4. [Local Run](#-local-run)  
5. [Repo Structure](#-repo-structure)  
6. [Deployment](#-deployment)  
   - 6.1 [Streamlit Cloud](#61-streamlit-cloud)  
   - 🌐 **Live App** → [Open the web app](https://your-app-url-here)  

9. [Contributing](#-contributing)  
10. [License](#-license)  
11. [Author](#-author)  

---

## ❓ Why?
IDB analysts spend valuable hours copying data between spreadsheets to craft the official templates.  
This project eliminates that manual work:

1. **Upload** the original project workbook (`.xlsx`) containing  
   *SDO & Result Indicators* and *Solutions & Outputs*.  
2. **Generate** the four fully-formatted templates in seconds.  
3. **Download** a single Excel file ready for review.

---

## ✨ Features

| ✅ | Description |
|----|-------------|
| 🌐 **Interactive web UI** | Drag-and-drop multiple `.xlsx` files, live progress bar, download buttons. |
| 🚀 **Batch processing** | Creates a packaged template for every workbook uploaded. |
| 🎨 **Corporate styling** | Merged cells, IDB colour palette, borders, data-validation lists & formulas via **openpyxl**. |
| 🔄 **Portable** | Works locally or on Streamlit Cloud, **Azure App Service**, and **Azure Container Apps**. |
| 🖥️ **Zero client installs** | Users only need a modern browser. |

---

## 🛠️ Requirements

| Tool | Min Version |
|------|-------------|
| Python | 3.9 |
| pip / venv | latest |
| OS | Windows / macOS / Linux |

> **Dependencies** – installed automatically from `requirements.txt` (`streamlit`, `pandas`, `openpyxl`, …).

---

## 🚀 Local Run

```bash
# 1 · Clone
git clone https://github.com/<USER>/<REPO>.git
cd <REPO>

# 2 · Virtual env
python -m venv venv
# Windows ➜ venv\Scripts\activate
source venv/bin/activate

# 3 · Install
pip install -r requirements.txt

# 4 · Launch
streamlit run app.py
```
---
## 🗂️ Repo Structure
``` bash

.
├─ app.py          # Streamlit UI
├─ pipeline.py     # Orchestrates read ➜ build ➜ export
├─ tables.py       # openpyxl builders (templates C–F)
├─ run.sh          # Start script for Azure App Service
├─ Dockerfile      # Container image for Azure Container Apps
├─ requirements.txt
└─ README.md
```
---
# 🌍 Deployment
6.1 Streamlit Cloud
Push the repository to GitHub.

Log in at https://streamlit.io/cloud.

Create app → choose repo, branch, app.py → Deploy.
Your web-URL is live in ~30 s (free tier, 1 GB RAM).

Live demo: Open the web app

## 🤝 Contributing
Fork → create branch feature/<name>

Run linters (black, flake8)

Open a Pull Request with a clear description of your change.

# 📜 License
MIT © 2025 — Santiago Navas Gómez

# 👤 Author
Santiago Navas Gómez — Economist & Data Scientist Consultant.
Works at the Inter-American Development Bank (Strategic Planning & Development Effectiveness Office).

“Automate today to measure better tomorrow.”