# 📊 Global Superstore Sales Analysis  

Applied Power BI, Power Query, and DAX to clean, model, and visualize retail sales data, enabling data-driven decision making for market expansion and product strategy.  

Author: 👤 **Loc Ha**  
Date: 📅 June 2025  

![Power BI](https://img.shields.io/badge/Tool-Power%20BI-F2C811?logo=powerbi&logoColor=white)  ![Power Query](https://img.shields.io/badge/ETL-Power%20Query-217346?logo=microsoft-excel&logoColor=white)  ![DAX](https://img.shields.io/badge/Formula-DAX-006272?logo=databricks&logoColor=white)  

---

## 🚀 Executive Overview  

Superstore is a fictional retail company based in the United States, specializing in Furniture, Office Supplies, and Technology.
In this project, I took the role of a **Business Intelligence Analyst** to uncover key opportunities and challenges for business growth and profitability.  

### 🔎 Business Questions  
- Which **states and cities** are generating the highest revenue?  
- Which **product category** is both the best-selling and the most profitable?  
- Which **sub-categories and specific products** are top performers as well as underperformers?  
- Are there products that are frequently **bought together**?  
- Which **customer segment** is bringing in the most profit?  
- What is the most preferred **shipping mode** among customers?  
- How has the company’s performance **trended over recent months**?  
- What are the **KPIs** to track?  

---

## 📑 Table of Contents  
1. [📌 Background & Overview](#-background--overview)  
2. [📂 Dataset Description & Data Structure](#-dataset-description--data-structure)  
3. [🧠 Design Thinking Process](#-design-thinking-process)  
4. [⚒️ Main Process](#️-main-process)  
5. [📊 Key Insights & Visualizations](#-key-insights--visualizations)  
6. [🔎 Final Conclusion](#-final-conclusion)  

---

## 📌 Background & Overview  

### Objective  
The **Senior Manager** wants to evaluate the company’s global performance to:  
✔️ Identify key growth regions and products.  
✔️ Support decision-making for market expansion.  
✔️ Select strategic product categories to prioritize.  

### 👤 Who is this project for?  
✔️ Senior managers and executives.  
✔️ Business analysts & data analysts.  
✔️ Decision-makers in retail & operations.  

---

## 📂 Dataset Description & Data Structure  

### 📌 Data Source  
- **Source**: Superstore – a fictional U.S. retail company.  
- **Industry**: Furniture, Office Supplies, Technology.  
- **Timeframe**: 2011–2014.  
- **Format**: Excel (.xlsx).  
- **Size**: ~10K+ rows, 3 core tables.  

### 📊 Tables Used  
- **Fact_Orders** → sales, profit, quantity, customer, market.  
- **Dim_People** → sales reps per region.  
- **Fact_Returns** → return records.  
- **Dim_Product** → product category & subcategory.  
- **Dim_Date** → date hierarchy (day, month, quarter, year).  
- **_Measures** → DAX KPIs (Profit Margin, Return Rate %, etc.).  

### 🔗 Data Relationships  
<img width="1828" height="1539" alt="Screenshot 2025-09-06 113720" src="https://github.com/user-attachments/assets/18f5f7b0-6d96-4a15-9494-cdbc85e5713b" />


---

## 🧠 Design Thinking Process  

1️⃣ **Empathize** – Understand stakeholder (Senior Manager).  
- Needs insights into sales, profit, product performance, and returns.  
- Wants to expand into profitable markets.  

2️⃣ **Define** – Clarify the challenge.  
- Identify high-performing regions/products.  
- Detect underperforming categories.  

3️⃣ **Ideate** – Brainstorm metrics & visuals.  
- Market-level dashboard.  
- Product performance breakdown.  
- Insights & Recommendations summary page.  

4️⃣ **Prototype & Test** – Build dashboard, share feedback, iterate.  

📌 Design Thinking file (Google Sheets) was created to document stakeholder requirements and empathy maps.  

---

## ⚒️ Main Process  

1️⃣ **Data Cleaning & Preprocessing** (Power Query)  
✔️ Removed duplicates.  
✔️ Promoted headers.  
✔️ Standardized column names.  
✔️ Checked nulls and data types.  

2️⃣ **Exploratory Data Analysis (EDA)**  
✔️ Sales trend analysis.  
✔️ Return behavior by product & region.  

3️⃣ **DAX Measures**  
```DAX
Avg Order Value = DIVIDE([Total Sales],[Total Orders])

Order Count by Product-Market = DISTINCTCOUNT(Fact_Orders[Order ID])

Profit Margin (%) = 
DIVIDE(SUM(Fact_Orders[Profit]), SUM(Fact_Orders[Sales]))

Return Rate % = 
DIVIDE(
    CALCULATE(
        COUNTROWS(Fact_Returns),
        FILTER(
            Fact_Orders,
            Fact_Orders[Order ID] IN VALUES(Fact_Returns[Order ID])
        )
    ),
    DISTINCTCOUNT(Fact_Orders[Order ID])
)

Total Orders = DISTINCTCOUNT(Fact_Orders[Order ID])
Total Profit = SUM(Fact_Orders[Profit])
Total Quantity = SUM(Fact_Orders[Quantity])
Total Return Order = 
    CALCULATE(
        COUNTROWS(Fact_Returns),
        FILTER(
            Fact_Orders,
            Fact_Orders[Order ID] IN VALUES(Fact_Returns[Order ID])
        )
    )
Total Sales = SUM(Fact_Orders[Sales])

Total Sales YoY% = 
VAR __PREV_YEAR = CALCULATE([Total Sales], DATEADD('Dim_Date'[Date], -1, YEAR))
RETURN DIVIDE([Total Sales] - __PREV_YEAR, __PREV_YEAR)
```

4️⃣ **Power BI Visualization**  
✔️ Built interactive dashboards: Market, Product, Expansion, Recommendations.  
✔️ Added slicers for Year, Region, Category, Salesperson.  

---

## 📊 Key Insights & Visualizations  

### 🔍 Dashboard Previews  

#### 1️⃣ Market Expansion Dashboard  
<img width="2745" height="1559" alt="Screenshot 2025-09-06 113616" src="https://github.com/user-attachments/assets/df3ddda2-00af-466a-bd71-6544210a1d79" />


- **Observation**: Central region leads in sales, while Canada shows the highest profit margin (26.6%) but low revenue.  
- **Recommendation**: Expand in Central for scale; test marketing in Canada to exploit profit margins.  

---

#### 2️⃣ Market Analysis Dashboard  
<img width="2752" height="1550" alt="Screenshot 2025-09-06 113620" src="https://github.com/user-attachments/assets/88cc0721-0fa7-46d3-b3e2-77050b409f1c" />


- **Observation**: Southeast Asia shows strong YoY growth (+53%) despite low margins and high returns.  
- **Recommendation**: Test new product launches and optimize margins in Southeast Asia.  

---

#### 3️⃣ Product Dashboard  
<img width="2731" height="1555" alt="Screenshot 2025-09-06 113624" src="https://github.com/user-attachments/assets/c6b0d951-b81a-475c-aade-8a132a517d48" />

- **Observation**: Categories like “Tables” have negative profit margin (-8.46%) and high return rates.  
- **Recommendation**: Pause expansion for underperforming products until root causes are fixed.  

---

## ✅ Insights & Recommendations  

- Central region → focus on deep expansion.  
- Southeast Asia → experiment with new launches + margin improvements.  
- Canada → test campaigns to leverage high margins.  
- Products (Tables, Appliances, Accessories, Paper, Fasteners) → investigate losses before scaling.  

---

## 🔎 Final Conclusion 

📌 **Key Takeaways**:  
✔️ Double down on **Central** region – high revenue and growth.  
✔️ Explore **Canada** as a high-margin but underdeveloped market.  
✔️ Run pilot campaigns in **Southeast Asia** – fast-growing but low-margin.  
✔️ Suspend or fix **underperforming categories** (Tables, Appliances, Fasteners).  
✔️ Use data-driven monitoring (returns, margin %, YoY trends) to guide future expansion.  
