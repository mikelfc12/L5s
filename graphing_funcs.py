import plotly.express as px
import pandas as pd
from numpy import pi
import plotly.graph_objects as go
from datetime import datetime, timedelta


raw_data_df = pd.read_csv('raw_data.csv')


#### Data Prep  Functions ####

def prepare_data(raw_data: pd.DataFrame):
    winrate_tbl = pd.DataFrame([])

    for player in raw_data['Name'].unique():
        player_stats = raw_data[raw_data['Name'] == player]
        wins = sum([1 if x == 'W' else 0 for x in player_stats['Result']])
        games = len(player_stats['Result'])
        winrate = wins / games
        player_res_tbl = pd.DataFrame({'Name' : player, 'Win Rate': winrate}, index=[0])
        winrate_tbl = pd.concat([winrate_tbl, player_res_tbl])

    raw_data = raw_data.merge(winrate_tbl, on = 'Name')
    per_player_summary = raw_data.groupby('Name').agg(
        {'Team GF': 'mean',
        'Team GA': 'mean',
        'Goals': 'mean',
        'MOTM': 'sum',
        'GOTG': 'sum',
        'Rating': 'mean',
        'Win Rate': 'mean'
        }
    ).round(2)
    return(per_player_summary)

def get_max_mins(pre_grouped_player_data: pd.DataFrame):
    melted_data = pre_grouped_player_data.melt('Name', var_name = 'Stat', value_name = 'Value')

    max_min_tbl = melted_data.drop('Name', axis=1).groupby(['Stat'], as_index=False).agg(['max','min'])
    melted_data['Rank'] = melted_data.groupby(['Stat'], as_index=False)['Value'].rank('first', ascending=False)
    max_min_tbl.columns = ['Stat','Max','Min']
    #max_min_tbl = max_min_tbl.drop('del', axis = 1)

    melted_data = melted_data.merge(max_min_tbl,'left', on='Stat')

    melted_data['Prop'] = melted_data['Value'] / melted_data['Max']
    #Reverse Team GA prop, as it's a negative stat. May be counterintuitive on plot though
    melted_data.loc[melted_data['Stat'] == 'Team GA','Prop'] = 1 - melted_data.loc[melted_data['Stat'] == 'Team GA','Prop']
    melted_data.loc[melted_data['Stat'] == 'Team GA','Rank'] = melted_data['Rank'].max() - melted_data.loc[melted_data['Stat'] == 'Team GA','Rank']

    return(melted_data)

def filter_player_data(data: pd.DataFrame, list_of_players):
    filt = data[data['Name'].isin(list_of_players)].reset_index()
    return(filt)


def xlserial_to_date(excel_date):
    dt = datetime.fromordinal(datetime(1900, 1, 1).toordinal() + excel_date - 2)
    return dt

#### radar func ######

def plot_polar_chart(finaldata, list_of_players, method = 'prop', return_obj = False):
    tot_players = len(finaldata['Name'].unique())
    filt_data = filter_player_data(finaldata, list_of_players)
    max_rank = finaldata['Rank'].max()
    filt_data['Asc Rank'] = [max(max_rank - player_rank, 1) for player_rank in filt_data['Rank']]

    var_dict = {
        'raw': 'Value',
        'prop': 'Prop',
        'rank': 'Asc Rank'
    }
    var_of_interest = var_dict[method]

    fig = go.Figure()

    no_players = max(len(filt_data['Name'].unique()),1)
    no_cols = max(len(filt_data['Stat'].unique()),1)
    sectionwidth = 2*pi/no_cols
    buffer = 0 #0.05*sectionwidth
    colwidth = (sectionwidth - buffer)/no_players
    coloffset = colwidth + buffer/no_players

    stat_col = str(filt_data.columns.get_loc('Stat'))
    val_col = str(filt_data.columns.get_loc('Value'))
    rank_col = str(filt_data.columns.get_loc('Rank'))

    #Loop through players and add their traces
    i = 0
    for player in list_of_players:
        player_data = filt_data.loc[filt_data['Name'] == player]
        player_stats = player_data[var_of_interest]
        stat_names = player_data['Stat']
        fig.add_trace(
            go.Barpolar(
                r = player_stats, 
                theta = stat_names, 
                name = player, 
                base = 'overlay', 
                width = colwidth,
                offset = (i-no_players)*coloffset,
                customdata = player_data,
                hovertemplate =     
                    "<b>%{data.name}</b><br>"+
                    "%{customdata["+stat_col+"]}: %{customdata["+val_col+"]}<br>"+
                    "Overall rank: %{customdata["+rank_col+"]} of "+str(tot_players)+
                    "<extra></extra>" 
            )
        )
        i += 1
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                showticklabels=False, # Hides the numbers
                ticks='',             # Hides the tick lines
            )
        )
    )
    if return_obj:
        return fig
    else:
        fig.show()

