# ESG Investment Advisor

## Project Overview
The **ESG Investment Advisor** is an AI-driven platform designed to assess and analyze Environmental, Social, and Governance (ESG) risks associated with companies. The system collects, processes, and evaluates ESG-related data from multiple sources, including financial reports, news sentiment, social media analysis, and satellite data. It leverages **reinforcement learning (RL)** for strategic decision-making and **explainable AI (XAI)** techniques for transparency. The primary objective is to help investors make informed and sustainable investment decisions while mitigating greenwashing risks.

## Features & Capabilities
### **Data Collection & Integration**
- **Financial Reports Analysis**: Scrapes and processes ESG-related data from company financial disclosures and sustainability reports.
- **News & Social Media Sentiment Analysis**: Uses NLP-based sentiment analysis on financial news, social media, and alternative data sources to detect ESG-related trends.
- **Satellite Data Processing**: Collects environmental and geospatial data to analyze company sustainability practices.
- **Supply Chain ESG Risk Analysis**: Evaluates the ESG risks associated with a company's supply chain network.

### **AI-Powered Risk Assessment & Predictions**
- **Greenwashing Detection**: Identifies misleading ESG claims by companies using NLP models.
- **Real-time ESG Ratings**: Generates ESG scores by benchmarking company data against industry standards.
- **Reinforcement Learning for Investment Strategy**: Trains AI agents to optimize investment decisions based on ESG factors and financial performance.
- **Predictive Analytics**: Forecasts the long-term impact (6 months to 1 year) of ESG factors on financial performance.

### **Visualization & Explainability**
- **Risk Heatmaps**: Visual representation of ESG risk levels across industries and companies.
- **Supply Chain Analysis Dashboards**: Identifies ESG vulnerabilities within a company’s supply chain.
- **SHAP-based Explainable AI**: Ensures transparency by explaining model predictions and mitigating bias.

## File Structure & Module Breakdown
```
ESG-INVESTMENT-ADVISOR/
│── backend/
│   │── app.py                 # Backend API for serving predictions
│   │── model_serving.py       # Serves ML models through API
│   │── test_requests.py       # Test scripts for API requests
│
│── data_collection/            # ESG Data Collection Scripts
│   │── financial_reports_scraper.py  # Scrapes ESG data from financial reports
│   │── news_sentiment_scraper.py     # Extracts news sentiment
│   │── social_media_analysis.py      # Analyzes social media sentiment
│   │── satellite_data_fetcher.py     # Fetches satellite data
│   │── combining_datasets.py         # Merges multiple ESG data sources
│
│── data_preprocessing/         # Data Cleaning & Feature Engineering
│   │── feature_engineering.ipynb  # Jupyter Notebook for data transformations
│   │── final_processed_esg_data.csv  # Cleaned ESG dataset
│
│── Datasets/
│   │── esg_data/
│       │── cleaned_esg_data.csv  # Preprocessed ESG data
│       │── data.csv              # Raw ESG data
│
│── frontend/
│   │── pages/
│       │── Risk Heatmap.py       # Generates ESG risk heatmaps
│       │── Supply chain.py       # Analyzes ESG-related supply chain risks
│       │── Statistics Section.py # Displays key ESG statistics
│       │── Home.py               # Main UI
│
│── models/                     # Machine Learning & AI Models
│   │── rl_agent.py              # Reinforcement Learning agent
│   │── rl_env.py                # RL environment for ESG decision-making
│   │── rl_train.py              # Trains the RL model
│   │── sentiment_analysis.ipynb # ESG sentiment analysis
│   │── greenwashing_model.pkl   # Model to detect greenwashing
│   │── trained_rl_model.pth     # Trained reinforcement learning model
│
│── results/                     # Model Outputs & Evaluation
│   │── agent_results/           # RL agent decision logs
│   │── sentiment_shap/          # SHAP explanations for sentiment analysis
│   │── greenwashing_shap/       # SHAP values for greenwashing detection
│   │── esg_risk_heatmaps/       # Visual heatmaps for ESG risk analysis
│   │── supply_chain_dashboard/  # ESG-related supply chain insights
│
│── visualizations/               # ESG Risk Heatmaps & Insights
│   │── esg_correlation_heatmap.png # ESG factor correlation analysis
│   │── esg_scores_by_industry.png  # Industry-wide ESG scores
│   │── top_bottom_esg_companies.png # ESG scores of best/worst companies
```

