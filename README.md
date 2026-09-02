# 🐞 Intelligent Software Defect Tracking System with Resolution Assistance

## 📌 Project Overview

The **Intelligent Software Defect Tracking System with Resolution Assistance** is an interactive web-based dashboard developed to analyze and monitor software defects throughout their lifecycle.

The system helps users understand bug-related information such as bug status, priority, severity, modules, root causes, teams, resolution time, and historical trends.

In addition to data visualization, the project includes an **AI Resolution Assistant** that provides possible defect classifications, root causes, recommended solutions, testing recommendations, and priority actions based on defect information.

The system also includes a **General AI Assistant** that can answer both project-related questions and general questions about topics such as Artificial Intelligence, Machine Learning, Python, programming, science, technology, and more.

---

# 🎯 Objectives

The main objectives of this project are:

* To track and analyze software defects efficiently.
* To monitor bugs based on status, priority, and severity.
* To identify modules with a high number of bugs.
* To analyze common root causes of software defects.
* To evaluate team performance based on assigned bugs and resolution time.
* To monitor bugs reported and closed over time.
* To calculate average bug resolution time and closure rate.
* To provide an intelligent resolution assistance system for software defects.
* To provide testing recommendations for identified defects.
* To enable users to search and filter bug records.
* To allow users to download filtered bug reports.
* To provide AI-powered assistance for project-related and general questions.

---

# 🚀 Features

## 📊 Interactive Dashboard

The dashboard provides an overview of important software defect metrics, including:

* 🐞 Total Bugs
* 🔓 Open Bugs
* ✅ Closed Bugs
* 🚨 Critical Bugs
* ⏱ Average Resolution Time
* 📈 Closure Rate

---

## 🔎 Dashboard Filters

Users can filter the dashboard data based on:

* Bug Status
* Priority
* Severity
* Module
* Sprint
* Team

A reset option is also provided to clear the applied filters.

---

## 📊 Overview Analysis

The dashboard provides visualizations for:

* Bug Status Distribution
* Priority-wise Bug Distribution
* Severity-wise Bug Distribution
* Top Modules with the Most Bugs

---

## 🔍 Detailed Bug Analysis

The system analyzes software defects based on:

* Module-wise Bug Distribution
* Sprint-wise Bug Distribution
* Root Cause Analysis
* Resolution Distribution

This helps identify areas that require more attention during software development and testing.

---

## 👥 Team Performance Analysis

The dashboard provides insights into:

* Team-wise Bug Count
* Average Resolution Time
* Developers with the Highest Number of Assigned Bugs

This helps evaluate workload distribution and team performance.

---

## 📈 Bug Trends

The system provides trend analysis using:

* Bugs Reported Over Time
* Bugs Closed Over Time
* Resolution Time Distribution

These visualizations help users understand the behavior and progress of software defects over time.

---

## 📋 Bug Records Management

The system provides a detailed view of bug records.

Users can:

* Search bugs using Bug ID or Bug Title.
* View detailed bug information.
* Analyze filtered records.
* Download filtered bug reports in CSV format.

---

# 🤖 AI Resolution Assistant

The AI Resolution Assistant allows users to enter defect information, including:

* Bug Title
* Bug Description
* Affected Module
* Severity
* Priority
* Known Root Cause

Based on the provided information, the system identifies possible defect categories such as:

* Authentication Defects
* Database Defects
* User Interface Defects
* Performance Defects
* API Defects
* Security and Access Control Defects
* Input Validation Defects
* General Software Defects

The assistant provides:

### 🔍 Possible Root Cause

A possible explanation for the defect.

### 🛠 Recommended Resolution

Suggestions for investigating and resolving the issue.

### 🧪 Testing Recommendation

Recommended testing activities after applying the fix.

### 📌 Recommended Action

Priority-based actions based on the severity of the defect.

---

# 💬 AI Assistant

The project includes a General AI Assistant powered by **Google Gemini AI**.

The AI Assistant can answer:

### Project-Related Questions

Examples include:

