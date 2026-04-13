import plotly.express as px
import pandas as pd
from numpy import pi
import plotly.graph_objects as go

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


#### radar func ######

def plot_polar_chart(finaldata, list_of_players, method = 'prop'):
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

    no_players = len(filt_data['Name'].unique())
    no_cols = len(filt_data['Stat'].unique())
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
    fig.show()

def plot_radar_chart(finaldata, list_of_players, method = 'prop'):
    filt_data = filter_player_data(finaldata, list_of_players)
    max_rank = finaldata['Rank'].max()
    filt_data['Asc Rank'] = [max(max_rank - player_rank, 1) for player_rank in filt_data['Rank']]

    var_dict = {
        'raw': 'Value',
        'prop': 'Prop',
        'rank': 'Asc Rank'
    }
    var_of_interest = var_dict[method]

    fig = px.line_polar(
        filt_data,
        r = var_of_interest,
        theta = 'Stat', 
        color = 'Name',
        line_close = True,
        hover_name = 'Name',
        hover_data = ['Name', 'Stat', 'Value', 'Rank']
    )
    fig.update_traces(fill='toself') 
    fig.show()


#simplified plot testing
# fig = px.bar_polar(
#     filt_data2,
#     r = 'Value',
#     theta = 'Stat', 
#     barmode = 'group',
#     color = 'Name'
# )
# try px.line_polar ### seems to work
# fig = px.line_polar(
#     filter_player_data(grouped_datam, player_list),
#     r = 'Value',
#     theta = 'Stat', 
#     color = 'Name',
#     line_close = True
# )
# fig.update_traces(fill='toself') 
# fig.show()
# #bar works, why doesn't bar_polar??
# fig = px.bar(
#     filt_data2,
#     x = 'Stat',
#     y = 'Value', 
#     barmode = 'group',
#     color = 'Name'
# )
#fig.update_layout(polar=dict(barmode='overlay'))

#### Testing params; would need integrating into a tab ####

player1 = 'Daniel Hirst'
player2 = 'Jacob Stokes'
player3 = 'James King'

player_list = [player1, player2, player3]


#### Main process ####
grouped_data = prepare_data(raw_data_df).reset_index()
grouped_datam = get_max_mins(grouped_data)

print(grouped_datam) # debug


plot_polar_chart(grouped_datam, player_list, 'rank')
#plot_radar_chart(grouped_datam, player_list)
