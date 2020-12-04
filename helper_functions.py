#modular functions used for various reasons for app.py to declutter the code
import plotly.express as px
import plotly.graph_objects as go
from dash.exceptions import PreventUpdate
import os

#initialize mapbox access token
mapbox_access_token = os.environ.get('MAPBOX_API_KEY')
px.set_mapbox_access_token(mapbox_access_token)
branch_color_map = {'Navy':'#000080', 'Army':'#4b5320', 'Air Force':'#87d3f8','Marine Corps':'#dc143c'}

def scaler(series, bottom_range, top_range):
    '''
    Scales data between a range between (bottom_range, top_range)
    𝑥𝑛𝑜𝑟𝑚𝑎𝑙𝑖𝑧𝑒𝑑=(𝑏−𝑎) * 𝑥−𝑚𝑖𝑛(𝑥)     + a
                    𝑚𝑎𝑥(𝑥)−𝑚𝑖𝑛(𝑥)
    Input: pd.Series, np.array (list will not broadcast)
    Ouput: scaled version of Input between bottom_range and top_range
    '''
    #This value is known due to the current (Nov 2020) SOF distribution
    # ***** Need to not hard code this value *****
    max_series = 92
    min_series = 1
    multiplier = top_range - bottom_range
    numerator = series - min_series
    denominator = max_series - min_series
    ans = (multiplier * numerator/denominator) + bottom_range
    return ans + bottom_range



def update_scatter_map_layout(fig):
    '''
    Updates scatter map (fig) with "update_layout" method
    '''
    fig.update_layout(
        showlegend=False,
        hoverlabel=dict(
            font_size=12,
            font_family='Times New Roman'),
        autosize=False,
        mapbox=dict(
            accesstoken=mapbox_access_token,
            #style='dark',
            style='carto-positron',
            center=dict(lat=38.7, lon=-98.5795),
            zoom=3.75),
    margin={'l':0, 'r':0, 'b':0, 't':0}
    )


def plot_scatter_map(values, selector, df):
    px.set_mapbox_access_token(mapbox_access_token)

    def data_crunch(data, vals):
        temp = df[df[selector].isin(vals)]
        points = temp.groupby(['Branch', 'Tribe', 'latitude', 'longitude', 'CityState'])['Id'] \
            .count().to_frame().reset_index()
        points['text'] = points['CityState'] + ': ' + points['Id'].astype(str)
        points['Id'] = scaler(points['Id'], 1, 45)
        return points

    if isinstance(values, str):
        selected_values = [values]
        points = data_crunch(df, selected_values)

        new_map_update = plot_points(points)
        update_scatter_map_layout(new_map_update)

        return new_map_update

    else:
        points = data_crunch(df, values)

        new_map_update = plot_points(points)
        update_scatter_map_layout(new_map_update)

        return new_map_update

def plot_points(data):
    '''
    Plots all points from input dataframe
    '''
    fig = px.scatter_mapbox(data,
                       hover_name='text',
                       hover_data=dict(
                        Id=False,
                        latitude=False,
                        longitude=False
                       ),
                       opacity=0.7,
                       color=data.columns[0],
                       color_discrete_map=branch_color_map,
                       lat='latitude',
                       lon='longitude',
                       size='Id',
                       size_max=data['Id'].max(),
                       height=500
                       )
    return fig



def update_bar_chart_layout(chart, selector=None, chart_title=None, title_size=30, total_sum=None, yticks=False):
    '''
    Updates bar chart with "update layout" method
    '''
    if selector is None:
        yticks=True
    if selector == 'Branch':
        chart_title = 'Service Branch Breakout'
    elif selector == 'Tribe':
        chart_title = f'{chart_title}       Total = {total_sum}'
    update = chart.update_layout(
        font_family='Balto',
        hoverlabel=dict(
            font_size=14,
            font_family='Times New Roman'),
        title=dict(text=chart_title, x=0.5),
        font=dict(size=18, color="darkgrey"),
        xaxis=dict(color="lightsteelblue"),
        yaxis=dict(showgrid=False, showticklabels=yticks, color="darkgrey"),
        titlefont_size=title_size,
        showlegend=False,
        paper_bgcolor="#252e3f",
        plot_bgcolor="#4c5057",
        margin=dict(t=50, r=50, b=50, l=50),
    )
    return update

