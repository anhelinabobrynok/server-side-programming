from django.shortcuts import render
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import ColumnDataSource, HoverTool
import pandas as pd
from .models import Movie

def bokeh_dashboard(request):
    movies_qs = Movie.objects.all().values('release_year', 'rating', 'title')
    df = pd.DataFrame(list(movies_qs))

    script = None
    div = "<div>Дані відсутні</div>"

    if not df.empty:
        df['rating'] = pd.to_numeric(df['rating'], errors='coerce').fillna(0)
        df = df.dropna(subset=['release_year'])
        df['release_year'] = df['release_year'].astype(int)

        df_year = df.groupby('release_year')['rating'].mean().reset_index()
        df_year = df_year.sort_values('release_year')

        source = ColumnDataSource(df_year)

        p = figure(
            title="Середній рейтинг фільмів (за роком випуску)",
            x_axis_label='Рік випуску',
            y_axis_label='Середній рейтинг',
            width=800,   
            height=400, 
            background_fill_color="#fafafa"
        )

        p.line(x='release_year', y='rating', source=source, line_width=3, color="navy")
        
        p.scatter(x='release_year', y='rating', source=source, size=10, color="orange", legend_label="Рейтинг")

        p.add_tools(HoverTool(tooltips=[
            ("Рік", "@release_year"),
            ("Рейтинг", "@rating{0.2f}")
        ]))

        script, div = components(p)

    return render(request, 'dashboard/bokeh.html', {'script': script, 'div': div})