import numpy as np
import matplotlib.pyplot as plt
import MySQLdb
from scipy import linalg

db = MySQLdb.connect(user=/user,passwd=/pw,db="cbb_records")
team_query = db.cursor()
game_query = db.cursor()
team_query.execute("""select distinct team_name from records;""")
team_names = team_query.fetchall()
team_query.execute("""select avg(wp) from records;""")
a_wp = team_query.fetchall()
a_wp = a_wp[0][0]
n_teams = np.size(team_names)
team_wp_all = np.zeros((1,n_teams))
team_sos_all = np.zeros((1,n_teams))
all_games = np.zeros((1,6))
for j in range(n_teams):
    print team_names[j]
    game_query.execute("""select t2.team_id, t3.team_id, t1.game_site, t1.team_score, t1.opponent_score, t2.wp, t3.wp, t2.games, t3.games from games as t1, records as t2, records as t3 where t1.team_name = t2.team_name and t1.opponent=t3.team_name and t1.team_name=%s;""", (team_names[j][0],))
    games_tuple = game_query.fetchall()
    games = np.array(games_tuple)
    opponents = games[:,1]
    n_opponents = np.size(opponents)
    game_site_str = games[:,2]
    game_site = (game_site_str == '@')*-1
    game_site += (game_site_str == 'H')*1
    team_score = np.array(games[:,3],dtype='float')
    opp_score = np.array(games[:,4],dtype='float')
    score_diff = team_score-opp_score
    team_wp = np.array(games[:,0],dtype='float')
    opp_wp = np.array(games[:,1],dtype='float')
    team_sos = np.mean(opp_wp)*np.ones(n_opponents)
    opp_sos = np.copy(team_sos)
    team_all_games = np.transpose([team_wp, opp_wp, game_site, n_opponents*np.ones(n_opponents), opp_sos, score_diff])
    all_games = np.append(all_games,team_all_games,0)
    team_wp_all[0,j] = team_wp[0]
    team_sos_all[0,j] = team_sos[0]

home_wp = 1-2*float(np.sum((all_games[:,2]<0)*(all_games[:,5]>0)))/np.sum(all_games[:,2]<0)
home_bonus = -float(np.sum((all_games[:,2]<0)*(all_games[:,5])))/np.sum(all_games[:,2]<0)
blow_out = np.ceil(2*np.std(all_games[:,5]))
diff = np.inf
total_games = np.shape(all_games)[0]
total_teams_chi = np.inf*(np.ones(n_teams))
total_teams_pra = np.zeros(n_teams)
n_iter = 100
chi_value = np.zeros(n_iter)
count = 0
######################################
#Ranking that uses point differential#
######################################
while count<n_iter and diff > 1e-2:
    total_teams_chi[:] = 0
    total_teams_pra_new = np.zeros(n_teams)
    game_number = np.zeros(n_teams)
    for j in range(1,total_games):
        team_a = all_games[j,0]
        team_b = all_games[j,1]
        if all_games[j,5] > 0:
            d_points_w = max(all_games[j,5]-np.sign(all_games[j,2])*home_bonus,1)
            d_points_w = min(d_points_w,blow_out) #some functional form of points scored in future games
            game_number[team_a-1] += 1
        elif all_games[j,5] < 0:
            d_points_w = min(all_games[j,5]-np.sign(all_games[j,2])*home_bonus,-1)
            d_points_w = max(d_points_w,-blow_out)
            game_number[team_a-1] += 1
        total_teams_chi[team_a-1] = (d_points_w-(total_teams_pra[team_a-1]-total_teams_pra[team_b-1]))**2*(.5+1./2.*game_number[team_a-1]/all_games[j,3])/np.trapz(.5+np.arange(0,all_games[j,3]+1,1)/all_games[j,3],np.arange(0,all_games[j,3]+1,1))
        total_teams_pra_new[team_a-1] += (d_points_w-(total_teams_pra[team_a-1]-total_teams_pra[team_b-1]))*(.5+1./2.*game_number[team_a-1]/all_games[j,3])/np.trapz(.5+np.arange(0,all_games[j,3]+1,1)/all_games[j,3],np.arange(0,all_games[j,3]+1,1))
    chi_value[count] = np.sum(total_teams_chi)
    count += 1
    diff = np.sum(total_teams_pra_new**2)
    print count, diff
    total_teams_pra = np.copy(total_teams_pra_new)+np.copy(total_teams_pra)


for j in range(n_teams):
    team_query.execute("""update records set pra=%s where team_id=%s """,(total_teams_pra[j],j+1))

####################################
#Ranking that uses pure wins/losses#
####################################
home_wp = 1-2*float(np.sum((all_games[:,2]<0)*(all_games[:,5]>0)))/np.sum(all_games[:,2]<0)
home_bonus = -float(np.sum((all_games[:,2]<0)*(all_games[:,5])))/np.sum(all_games[:,2]<0)
blow_out = np.ceil(2*np.std(all_games[:,5]))
diff = np.inf
total_games = np.shape(all_games)[0]
total_teams_chi = np.inf*(np.ones(n_teams))
total_teams_pra = np.zeros(n_teams)
n_iter = 100
chi_value = np.zeros(n_iter)
count = 0
while count<n_iter and diff > 1e-4:
    total_teams_chi[:] = 0
    total_teams_pra_new = np.zeros(n_teams)
    game_number = np.zeros(n_teams)
    for j in range(1,total_games):
        team_a = all_games[j,0]
        team_b = all_games[j,1]
        game_number[team_a-1] += 1
        d_points_w = np.sign(all_games[j,5])-np.sign(all_games[j,2])*home_wp
        total_teams_chi[team_a-1] = (d_points_w-(total_teams_pra[team_a-1]-total_teams_pra[team_b-1]))**2/all_games[j,3]
        total_teams_pra_new[team_a-1] += (d_points_w-(total_teams_pra[team_a-1]-total_teams_pra[team_b-1]))/all_games[j,3]
    chi_value[count] = np.sum(total_teams_chi)
    count += 1
    diff = np.sum(total_teams_pra_new**2)
    print count, diff
    total_teams_pra = np.copy(total_teams_pra_new)+np.copy(total_teams_pra)


for j in range(n_teams):
    team_query.execute("""update records set ts=%s where team_id=%s """,(total_teams_pra[j],j+1))
