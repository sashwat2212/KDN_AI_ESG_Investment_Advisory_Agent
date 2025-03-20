import shap
import numpy as np
import matplotlib.pyplot as plt
import os
import joblib 
import pandas as pd
from sklearn.preprocessing import LabelEncoder


results_folder = "results"
os.makedirs(results_folder, exist_ok=True)


rf_model = joblib.load("/Users/kdn_aisashwat/Desktop/esg-investment-advisor /models/greenwashing_model.pkl")  


df = pd.read_csv("/Users/kdn_aisashwat/Desktop/esg-investment-advisor /data_preprocessing/final_processed_esg_data.csv")  
X = df.drop(columns=["Greenwashing_Risk"])  
print(X.dtypes)


feature_names = X.columns.tolist()



categorical_cols = X.select_dtypes(include=["object"]).columns


label_encoders = {}
for col in categorical_cols:
    le = LabelEncoder()
    X[col] = le.fit_transform(X[col]) 
    label_encoders[col] = le 


explainer = shap.TreeExplainer(rf_model)
shap_values = explainer.shap_values(X)


fig = plt.figure()
shap.summary_plot(shap_values, X, feature_names=feature_names, show=False)
plt.savefig(os.path.join(results_folder, "shap_summary_greenwashing.png"), dpi=300, bbox_inches="tight")
plt.close(fig)


idx = np.random.randint(len(X))  
fig = plt.figure()
shap.waterfall_plot(shap.Explanation(values=shap_values[idx], base_values=explainer.expected_value, data=X.iloc[idx]), show=False)
plt.savefig(os.path.join(results_folder, "shap_waterfall_greenwashing.png"), dpi=300, bbox_inches="tight")
plt.close(fig)


print(f"SHAP plots saved in '{results_folder}' for Greenwashing Analysis!")
