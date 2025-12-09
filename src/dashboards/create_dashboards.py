"""
Exemplo de dashboard com Plotly (alternativa a Metabase)
Gera gráficos interativos em HTML
"""

import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import json

def create_sample_dashboard():
    """Cria dashboard de exemplo com múltiplos gráficos"""
    
    # Dados simulados
    dates = [(datetime.now() - timedelta(days=x)).strftime('%Y-%m-%d') for x in range(30)]
    transactions = [1000 + (i * 50) for i in range(30)]
    revenue = [50000 + (i * 2000) for i in range(30)]
    
    # Gráfico 1: Transações por dia
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(
        x=dates, y=transactions,
        mode='lines+markers',
        name='Transações',
        line=dict(color='#1f77b4', width=2),
        fill='tozeroy'
    ))
    fig1.update_layout(
        title='Transações Diárias (últimos 30 dias)',
        xaxis_title='Data',
        yaxis_title='Número de Transações',
        template='plotly_white',
        height=400
    )
    fig1.write_html('dashboards/transactions_daily.html')
    print("✅ Criado: transactions_daily.html")
    
    # Gráfico 2: Receita acumulada
    cumsum_revenue = [sum(revenue[:i+1]) for i in range(len(revenue))]
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(
        x=dates, y=cumsum_revenue,
        fill='tozeroy',
        name='Receita Cumulada',
        line=dict(color='#2ca02c', width=2)
    ))
    fig2.update_layout(
        title='Receita Cumulada (últimos 30 dias)',
        xaxis_title='Data',
        yaxis_title='Receita ($)',
        template='plotly_white',
        height=400
    )
    fig2.write_html('dashboards/revenue_cumulative.html')
    print("✅ Criado: revenue_cumulative.html")
    
    # Gráfico 3: Distribuição por categoria (pie)
    categories = ['Electronics', 'Clothing', 'Food', 'Books', 'Other']
    values = [4500, 3200, 2100, 1800, 1400]
    
    fig3 = go.Figure(data=[go.Pie(
        labels=categories,
        values=values,
        textinfo='label+percent'
    )])
    fig3.update_layout(title='Distribuição de Vendas por Categoria')
    fig3.write_html('dashboards/category_distribution.html')
    print("✅ Criado: category_distribution.html")
    
    # Gráfico 4: Top 5 usuários
    top_users = [
        {'user': 'Alice', 'purchases': 45},
        {'user': 'Bob', 'purchases': 38},
        {'user': 'Charlie', 'purchases': 32},
        {'user': 'Diana', 'purchases': 28},
        {'user': 'Eve', 'purchases': 24},
    ]
    
    fig4 = go.Figure()
    fig4.add_trace(go.Bar(
        x=[u['user'] for u in top_users],
        y=[u['purchases'] for u in top_users],
        marker=dict(color='#ff7f0e')
    ))
    fig4.update_layout(
        title='Top 5 Usuários por Número de Compras',
        xaxis_title='Usuário',
        yaxis_title='Número de Compras',
        template='plotly_white'
    )
    fig4.write_html('dashboards/top_users.html')
    print("✅ Criado: top_users.html")
    
    # Gráfico 5: KPIs (gauge)
    fig5 = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=8.5,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Qualidade de Dados"},
        delta={'reference': 8.0},
        gauge={
            'axis': {'range': [0, 10]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 5], 'color': "lightgray"},
                {'range': [5, 8], 'color': "gray"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 9
            }
        }
    ))
    fig5.update_layout(height=400)
    fig5.write_html('dashboards/data_quality_gauge.html')
    print("✅ Criado: data_quality_gauge.html")
    
    print("\n📊 Dashboards criados em dashboards/")
    print("Abra em um navegador: file://.../dashboards/transactions_daily.html")

if __name__ == '__main__':
    import os
    os.makedirs('dashboards', exist_ok=True)
    create_sample_dashboard()