## Execution Results, Screenshot Logs, Output Files
<img width="1512" alt="Image" src="https://github.com/user-attachments/assets/70f9a78e-c7c9-41b8-9c5c-81d9d24bce08" />
<img width="1510" alt="Image" src="https://github.com/user-attachments/assets/1a305b60-d6ac-4e84-9d81-63564f1d238a" />
<img width="1511" alt="Image" src="https://github.com/user-attachments/assets/58baf0ee-b6d4-4a0a-b2f6-4331ca1b7ea4" />
<img width="1512" alt="Image" src="https://github.com/user-attachments/assets/ca5dd3d7-3ef7-4396-8e65-11d83bd9cd1f" />
<img width="1511" alt="Image" src="https://github.com/user-attachments/assets/46e190a8-abe4-4718-b3a7-f4e3cedaf753" />
<img width="1510" alt="Image" src="https://github.com/user-attachments/assets/2fce4a90-c0f0-402c-8d60-432fac239076" />
<img width="1512" alt="Image" src="https://github.com/user-attachments/assets/436195ba-4a88-45e3-aba7-02b21ced4e3b" />
<img width="1512" alt="Image" src="https://github.com/user-attachments/assets/7c8d1471-3c04-497a-acef-29740b8485a9" />
<img width="1512" alt="Image" src="https://github.com/user-attachments/assets/e55f189b-32cc-4f25-8437-b880031f76aa" />
<img width="1512" alt="Image" src="https://github.com/user-attachments/assets/cdde492f-a6d7-472e-b990-06afacacaef3" />
<img width="1512" alt="Image" src="https://github.com/user-attachments/assets/e8ea9021-7e6e-4d28-aa32-5974b539162c" />
<img width="1512" alt="Image" src="https://github.com/user-attachments/assets/39111f9f-3c7e-4e7a-a7ee-e01156ac0dad" />
<img width="1512" alt="Image" src="https://github.com/user-attachments/assets/71abb407-079a-4cc0-b766-13df4f3e8bf1" />
<img width="1512" alt="Image" src="https://github.com/user-attachments/assets/098f6077-8271-439f-bfc3-c390ecfb7003" />
<img width="1512" alt="Image" src="https://github.com/user-attachments/assets/b64fdd04-79e1-4ed6-ac3c-222d16f74699" />
<img width="1512" alt="Image" src="https://github.com/user-attachments/assets/ac449d38-6a7a-49a4-8390-33b39155cf8a" />
<img width="1511" alt="Image" src="https://github.com/user-attachments/assets/ad3eb622-9493-4023-b6da-5f1a89a8247a" />
### Sample Outputs:
#### **Sentiment Analysis**
- **Input**: News headlines & social media posts related to a company.
- **Processing**: NLP-based text classification for ESG sentiment.
- **Output**: ESG sentiment scores ranging from **-1 (negative)** to **+1 (positive)**.

#### **Greenwashing Detection**
- **Input**: Company sustainability reports & public ESG claims.
- **Processing**: NLP model trained on ESG disclosures.
- **Output**: Probability score indicating potential greenwashing (**e.g., 0.85 → high chance of greenwashing**).

#### **Reinforcement Learning-Based Investment Decisions**
- **Input**: ESG scores, financial performance, sentiment analysis.
- **Processing**: RL agent optimizes investment strategies.
- **Output**: AI-powered investment recommendations with confidence scores.

### **Screenshots & Logs**
(Screenshots of dashboards, model results, API responses, and heatmaps will be included here.)

## Edge Case Testing & Data Scenarios
1. **Companies with conflicting ESG claims**: Analyzed firms that report high ESG scores but have negative sentiment in news/social media.
2. **Greenwashing edge cases**: Tested companies with misleading ESG disclosures.
3. **Market crisis scenarios**: Evaluated the RL agent's response to economic downturns.
4. **Extreme sentiment shifts**: Tested model behavior for sudden sentiment changes.
5. **Supply chain disruption cases**: Tested how external ESG risks (e.g., regulatory changes, climate events) impact company ESG scores.

## Future Enhancements
- **Integration with IoT Data**: Enhance ESG assessment using sensor-based environmental data.
- **Advanced Time-Series Forecasting**: Improve ESG trend prediction using deep learning models (e.g., LSTMs, transformers).
- **Portfolio Optimization**: Develop AI-driven personalized ESG portfolio strategies for investors.
- **Real-time ESG Event Tracking**: Deploy event-driven architecture for real-time monitoring of ESG incidents.

## Conclusion
The ESG Investment Advisor integrates AI, NLP, RL, and XAI to enhance ESG risk analysis and investment strategies. By combining real-time data processing, reinforcement learning, and visualization tools such as risk heatmaps and supply chain analysis dashboards, this platform provides **a holistic, data-driven approach** to sustainable and responsible investing.