# def plot_radar_chart2(finaldata, list_of_players, method = 'prop'):
#     filt_data = filter_player_data(finaldata, list_of_players)
#     max_rank = finaldata['Rank'].max()
#     filt_data['Asc Rank'] = [max(max_rank - player_rank, 1) for player_rank in filt_data['Rank']]

#     var_dict = {
#         'raw': 'Value',
#         'prop': 'Prop',
#         'rank': 'Asc Rank'
#     }
#     var_of_interest = var_dict[method]

#     fig = px.line_polar(
#         filt_data,
#         r = var_of_interest,
#         theta = 'Stat', 
#         color = 'Name',
#         line_close = True,
#         hover_name = 'Name',
#         hover_data = ['Name', 'Stat', 'Value', 'Rank']
#     )
#     fig.update_traces(fill='toself') 
#     fig.show()

def plot_radar_chart(finaldata, list_of_players, method = 'prop', return_obj = False):
    tot_players = len(finaldata['Name'].unique())
    filt_data = filter_player_data(finaldata, list_of_players)
    max_rank = finaldata['Rank'].max()
    filt_data['Asc Rank'] = [max(max_rank - player_rank, 1) for player_rank in filt_data['Rank']]

    var_dict = {
        'raw': 'Value',
        'prop': 'Prop',
        'rank': 'Asc Rank'
    }
    var_of_interest = var_dict[method]

    fig = go.Figure()

    stat_col = str(filt_data.columns.get_loc('Stat'))
    val_col = str(filt_data.columns.get_loc('Value'))
    rank_col = str(filt_data.columns.get_loc('Rank'))

    #Loop through players and add their traces
    for player in list_of_players:
        player_data = filt_data.loc[filt_data['Name'] == player]
        player_data = player_data._append(player_data.iloc[0]) # need this to close loop
        player_stats = player_data[var_of_interest]
        stat_names = player_data['Stat']

        fig.add_trace(
            go.Scatterpolar(
                r = player_stats, 
                theta = stat_names, 
                name = player, 
                customdata = player_data,
                hovertemplate =     
                    "<b>%{data.name}</b><br>"+
                    "%{customdata["+stat_col+"]}: %{customdata["+val_col+"]}<br>"+
                    "Overall rank: %{customdata["+rank_col+"]} of "+str(tot_players)+
                    "<extra></extra>" 
            )
        )
    fig.update_layout(
        polar=dict(
            gridshape="linear", #delete for circular chart
            radialaxis=dict(
                showticklabels=False, # Hides the numbers
                ticks='',             # Hides the tick lines
                visible=False,
                range = [0, max_rank+2] # give space to hover on max-rankers
            )
        )
    )
    fig.update_traces(#fill polys and hide joining line
        fill="toself", 
        hoveron="points"
    ) 
    if return_obj:
        return fig
    else:
        fig.show()



def _render_comp_chart(df, player_list, method = 'prop', radar = True):
    grouped_data = prepare_data(df).reset_index()
    grouped_datam = get_max_mins(grouped_data)
    
    if radar:
        chart = plot_radar_chart(grouped_datam, player_list, method, True)    
    else:
        chart = plot_polar_chart(grouped_datam, player_list, method, True)
    
    return chart



#plot_radar_chart(grouped_datam, player_list)


def form_chart(data, player, last_x_games = False, x = 0, return_obj = False):
    x = max(x,1)
    #player_data = data[data['Name'] == player].iloc[["Date",""]]

    graph_title =  f"Form of {player}"
    if last_x_games:
        graph_title += f", last {x} appearances"

    med_form = data['Rating'].median()
    min_form = data['Rating'].min()

    if last_x_games:
        player_data = data[data['Name'] == player].iloc[-x:]
    else:
        player_data = data[data['Name'] == player]
    date_col = player_data['Date'].apply(xlserial_to_date)
    form_col = player_data['Rating'].round(2)

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x = date_col, y = form_col, 
            marker = dict(
                color = form_col, 
                colorscale = ['red','yellow','green'],
                showscale = True,
                cmin = min_form,
                cmid = med_form,
                cmax = 7
            ),
            name = ''
        )
    )
    fig.add_trace(
        go.Line(
            x = [date_col.iloc[0] - timedelta(days=1), date_col.iloc[-1:] + timedelta(days=1)], 
            y = 2*[med_form], 
            line = dict(dash='dash', color = 'black'),
            mode = 'lines',
            hovertemplate = f'All-players median performance, {med_form.round(2)}',
            name = ''
        )
    )
    fig.update_layout(
        yaxis={"range": [0, 7]},
        title = graph_title
    )
    if return_obj:
        return fig
    else:
        fig.show()

# form_chart(raw_data_df, "Daniel Hirst")