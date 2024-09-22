import plotly.graph_objects as go
from plotly.subplots import make_subplots
import io
from datetime import datetime, timedelta

def analyze_weight_progress(weight_history, lang, messages):
    if not weight_history:
        return None, messages[lang]['no_weight_data']

    dates = [entry.date for entry in weight_history]
    weights = [entry.weight for entry in weight_history]

    # Create figure with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Add traces
    fig.add_trace(
        go.Scatter(x=dates, y=weights, name="Weight", line=dict(color="#FF9900", width=4)),
        secondary_y=False,
    )

    # Set x-axis title
    fig.update_xaxes(title_text=messages[lang]['date_label'])

    # Set y-axes titles
    fig.update_yaxes(title_text=messages[lang]['weight_label'], secondary_y=False)

    # Customize the layout
    fig.update_layout(
        title=messages[lang]['weight_chart_title'],
        font=dict(family="Arial", size=14),
        plot_bgcolor='rgba(0,0,0,0)',
        hovermode="x unified",
        height=600,
        width=1000,
    )

    # Remove gridlines
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False)

    # Add range slider
    fig.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1, label="1m", step="month", stepmode="backward"),
                    dict(count=6, label="6m", step="month", stepmode="backward"),
                    dict(count=1, label="YTD", step="year", stepmode="todate"),
                    dict(count=1, label="1y", step="year", stepmode="backward"),
                    dict(step="all")
                ])
            ),
            rangeslider=dict(visible=True),
            type="date"
        )
    )

    buf = io.BytesIO()
    fig.write_image(buf, format='png')
    buf.seek(0)

    initial_weight = weights[-1]
    current_weight = weights[0]
    weight_change = current_weight - initial_weight
    
    analysis_text = messages[lang]['analysis_text'].format(
        initial_weight=initial_weight,
        current_weight=current_weight,
        weight_change=abs(weight_change),
        direction=messages[lang]['gained'] if weight_change > 0 else messages[lang]['lost']
    )
    
    return buf, analysis_text