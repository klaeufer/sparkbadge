import plotly.express as px
import plotly as pl
import pandas as pd
import imgkit


def plot(data_points: list, height: int = 38, width: int = 95, top_margin: int = 0,
         left_margin: int = 0, bottom_margin: int = 0, right_margin: int = 0,
         title: str = "", output_file: str = "", auto_open=False):
    # image width  = width - left_margin - right_margin
    # image height = height - top_margin - bottom_margin
    fig = px.area(pd.DataFrame(data_points), height=height, width=width, title=title,
                  range_y=[min(data_points), max(data_points)], )
    fig.update_traces(line=dict(width=2), line_color='#92acc8')
    fig.update_xaxes(visible=False, fixedrange=True)
    fig.update_yaxes(visible=False, fixedrange=True)
    fig.update_layout(annotations=[], overwrite=True)
    fig.update_layout(showlegend=False, plot_bgcolor="white",
                      margin=dict(t=top_margin, l=left_margin, b=bottom_margin, r=right_margin))
    pl.offline.plot(fig, filename=output_file + '.html', config=dict(displayModeBar=False), auto_open=auto_open)
    imgkit.from_file(output_file + '.html', output_file + '.png')