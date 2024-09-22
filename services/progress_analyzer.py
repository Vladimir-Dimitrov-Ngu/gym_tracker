from datetime import datetime
import io

import plotly.graph_objects as go


def analyze_weight_progress(weight_history, lang, messages):
    if not weight_history:
        return None, messages[lang]['no_weight_data']

    dates = [entry.date for entry in weight_history]
    weights = [entry.weight for entry in weight_history]

    # Создаем график
    fig = go.Figure()

    # Добавляем линию веса
    fig.add_trace(
        go.Scatter(x=dates, y=weights, name="Weight", line=dict(color="#FF9900", width=4), mode='lines+markers',
                   marker=dict(size=8, color='#0066CC', symbol='circle'))
    )

    # Настройка осей
    fig.update_xaxes(
        title_text=messages[lang]['date_label'],
        tickangle=45,
        tickformat='%Y-%m-%d',
        dtick='M1'
    )
    fig.update_yaxes(title_text=messages[lang]['weight_label'])

    # Настраиваем оформление
    fig.update_layout(
        title=messages[lang]['weight_chart_title'],
        font=dict(family="Arial", size=14),
        plot_bgcolor='rgba(0,0,0,0)',  # прозрачный фон
        hovermode="x unified",
        height=600,
        width=1000,
        margin=dict(l=50, r=50, t=50, b=100)  # Увеличиваем нижний отступ
    )

    # Отключаем линии сетки
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False)

    # Убираем слайдер времени и настраиваем формат даты
    fig.update_layout(
        xaxis=dict(
            rangeslider=dict(visible=False),
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
