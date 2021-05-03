import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from PIL import Image
import matplotlib, random

#@st.cache
def load_data():
    df2 = pd.read_csv(r'C:\Users\PSREDDY\Desktop\IplMatches.csv')
    df1=  pd.read_csv(r'C:\Users\PSREDDY\Desktop\IplBalls.csv')

    #numeric_df = df.select_dtypes(['float', 'int'])
    #numeric_cols = numeric_df.columns

    #text_df = df.select_dtypes(['object'])
    #text_cols = text_df.columns

    #country_col=df['Country']
    #country_unique=country_col.unique()

    team_unique = list(df1.batting_team.unique())
    venue_unique=list(df2.venue.unique())


    #grt_col=df['Group Technology']
    #grt_unique=grt_col.unique()

    return df1,df2,team_unique,venue_unique


df1,df2,team_unique,venue_unique=load_data()
team_unique.append('Choose any Option')
venue_unique.append('Choose any Option')
hex_colors_dic = {}
rgb_colors_dic = {}
hex_colors_only = []
for name, hex in matplotlib.colors.cnames.items():
    hex_colors_only.append(hex)
    hex_colors_dic[name] = hex
    rgb_colors_dic[name] = matplotlib.colors.to_rgb(hex)
img = Image.open(r"C:\Users\PSREDDY\Desktop\ipl-3.jpg")
st.image(img, width=700)
st.title('IPL Analysis')

st.sidebar.title('Menu')
check_box_bat=st.sidebar.checkbox(label='Batsman')


