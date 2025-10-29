# 🎬 Netflix Content Analysis Dashboard

An interactive and visually engaging **Netflix Content Analysis Dashboard** built using **Streamlit**, **Pandas**, and **Plotly**.  
This dashboard provides insights into Netflix’s content library — helping users explore data about movies, TV shows, genres, release years, and much more.

---

## 🌐 Live Demo

👉[[Click here to open the app](https://netflix-dashboard-byakshaypatil.streamlit.app/)]

---

## 📊 Features

- 🔍 **Interactive Filters** – Filter Netflix titles by Type (Movie/TV Show), Country, and Genre  
- 📈 **Content Trends Over Time** – Visualize Netflix’s growth by year  
- 🎭 **Top Genres Analysis** – Discover the most popular genres on Netflix  
- 🌎 **Country-Wise Distribution** – See where most Netflix titles come from  
- 🧾 **Data Preview** – Explore the underlying dataset in real time  
- ⚡ **Fast and Responsive** – Built for performance and simplicity  

---

## 🧠 Tech Stack

| Component | Technology Used |
|------------|----------------|
| **Frontend** | Streamlit |
| **Backend / Logic** | Python |
| **Data Processing** | Pandas, NumPy |
| **Visualization** | Plotly Express, Plotly Graph Objects |
| **Deployment** | Streamlit Cloud |
| **Dataset Source** | Netflix Titles Dataset (Kaggle / Public Domain) |

---

## 🚀 How to Run Locally

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/AkshayPatil9370/Netflix-Dashboard.git
cd Netflix-Dashboard
```

### 2️⃣ Create a Virtual Environment (Recommended)
```bash
python -m venv venv
venv\Scripts\activate      # On Windows
# or
source venv/bin/activate   # On Mac/Linux
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Run the App
```bash
streamlit run netflix_dashboard.py
```

Then open your browser and go to 👉 [http://localhost:8501](http://localhost:8501)

---

## 🧾 Dataset Information

The dashboard uses the **Netflix Titles Dataset**, containing detailed information such as:
- 🎬 **Title**  
- 📺 **Type** (Movie / TV Show)  
- 🌍 **Country**  
- 📅 **Release Year** & **Date Added**  
- ⭐ **Rating**  
- ⏱️ **Duration**  
- 🎭 **Listed In (Genres)**  
- 🎥 **Director / Cast**

---

## 👨‍💻 Author

**Akshay Patil**  
🎓 M.Tech in Modelling and Simulation – *Savitribai Phule Pune University*  
💼 Aspiring Data Scientist | Python & Data Visualization Enthusiast  
📫 [Connect on LinkedIn]([https://www.linkedin.com/in/yourprofile](https://www.linkedin.com/in/akshay-patil-667a44283 ))  

---

## ⭐ Support

If you found this project useful, please consider:

- 🌟 Starring this repository  
- 🔗 Sharing it with your friends and classmates  
- 💬 Giving feedback or contributing improvements  

---

### 🧩 Project Structure

```
Netflix-Dashboard/
│
├── netflix_dashboard.py      # Main Streamlit app file
├── netflix_titles.csv        # Dataset file
├── requirements.txt          # Dependencies
├── README.md                 # Project documentation
├── images/
│   └── dashboard_preview.png # Dashboard preview image (optional)
└── venv/                     # Virtual environment (optional)
```

---

## 🏁 License

This project is open-source and available under the **MIT License**.

---

✨ *“Data tells stories — this dashboard lets you visualize Netflix’s story.”* 🎥

