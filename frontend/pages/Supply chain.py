import streamlit as st
import pandas as pd
import networkx as nx
import plotly.graph_objects as go
from PIL import Image
import base64


# Streamlit UI
st.set_page_config(layout="wide")
st.title("ESG Supply Chain Risk Tracker")
st.write("Analyze the global ESG risk exposure in corporate supply chains.")

st.markdown(
    """
    <style>
        .esg-header {
            font-size: 32px;
            font-weight: bold;
            color: rgb(0, 51, 141);  /* KPMG Blue */
            text-align: center;
        }
        [data-testid="stSidebar"] {
            background: #aceaff;
            padding: 25px;
            border-right: 4px solid rgb(0, 192, 174);
            color: #FFFFFF !important;
        }
        [data-testid="stSidebarContent"] {
            background: #aceaff;
            color: #FFFFFF !important;
            font-size: 16px;
        }
        [data-testid="stSidebar"] h1, 
        [data-testid="stSidebar"] h2, 
        [data-testid="stSidebar"] h3 {
            color: black !important;
        }
        /* Scrollable multiselect dropdown */
        div[data-baseweb="select"] {
            max-height: 150px;  /* Set the height of the box */
            overflow-y: auto;   /* Enable vertical scrolling */
        }
        .fraud-alert {
            font-size: 24px;
            font-weight: bold;
            text-align: center;
            padding: 10px;
            border-radius: 10px;
        }
        .low-risk {
            background: linear-gradient(135deg, rgb(12, 35, 60) 30%, rgb(0, 184, 245) 100%);
            padding: 15px;
            border-radius: 10px;
            color: white;
            text-align: center;
            font-size: 20px;
            font-weight: bold;
            margin: 10px 0;
        }
        .high-risk {
            background: linear-gradient(135deg, rgb(171, 13, 130) 30%, rgb(253, 52, 156) 100%);
            padding: 15px;
            border-radius: 10px;
            color: white;
            text-align: center;
            font-size: 20px;
            font-weight: bold;
            margin: 10px 0;
        }
    </style>
    """,
    unsafe_allow_html=True
)


def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Encode the logo
logo_base64 = get_base64_image("logo.png")

# Insert logo at the top of the sidebar
st.sidebar.markdown(
    f"""
    <style>
        .sidebar-logo {{
            display: flex;
            justify-content: left;
            align-items: left;
            margin-top: -350px;  /* Move logo up */
            margin-bottom: 20px; /* Add some space below */
        }}
        .sidebar-logo img {{
            width: 120px;  /* Adjust logo size */
        }}
    </style>
    <div class="sidebar-logo">
        <img src="data:image/png;base64,{logo_base64}">
    </div>
    """,
    unsafe_allow_html=True
)


# Load dataset
df = pd.read_csv("//Users/kdn_aisashwat/Desktop/esg-investment-advisor /Datasets/supply_chain_esg.csv")

def get_color(risk_level):
    return {
        "Low": "rgb(0, 192, 174)",   # Teal
        "Medium": "rgb(0, 184, 245)", # Light Blue
        "High": "rgb(253, 52, 156)"   # Magenta
    }.get(risk_level, "gray") 

# Sidebar Filters
st.sidebar.header("🔍 Filters")
selected_companies = st.sidebar.multiselect("Select Companies:", df["Company"].unique(), default=df["Company"].unique())
selected_risk = st.sidebar.multiselect("Select Risk Levels:", ["Low", "Medium", "High"], default=["Low", "Medium", "High"])

# Filter Data
filtered_df = df[(df["Company"].isin(selected_companies)) & (df["Risk_Level"].isin(selected_risk))]

# Display Filtered Data Table
st.write("### 📊 Supplier ESG Risk Overview")
st.dataframe(filtered_df)

# ESG Risk Color Mapping (Aligned with Sidebar)
def get_color(risk_level):
    return {
        "Low": "rgb(0, 192, 174)",   # Teal
        "Medium": "rgb(0, 184, 245)", # Light Blue
        "High": "rgb(253, 52, 156)"   # Magenta
    }.get(risk_level, "gray")  # Default gray

# Create Network Graph
G = nx.Graph()
for _, row in filtered_df.iterrows():
    G.add_node(row['Company'], color="rgb(0, 51, 141)", size=20)  # KPMG Blue
    G.add_node(row['Supplier'], color=get_color(row['Risk_Level']), size=15)
    G.add_edge(row['Company'], row['Supplier'])

# Convert to Plotly Network Graph
pos = nx.spring_layout(G, seed=42)
edge_x, edge_y, node_x, node_y, node_colors, node_text = [], [], [], [], [], []

# Draw edges (soft blue-gray edges for consistency)
for edge in G.edges():
    x0, y0 = pos[edge[0]]
    x1, y1 = pos[edge[1]]
    edge_x.extend([x0, x1, None])
    edge_y.extend([y0, y1, None])

# Draw nodes
for node in G.nodes():
    x, y = pos[node]
    node_x.append(x)
    node_y.append(y)
    node_colors.append(G.nodes[node]['color'])
    node_text.append(node)

# Plotly Graph with Sidebar Colors
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=edge_x, y=edge_y, mode='lines',
    line=dict(width=0.8, color="rgb(102, 163, 255)")  # Sidebar blue for edges
))
fig.add_trace(go.Scatter(
    x=node_x, y=node_y, mode='markers',
    marker=dict(size=12, color=node_colors, line=dict(width=2, color="black")),
    text=node_text, hoverinfo='text'
))

fig.update_layout(showlegend=False, margin=dict(l=0, r=0, t=0, b=0))
st.plotly_chart(fig, use_container_width=True)