if(check_box_bat):
    select_bat=st.sidebar.selectbox('Select any one',['Choose any option','Top Batsman','Highest Score','Match Finishers','Previous Matches Batting stats'])


    if(select_bat=='Top Batsman'):
        select_team1=st.selectbox('Select batting Team',team_unique,index=len(team_unique)-1)
        select_team2=st.selectbox('Select Bowling Team',team_unique,index=len(team_unique)-1)

        # Team-Team analysis (For Batsman)

        tb_ga1 = df1.loc[:, ['batting_team', 'bowling_team', 'batsman', 'batsman_runs']]


        def batsman(bat_team, bowl_team, tb_ga1):
            tb_ga2 = tb_ga1[(tb_ga1['batting_team'] == bat_team) & (tb_ga1['bowling_team'] == bowl_team)]
            tb_ga3 = tb_ga2.drop('bowling_team', axis=1)
            tb_ga4 = tb_ga3.groupby(['batting_team', 'batsman'], as_index=False).agg({"batsman_runs": "sum"})
            tb_ga5 = tb_ga4.sort_values('batsman_runs', ascending=False, na_position='last')
            tb_ga6 = tb_ga5[['batsman', 'batsman_runs']].head(3)

            fig3 = go.Figure()
            fig3.add_trace(
                go.Bar(x=tb_ga6['batsman'], y=tb_ga6['batsman_runs'], marker=dict(color=hex_colors_only[10:13])))
            fig3.update_xaxes(title_text="Batsman")
            fig3.update_yaxes(title_text="Total Runs Scored")
            fig3.update_layout(title_text='Top three batsman of {} against {}'.format(bat_team, bowl_team))
            st.plotly_chart(fig3)

        if(st.button('Proceed')):
            if((select_team1!='Choose any Option') & (select_team2!='Choose any Option')):
                batsman(select_team1,select_team2,tb_ga1)

    if (select_bat=='Highest Score'):
        bat_name=st.text_input("Enter batsman name:")
        select_bowl_team = st.selectbox('Select bowling Team', team_unique, index=len(team_unique)-1)

        # Highest score of a batsman

        hb_ga1 = df1.loc[:, ['id', 'batsman', 'batsman_runs', 'bowling_team']]


        def high_score(bat, bowl_team, hb_ga1):
            hb_ga2 = hb_ga1[(hb_ga1['batsman'] == bat) & (hb_ga1['bowling_team'] == bowl_team)]

            hb_ga3 = hb_ga2.groupby(['id'], as_index=False).agg({'batsman_runs': 'sum'})
            # print(hb_ga3)
            hb_ga4 = hb_ga3.sort_values('batsman_runs', axis=0, ascending=False, na_position='last')
            hb_demo = hb_ga4.head(1)
            high = hb_demo.values
            # print(hb_ga4)
            # print(hb_demo)
            # print(high)

            st.text('Highest score of {} against {} is {}'.format(bat, bowl_team, high[0][1]))

        if(st.button('Proceed')):
            if ((select_bowl_team!= 'Choose any Option') & (str(bat_name)!='')):
                high_score(str(bat_name),select_bowl_team,hb_ga1)

    if (select_bat =='Match Finishers' ):
        select1_team1 = st.selectbox('Select batting Team', team_unique, index=len(team_unique) - 1)
        select1_team2 = st.selectbox('Select Bowling Team', team_unique, index=len(team_unique) - 1)

        # Most Runs by a batsman in death overs (16-20 Overs)

        tdb_ga1 = df1.loc[:, ['over', 'batsman', 'batsman_runs', 'batting_team', 'bowling_team']]


        def top_death_bat(bat_team, bowl_team, tdb_ga1):
            tdb_ga2 = tdb_ga1[(tdb_ga1['batting_team'] == bat_team) & (tdb_ga1['bowling_team'] == bowl_team) & (
                        (tdb_ga1['over'] == 15) | (tdb_ga1['over'] == 16) | (tdb_ga1['over'] == 17) | (
                            tdb_ga1['over'] == 18) | (tdb_ga1['over'] == 19))]
            # print(td_ga3['over'].unique())
            tdb_ga3 = tdb_ga2.groupby('batsman', as_index=False).agg({'batsman_runs': 'sum'})
            tdb_ga4 = tdb_ga3.sort_values('batsman_runs', axis=0, ascending=False, na_position='last')
            tdb_ga5 = tdb_ga4.head(3)
            # print(td_ga6)

            fig_d = go.Figure()
            fig_d.add_trace(
                go.Bar(x=tdb_ga5['batsman'], y=tdb_ga5['batsman_runs'], marker=dict(color=hex_colors_only[27:30])))
            fig_d.update_xaxes(title_text="Batsman")
            fig_d.update_yaxes(title_text="No. of runs scored in 16-20 overs ")
            fig_d.update_layout(title_text='Top Finishers of {}'.format(bat_team))
            st.plotly_chart(fig_d)


        if (st.button('Proceed')):
            if ((select1_team1 != 'Choose any Option') & (select1_team2 != 'Choose any Option')):
                top_death_bat(select1_team1,select1_team2,tdb_ga1)

    if (select_bat=='Previous Matches Batting stats'):
        bat_name = st.text_input("Enter batsman name:")
        select_bowl_team = st.selectbox('Select bowling Team', team_unique, index=len(team_unique) - 1)

        # Previous matches batting stats of a particular batsman

        tpb_ga1 = df1.loc[:,['id', 'batsman', 'batsman_runs', 'bowling_team']]


        def prev_bat(bat, bowl_team, num_matches, tpb_ga1):
            tpb_ga2 = tpb_ga1[(tpb_ga1['batsman'] == bat) & (tpb_ga1['bowling_team'] == bowl_team)]
            tpb_ga3 = tpb_ga2.groupby('id', as_index=False).agg({'batsman_runs': 'sum'})

            tpb_ga4 = tpb_ga3.sort_values('id', axis=0, ascending=False, na_position='last')

            tpb_ga5 = tpb_ga4.head(num_matches)

            fig_p1 = go.Figure()
            fig_p1.add_trace(go.Bar(x=[i for i in range(1, num_matches + 1)], y=tpb_ga5['batsman_runs'],
                                    marker=dict(color=hex_colors_only[12:12 + num_matches])))
            fig_p1.update_xaxes(title_text="Matches")
            fig_p1.update_yaxes(title_text="No. of runs scored")
            fig_p1.update_layout(
                title_text='Scores of {} in previous {} matches against {}'.format(bat, num_matches, bowl_team))
            st.plotly_chart(fig_p1)


        if (st.button('Proceed')):
            if ((select_bowl_team != 'Choose any Option') & (str(bat_name) != '')):
                prev_bat(bat_name,select_bowl_team, 5, tpb_ga1)



check_box_bowl=st.sidebar.checkbox(label='Bowler')