def plot_barchart(location, df, selector):
    temp_df = df[df['CityState'] == location]
    if selector == 'Branch':
        chart_df = temp_df['Branch'].value_counts().to_frame().reset_index()
        chart_df.rename(columns={'index':'Branch', 'Branch':'Count'}, inplace=True)
        chart_df = chart_df.sort_values('Count', ascending=False)
        total_sum = chart_df['Count'].sum()
    elif selector == 'Tribe':
        chart_df = temp_df.groupby(['Branch', 'Tribe'])['Id'].count().reset_index().sort_values('Id', ascending=False)
        chart_df.rename(columns={'Id': 'Count'}, inplace=True)
        chart_df = chart_df.sort_values('Count', ascending=False)
        total_sum = chart_df['Count'].sum()

    barchart = px.bar(chart_df,
                            x=selector,
                            y='Count',
                            orientation='v',
                            hover_name='Count',
                            color='Branch',
                            hover_data={'Count':False},
                            range_y=[0, 1.3*max(chart_df['Count'])],
                            color_discrete_map=branch_color_map,
                            text='Count',
                            )
    if selector == 'Branch':
        update_bar_chart_layout(barchart, selector=selector, chart_title='Service Branch Breakout', total_sum=None)
    elif selector == 'Tribe':
        update_bar_chart_layout(barchart, selector=selector, chart_title=location, total_sum=total_sum)
    barchart.update_traces(
        selector=dict(type='bar'),
        textposition='outside',
        marker_line=dict(
            width=2.5,
            color='black'),
        )
    return barchart

def plot_overall_marketing_barplot(df):
    channels = df['How_did_you_hear_about_Elite_Meet'].value_counts()
    channels = channels[channels > 2].sort_values().to_frame().reset_index()
    channels.rename(columns={'How_did_you_hear_about_Elite_Meet':'Count', 'index':'Channel'}, inplace=True)
    channels['Percents'] = round(channels['Count']/channels['Count'].sum() * 100, 2)
    channels['Percents'] = channels['Percents'].astype(str) + '%'

    barchart = px.bar(channels,
                      x='Count',
                      y='Channel',
                      orientation='h',
                      labels=dict(x='', y=''),
                      hover_name='Percents',
                      hover_data={'Count':True}
                      )

    update_bar_chart_layout(barchart, chart_title='Marketing Channels - Overall')

    return barchart

def plot_small_marketing_barplot(df, values):
    df = df.dropna()
    table = df.groupby(['Tribe', 'Branch', 'How_did_you_hear_about_Elite_Meet']).size()
    table = table[table > 2].to_frame(name='Count').reset_index()
    table.rename(columns={'How_did_you_hear_about_Elite_Meet':'Channels'}, inplace=True)
    bar_df = table[table['Tribe'] == values].sort_values(by='Count', ascending=False)
    bar_df['Percents'] = round(bar_df['Count']/bar_df['Count'].sum() * 100, 0)
    bar_df['Percents'] = bar_df['Percents'].astype(str) + '%'

    barchart = px.bar(bar_df,
                      x='Channels',
                      y='Count',
                      orientation='v',
                      color='Branch',
                      color_discrete_map=branch_color_map,
                      hover_name='Percents',
                      hover_data={'Branch':False, 'Count':False, 'Tribe':True, 'Channels':False},
                      text='Count'
                      )

    update_bar_chart_layout(barchart, chart_title=f'Marketing Channels:     {bar_df.iloc[0,1]} {bar_df.iloc[0,0]}', title_size=28)

    return barchart