* How many bugs are in the project?
* Which module has the highest number of bugs?
* How many open bugs are there?
* How many closed bugs are there?
* How many critical bugs are there?
* What is the average resolution time?
* Which team has the most bugs?
* What is the most common root cause?

### General Questions

The AI Assistant can also answer questions outside the project, including:

* Artificial Intelligence
* Machine Learning
* Python
* Programming
* Data Science
* Software Testing
* Science
* Technology
* General Knowledge

---

# 🛠 Technologies Used

The project was developed using the following technologies:

* **Python** – Core programming language
* **Streamlit** – Web application and dashboard development
* **Pandas** – Data processing and analysis
* **Plotly** – Interactive data visualization
* **Google Gemini AI** – AI-powered question answering
* **CSV** – Dataset storage and management

---

# 📂 Project Structure

```text
Intelligent-Software-Defect-Tracking-System-with-Resolution-Assistance/
│
├── app.py
│
├── Intelligent Software Defect Tracking System with Resolution Assistance.csv
│
├── README.md
│
├── requirements.txt
│
└── .streamlit/
    └── secrets.toml
```

---

# 📊 Dataset Information

The dataset contains software defect-related information such as:

* Bug ID
* Bug Title
* Module
* Feature
* Sprint
* Release Version
* Severity
* Priority
* Status
* Lifecycle Stage
* Assigned Developer
* Team
* Root Cause
* Resolution
* Resolution Time
* Date Reported
* Date Closed

The system processes the dataset and generates interactive visualizations and insights.

---

# ⚙️ Installation

## 1. Clone the Repository

```bash
git clone https://github.com/godugulamonika2004-netizen/Intelligent-Software-Defect-Tracking-System-with-Resolution-Assistance.git
```

## 2. Navigate to the Project Folder

```bash
cd Intelligent-Software-Defect-Tracking-System-with-Resolution-Assistance
```

## 3. Install Required Libraries

```bash
pip install -r requirements.txt
```

## 4. Configure the Gemini API Key

Create the following file:

```text
.streamlit/secrets.toml
```

Add your Gemini API key:

```toml
GEMINI_API_KEY = "YOUR_API_KEY_HERE"
```

---

# ▶️ Run the Application

Run the following command:

```bash
streamlit run app.py
```

The application will open in your web browser.

---

# 📦 Requirements

Example `requirements.txt`:

```text
streamlit
pandas
plotly
google-genai
```

---

# 💡 Key Benefits

* Provides centralized software defect analysis.
* Makes bug information easier to understand using visualizations.
* Helps identify critical defects and high-risk modules.
* Supports team performance analysis.
* Tracks bug trends and resolution time.
* Provides intelligent defect resolution assistance.
* Provides AI-powered answers for both project and general questions.
* Allows users to filter, search, and download bug records.

---

# 🔮 Future Enhancements

The project can be enhanced in the future by adding:

* User authentication and role-based access.
* Real-time database integration.
* Automated bug prediction using Machine Learning.
* Bug severity prediction.
* Similarity detection for duplicate bugs.
* Automated bug assignment to developers.
* Chat history for the AI Assistant.
* Email notifications for critical bugs.
* Integration with bug tracking tools.
* Deployment using cloud services.

---

# 🏁 Conclusion

The **Intelligent Software Defect Tracking System with Resolution Assistance** provides an efficient way to analyze and monitor software defects using an interactive dashboard.

The project combines **data analysis, visualization, rule-based defect assistance, and Artificial Intelligence** to provide meaningful insights into software defects. Users can monitor bug status, severity, priority, root causes, team performance, resolution time, and historical trends.

The **AI Resolution Assistant** provides recommendations for investigating and resolving defects, while the **AI Assistant** supports both project-related and general questions.

Overall, the project demonstrates how data analytics and Artificial Intelligence can be combined to improve software defect tracking, analysis, and resolution.

---

## 👩‍💻 Developed By

**Godugula Monika**

### Project Title

🐞 **Intelligent Software Defect Tracking System with Resolution Assistance**