if(check_box_bowl):
    select_bowl = st.sidebar.selectbox('Select any one',['Choose any option', 'Top Bowlers', 'Batsman dismissal', 'Death Bowlers','Previous Matches Bowling stats'])

    if(select_bowl=='Top Bowlers'):
        select_team1_bat = st.selectbox('Select batting Team', team_unique, index=len(team_unique) - 1)
        select_team2_bowl = st.selectbox('Select Bowling Team', team_unique, index=len(team_unique) - 1)

        # Team-Team analysis (For Bowlers)

        tbo_ga1 = df1.loc[:,['batting_team', 'bowling_team', 'bowler', 'is_wicket', 'dismissal_kind']]


        def bowler(bat_team, bowl_team, tbo_ga1):
            tbo_ga2 = tbo_ga1[(tbo_ga1['batting_team'] == bat_team) & (tbo_ga1['bowling_team'] == bowl_team)]
            tbo_ga21 = tbo_ga2[tbo_ga2['dismissal_kind'] != 'run out']
            tbo_ga3 = tbo_ga21.drop(['batting_team', 'dismissal_kind'], axis=1)
            tbo_ga4 = tbo_ga3.groupby(['bowling_team', 'bowler'], as_index=False).agg({"is_wicket": "sum"})
            tbo_ga5 = tbo_ga4.sort_values('is_wicket', ascending=False, na_position='last')
            tbo_ga6 = tbo_ga5[['bowler', 'is_wicket']].head(3)

            fig4 = go.Figure()
            fig4.add_trace(
                go.Bar(x=tbo_ga6['bowler'], y=tbo_ga6['is_wicket'], marker=dict(color=hex_colors_only[10:13])))
            fig4.update_xaxes(title_text="Bowler")
            fig4.update_yaxes(title_text="Total Wickets taken")
            fig4.update_layout(title_text='Top three bowlers of {} against {}'.format(bowl_team, bat_team))
            st.plotly_chart(fig4)


        if (st.button('Proceed')):
            if ((select_team1_bat != 'Choose any Option') & (select_team2_bowl != 'Choose any Option')):
                bowler(select_team1_bat,select_team2_bowl,tbo_ga1)

    if (select_bowl=='Batsman dismissal'):
        bat_nameb = st.text_input("Enter batsman name:")
        select_bowl1_team = st.selectbox('Select bowling Team', team_unique, index=len(team_unique) - 1)

        # Top 3 bowlers of a team who taken the wicket of batsman many times.

        wb_ga1 = df1[df1['dismissal_kind'] != 'run out']
        wb_ga2 = wb_ga1.loc[:, ['batsman', 'bowler', 'bowling_team', 'is_wicket']]


        def top3_bowl(bat_p, bt):
            wb_ga3 = wb_ga2[(wb_ga2['batsman'] == bat_p) & (wb_ga2['bowling_team'] == bt)]
            wb_ga4 = wb_ga3.loc[:, ['bowler', 'is_wicket']]
            wb_ga5 = wb_ga4.groupby('bowler', as_index=False).agg({"is_wicket": "sum"})
            wb_ga6 = wb_ga5.sort_values('is_wicket', axis=0, ascending=False, na_position='last')
            wb_ga7 = wb_ga6.head(3)

            figb = go.Figure()
            figb.add_trace(go.Bar(x=wb_ga7['bowler'], y=wb_ga7['is_wicket'], marker=dict(color=hex_colors_only[17:20])))
            figb.update_xaxes(title_text="Bowlers")
            figb.update_yaxes(title_text="No. of times the wicket has fallen ")
            figb.update_layout(title_text='{} became out mostly'.format(bat_p))
            st.plotly_chart(figb)

        if (st.button('Proceed')):
            if ((select_bowl1_team != 'Choose any Option') & (str(bat_nameb) != '')):
                top3_bowl(bat_nameb,select_bowl1_team)

    if (select_bowl =='Death Bowlers'):
        select_team1_bat1 = st.selectbox('Select batting Team', team_unique, index=len(team_unique) - 1)
        select_team2_bowl1 = st.selectbox('Select Bowling Team', team_unique, index=len(team_unique) - 1)

        # Top death Bowlers (16-20 Overs)

        td_ga1 = df1.loc[:, ['over', 'bowler', 'is_wicket', 'dismissal_kind', 'batting_team', 'bowling_team']]
        td_ga2 = td_ga1[td_ga1['dismissal_kind'] != 'run out']


        def top_death_bowl(bat_team, bowl_team, td_ga2):
            td_ga3 = td_ga2[(td_ga2['batting_team'] == bat_team) & (td_ga2['bowling_team'] == bowl_team) & (
                        (td_ga2['over'] == 15) | (td_ga2['over'] == 16) | (td_ga2['over'] == 17) | (
                            td_ga2['over'] == 18) | (td_ga2['over'] == 19))]
            # print(td_ga3['over'].unique())
            td_ga4 = td_ga3.groupby('bowler', as_index=False).agg({'is_wicket': 'sum'})
            td_ga5 = td_ga4.sort_values('is_wicket', axis=0, ascending=False, na_position='last')
            td_ga6 = td_ga5.head(3)
            # print(td_ga6)

            fig_d = go.Figure()
            fig_d.add_trace(
                go.Bar(x=td_ga6['bowler'], y=td_ga6['is_wicket'], marker=dict(color=hex_colors_only[22:25])))
            fig_d.update_xaxes(title_text="Bowlers")
            fig_d.update_yaxes(title_text="No. of Wickets Taken in 16-20 overs ")
            fig_d.update_layout(title_text='Top Death Bowlers of {}'.format(bowl_team))
            st.plotly_chart(fig_d)

        if (st.button('Proceed')):
            if ((select_team1_bat1 != 'Choose any Option') & (select_team2_bowl1 != 'Choose any Option')):
                top_death_bowl(select_team1_bat1,select_team2_bowl1, td_ga2)

    if (select_bowl=='Previous Matches Bowling stats'):
        bowl_nameb = st.text_input("Enter Bowler name:")
        select_bat1_team = st.selectbox('Select batting Team', team_unique, index=len(team_unique) - 1)

        # Previous matches bowling stats of a particular bowler

        tmb_ga1 = df1.loc[:, ['id', 'bowler', 'batsman_runs', 'dismissal_kind', 'is_wicket', 'batting_team']]
        tmb_ga2 = tmb_ga1[tmb_ga1['dismissal_kind'] != 'run out']


        def prev_bowl(bowl, bat_team, num_matches, tmb_ga2):
            tmb_ga3 = tmb_ga2[(tmb_ga2['bowler'] == bowl) & (tmb_ga2['batting_team'] == bat_team)]

            tmb_ga4 = tmb_ga3.groupby('id', as_index=False).agg({'batsman_runs': 'sum', 'is_wicket': 'sum'})

            tmb_ga5 = tmb_ga4.sort_values('id', axis=0, ascending=False, na_position='last')

            tmb_ga6 = tmb_ga5.head(num_matches)

            fig_p2 = go.Figure(
                data=[go.Bar(x=[i for i in range(1, num_matches + 1)], y=tmb_ga6['batsman_runs'], name="Runs"),
                      go.Bar(x=[i for i in range(1, num_matches + 1)], y=tmb_ga6['is_wicket'], name="Wickets")])
            fig_p2.update_xaxes(title_text="Matches")
            fig_p2.update_yaxes(title_text="Bowling Spell")
            fig_p2.update_layout(
                title_text='Bowling Spells of {} in previous {} matches against {}'.format(bowl, num_matches, bat_team))
            st.plotly_chart(fig_p2)

        if (st.button('Proceed')):
            if ((select_bat1_team != 'Choose any Option') & (str(bowl_nameb) != '')):
                prev_bowl(bowl_nameb,select_bat1_team,5,tmb_ga2)








