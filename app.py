import dash
from dash import html, dash_table
import pandas as pd
from salesforce_api import authenticate_salesforce, fetch_sessions

# Authenticate and fetch data
auth_data = authenticate_salesforce()
records = fetch_sessions(auth_data)

# Convert to DataFrame
df = pd.DataFrame(records)
df['CreatedDate'] = pd.to_datetime(df['CreatedDate'])
df['LastModifiedDate'] = pd.to_datetime(df['LastModifiedDate'])

# Flag suspicious users (multiple IPs)
ip_counts = df.groupby('UsersId')['SourceIp'].nunique()
suspicious = ip_counts[ip_counts > 1].index.tolist()
df['Suspicious'] = df['UsersId'].apply(lambda x: '⚠️' if x in suspicious else '')

# Build Dash App
app = dash.Dash(__name__)
app.title = "Salesforce Session Monitor"

app.layout = html.Div([
    html.H1("Active Salesforce Sessions", style={"textAlign": "center"}),

    dash_table.DataTable(
        data=df.to_dict('records'),
        columns=[{"name": i, "id": i} for i in df.columns],
        style_table={'overflowX': 'auto'},
        style_cell={'textAlign': 'left'},
        page_size=15,
        style_data_conditional=[
            {
                'if': {
                    'filter_query': '{Suspicious} = "⚠️"',
                    'column_id': 'Suspicious'
                },
                'backgroundColor': '#FFDDDD',
                'color': 'red',
                'fontWeight': 'bold'
            }
        ]
    ),
    html.Div("⚠️ = User with multiple active IPs", style={"marginTop": "20px", "color": "red"})
])

if __name__ == "__main__":
    app.run_server(debug=True)
