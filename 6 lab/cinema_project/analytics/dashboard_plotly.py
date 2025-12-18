import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.offline import plot
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .analytics_repositories import AnalyticsRepository

@login_required
def analytics_dashboard(request):

    genre_qs = AnalyticsRepository.get_revenue_by_genre()
    df_genre = pd.DataFrame(list(genre_qs.values('name', 'total_revenue', 'total_tickets')))
    
    if not df_genre.empty:
        fig_genre = px.bar(
            df_genre, 
            x='name', 
            y='total_revenue',
            color='total_tickets',
            title='Дохід по жанрах (колір - к-сть квитків)',
            labels={'name': 'Жанр', 'total_revenue': 'Дохід (грн)', 'total_tickets': 'Продано квитків'},
            template='plotly_white'
        )
        plot_div_genre = plot(fig_genre, output_type='div', include_plotlyjs=False)
    else:
        plot_div_genre = "<div>Немає даних для відображення</div>"

    month_qs = AnalyticsRepository.get_monthly_revenue_stats()
    data_month = []
    for item in month_qs:
        data_month.append({
            'month': item['month'].strftime('%Y-%m') if item['month'] else 'N/A',
            'revenue': float(item['total_revenue'] or 0),
            'tickets': item['tickets_sold']
        })
    df_month = pd.DataFrame(data_month)

    if not df_month.empty:
        fig_month = px.line(
            df_month, 
            x='month', 
            y='revenue',
            markers=True,
            title='Динаміка доходів по місяцях',
            labels={'month': 'Місяць', 'revenue': 'Дохід (грн)'},
            template='plotly_white'
        )
        plot_div_month = plot(fig_month, output_type='div', include_plotlyjs=False)
    else:
        plot_div_month = "<div>Немає даних для відображення</div>"

    hall_qs = AnalyticsRepository.get_hall_utilization()
    df_hall = pd.DataFrame(list(hall_qs.values('name', 'avg_occupancy_rate', 'capacity')))
    
    if not df_hall.empty:
        df_hall['avg_occupancy_rate'] = df_hall['avg_occupancy_rate'].astype(float)
        
        fig_hall = px.bar(
            df_hall,
            x='name',
            y='avg_occupancy_rate',
            title='Середня заповнюваність залів (%)',
            labels={'name': 'Зал', 'avg_occupancy_rate': 'Заповнюваність %'},
            color='avg_occupancy_rate',
            color_continuous_scale='Viridis',
            template='plotly_white'
        )
        fig_hall.update_layout(yaxis_range=[0, 100])
        plot_div_hall = plot(fig_hall, output_type='div', include_plotlyjs=False)
    else:
        plot_div_hall = "<div>Немає даних для відображення</div>"

    context = {
        'plot_div_genre': plot_div_genre,
        'plot_div_month': plot_div_month,
        'plot_div_hall': plot_div_hall,
        'page_title': 'Cinema Analytics (Plotly)'
    }
    
    return render(request, 'analytics/dashboard.html', context)