check_box_ph=st.sidebar.checkbox(label='Player(head->head)')

if(check_box_ph):
    name_bat=st.text_input("Enter Batsman name:")
    name_bowl=st.text_input("Enter Bowler name:")

    # PLayer (head -> head)

    ph_ga1 = df1.loc[:, ['batsman', 'bowler', 'batsman_runs']]

    pbh_ga1 = df1.loc[:, ['batsman', 'bowler', 'is_wicket', 'dismissal_kind']]
    pbh_ga2 = pbh_ga1[pbh_ga1['dismissal_kind'] != 'run out']


    def player_head(bat_player, bowl_player, ph_ga1, pbh_ga2):
        ph_ga2 = ph_ga1[(ph_ga1['batsman'] == bat_player) & (ph_ga1['bowler'] == bowl_player)]
        bat_ls = list(ph_ga2['batsman_runs'])
        st.text('The Runs scored by {} against {} are {}'.format(bat_player, bowl_player, sum(bat_ls)))

        pbh_ga3 = pbh_ga2[(pbh_ga2['batsman'] == bat_player) & (pbh_ga2['bowler'] == bowl_player)]
        bowl_ls = list(pbh_ga3['is_wicket'])
        st.text('The No. of times {} became out in {} are {}'.format(bat_player, bowl_player, sum(bowl_ls)))


    if (st.button('Proceed')):
        if ((str(name_bat)!='') & (str(name_bowl)!='')):
            player_head(name_bat,name_bowl,ph_ga1,pbh_ga2)


