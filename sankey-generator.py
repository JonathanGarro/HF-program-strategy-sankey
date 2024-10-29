"""
Script ingests a CSV with exported data from the GMS to generate a Sankey diagram with program to strategy. 
Run `pip install pandas plotly` to install requirements
Replace the `gms-export.csv` with file. Ensure CSV contains "Top Level Primary Program", "Primary Strategy", and "Awarded Amount".
"""

import pandas as pd
import plotly.graph_objects as go

data = pd.read_csv('gms-export.csv', encoding='latin1')

sankey_data = data.groupby(
    ["Top Level Primary Program", "Primary Strategy"]
)["Awarded Amount"].sum().reset_index()

sources_unique = sankey_data["Top Level Primary Program"].unique().tolist()
targets_unique = sankey_data["Primary Strategy"].unique().tolist()

all_nodes = sources_unique + targets_unique
node_indices = {node: i for i, node in enumerate(all_nodes)}

source_indices = [node_indices[src] for src in sankey_data["Top Level Primary Program"]]
target_indices = [node_indices[tgt] for tgt in sankey_data["Primary Strategy"]]
values = sankey_data["Awarded Amount"].tolist()

fig = go.Figure(go.Sankey(
    node=dict(
        pad=15,
        thickness=20,
        line=dict(color="black", width=0.5),
        label=all_nodes,
    ),
    link=dict(
        source=source_indices,
        target=target_indices,
        value=values
    )
))

fig.update_layout(
    title_text="Sankey Diagram of Awarded Amounts by Program and Strategy",
    font_size=10,
    height=2000
)
fig.show()