check_box_th=st.sidebar.checkbox(label='Team(head->head)')

if(check_box_th):
    team_bat1=st.selectbox('Select batting Team', team_unique, index=len(team_unique) - 1)
    team_bowl1 = st.selectbox('Select bowling Team', team_unique, index=len(team_unique) - 1)
    venue_team= st.selectbox('Select Venue',venue_unique,index=len(venue_unique)-1)

    th_ga1 = df2.loc[:, ['venue', 'team1', 'team2', 'winner']]


    def team_head(t1, t2, v):
        th_ga2 = th_ga1[(th_ga1['venue'] == v) & (((th_ga1['team1'] == t1) & (th_ga1['team2'] == t2)) | (
                    (th_ga1['team1'] == t2) & (th_ga1['team2'] == t1)))]
        th_ga3 = th_ga2['winner']
        win_ls = list(th_ga3.value_counts())
        # print(th_ga3.value_counts())
        th_pd = pd.DataFrame(th_ga3.value_counts())
        # print(th_pd)
        th_pd_final = list(th_pd.index)
        # print(type(th_ga3.value_counts()))
        # print(win_ls)
        # print(th_ga3.unique())

        figa = go.Figure()
        figa.add_trace(go.Bar(x=th_pd_final, y=win_ls, marker=dict(color=hex_colors_only[10:12])))
        figa.update_xaxes(title_text="Teams")
        figa.update_yaxes(title_text="No. of matches won ")
        figa.update_layout(title_text='No. of matches won by {} and {} in {}'.format(t1, t2, v))
        st.plotly_chart(figa)


    if (st.button('Proceed')):
        if ((team_bat1!= 'Choose any Option') & (team_bowl1!= 'Choose any Option') & (venue_team!='Choose any Option')):
            team_head(team_bat1,team_bowl1,venue_team)

check_box_toss=st.sidebar.checkbox(label='Toss Decision Percentage')

if(check_box_toss):
    team_l1 = st.selectbox('Select Team-1', team_unique, index=len(team_unique) - 1)
    team_l2 = st.selectbox('Select Team-2', team_unique, index=len(team_unique) - 1)
    team_toss= st.selectbox('Select Toss Winner', team_unique, index=len(team_unique) - 1)


    # Taking Toss Decision percentage

    def toss_decision(no1, no2, toss_win, df1):
        toss_decision_lst = []
        toss_dec1 = df1[
            ((df1['team1'] == no1) & (df1['team2'] == no2)) | ((df1['team1'] == no2) & (df1['team2'] == no1))]
        toss_dec11 = toss_dec1.loc[:, ['toss_winner', 'toss_decision']]
        toss_dec2 = toss_dec11[toss_dec11['toss_winner'] == toss_win]
        toss_dec3 = list(toss_dec2['toss_decision'].value_counts())

        # print(toss_dec3)
        # print(toss_dec2.toss_decision.unique())

        for i in toss_dec3:
            toss_decision_lst.append((i / sum(toss_dec3)) * 100)

        fig = go.Figure(data=[go.Pie(labels=list(toss_dec2.toss_decision.unique()), values=toss_decision_lst)])
        fig.update_layout(title_text='Decision Taking Percentage of ' + (toss_win))
        st.plotly_chart(fig)

    if (st.button('Proceed')):
        if ((team_l1!= 'Choose any Option') & (team_l2!= 'Choose any Option') & (team_toss!='Choose any Option')):
            toss_decision(team_l1,team_l2,team_toss,df2)
