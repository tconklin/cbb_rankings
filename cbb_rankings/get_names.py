import re
import urllib2
import numpy as np

url_open = urllib2.urlopen('http://www.sports-reference.com/cbb/seasons/2016-school-stats.html')
url_text = url_open.read()


team_url_beg = np.array([m.end(0) for m in re.finditer('<tr  class="">\n   <td align="right" >[0-9]{,3}</td>\n   <td align="left" ><a href=''',url_text)])
team_url_end = np.array([m.end(0) for m in re.finditer('<tr  class="">\n   <td align="right" >[0-9]{,3}</td>\n   <td align="left" ><a href=''\S*.html',url_text)])
team_names_end = [m.end(0) for m in re.finditer('<tr  class="">\n   <td align="right" >[0-9]{,3}</td>\n   <td align="left" ><a href=''\S*.html'+"'>.{1,50}</a>",url_text)]
n_teams = np.size(team_url_beg)
team_names = ["" for x in range(n_teams)]
team_url = ["" for x in range(n_teams)]
write_file = "%s\t%s\t%s\t%s\t%s\t%s\n" % ("Team","Opponent","Game Site","Game Result","Team Score","Opponent Score")

for j in range(n_teams):
    team_url[j] = 'http://www.sports-reference.com'+url_text[team_url_beg[j]+1:team_url_end[j]-5]+'-schedule.html'
    team_names[j] = url_text[team_url_end[j]+2:team_names_end[j]-4]
    team_results_open = urllib2.urlopen(team_url[j])
    team_results_text = team_results_open.read()
    game_home_beg = np.array([(m.end(0)) for m in re.finditer('<tr  class="">\n   <td align="right".*1?\n   <td align="left".*2?\n   <td align="left".*3?\n   <td align="left".*4?\n   <td align=.*5?\n   <td align="left" >@?N?</td>\n   <td align="left" >(a href=.*>)?.*(</a>)?</td>\n   <td align=.*8?\n   <td align="left" >W?L?.*9?\n   <td align="right" >[0-9]{1,3}</td>.*0?\n   <td align="right" >[0-9]{1,3}</td>.*1?\n   <td align=.*2?\n   <td align=.*3?\n   <td align=.*4?\n   <td align=.*5?\n</tr>',team_results_text)])
    game_home_end = np.array([(m.end(0)) for m in re.finditer('<tr  class="">\n   <td align="right".*1?\n   <td align="left".*2?\n   <td align="left".*3?\n   <td align="left".*4?\n   <td align=.*5?\n   <td align="left" >@?N?</td>',team_results_text)])
    opp_names_beg = np.array([(m.end(0)) for m in re.finditer('<tr  class="">\n   <td align="right".*1?\n   <td align="left".*2?\n   <td align="left".*3?\n   <td align="left".*4?\n   <td align=.*5?\n   <td align="left" >@?N?</td>\n   <td align="left" >(<a href="\S*">)?',team_results_text)])
    opp_names_end = np.array([(m.end(0)) for m in re.finditer('<tr  class="">\n   <td align="right".*1?\n   <td align="left".*2?\n   <td align="left".*3?\n   <td align="left".*4?\n   <td align=.*5?\n   <td align="left" >@?N?</td>\n   <td align="left" >(<a href=.*>)?.*(</a>)?</td>',team_results_text)])
    win_loss = np.array([(m.end(0)) for m in re.finditer('<tr  class="">\n   <td align="right".*1?\n   <td align="left".*2?\n   <td align="left".*3?\n   <td align="left".*4?\n   <td align=.*5?\n   <td align="left" >@?N?</td>\n   <td align="left" >(a href=.*>)?.*(</a>)?</td>\n   <td align=.*8?\n   <td align="left" >W?L?.*9?\n',team_results_text)])
    team_score_beg = np.array([(m.end(0)) for m in re.finditer('<tr  class="">\n   <td align="right".*1?\n   <td align="left".*2?\n   <td align="left".*3?\n   <td align="left".*4?\n   <td align=.*5?\n   <td align="left" >@?N?</td>\n   <td align="left" >(a href=.*>)?.*(</a>)?</td>\n   <td align=.*8?\n   <td align="left" >W?L?.*9?\n   <td align="right" >',team_results_text)])
    team_score_end = np.array([(m.end(0)) for m in re.finditer('<tr  class="">\n   <td align="right".*1?\n   <td align="left".*2?\n   <td align="left".*3?\n   <td align="left".*4?\n   <td align=.*5?\n   <td align="left" >@?N?</td>\n   <td align="left" >(a href=.*>)?.*(</a>)?</td>\n   <td align=.*8?\n   <td align="left" >W?L?.*9?\n   <td align="right" >[0-9]{1,3}</td>',team_results_text)])
    opp_score_beg = np.array([(m.end(0)) for m in re.finditer('<tr  class="">\n   <td align="right".*1?\n   <td align="left".*2?\n   <td align="left".*3?\n   <td align="left".*4?\n   <td align=.*5?\n   <td align="left" >@?N?</td>\n   <td align="left" >(a href=.*>)?.*(</a>)?</td>\n   <td align=.*8?\n   <td align="left" >W?L?.*9?\n   <td align="right" >[0-9]{1,3}</td>.*0?\n   <td align="right" >',team_results_text)])
    opp_score_end = np.array([(m.end(0)) for m in re.finditer('<tr  class="">\n   <td align="right".*1?\n   <td align="left".*2?\n   <td align="left".*3?\n   <td align="left".*4?\n   <td align=.*5?\n   <td align="left" >@?N?</td>\n   <td align="left" >(a href=.*>)?.*(</a>)?</td>\n   <td align=.*8?\n   <td align="left" >W?L?.*9?\n   <td align="right" >[0-9]{1,3}</td>.*0?\n   <td align="right" >[0-9]{1,3}</td>',team_results_text)])
    n_games = np.size(opp_score_end)
    home_away = ["" for x in range(n_games)]
    opponent = ["" for x in range(n_games)]
    team = ["" for x in range(n_games)]
    win_loss_v = ["" for x in range(n_games)]
    team_score = np.zeros((n_games,2))
    print team_names[j]
    for k in range(n_games):
        team[k] = team_names[j].replace("&amp;","&")
        home_away[k] = team_results_text[game_home_end[k]-6].replace('>','H')
        if team_results_text[opp_names_end[k]-9:opp_names_end[k]] == '</a></td>':
            opponent[k] = team_results_text[opp_names_beg[k]:opp_names_end[k]-9]
        else:
            opponent[k] = team_results_text[opp_names_beg[k]:opp_names_end[k]-5]
        opponent[k] = opponent[k].split('>', 1)[-1].split('<', 1)[0].replace("&amp;","&")
        win_loss_v[k] = team_results_text[win_loss[k]-7:win_loss[k]-6]
        #print k
        team_score[k,0] = team_results_text[team_score_beg[k]:team_score_end[k]-5]
        team_score[k,1] = team_results_text[opp_score_beg[k]:opp_score_end[k]-5]
        write_file += "%s\t%s\t%s\t%s\t%s\t%s\n" % (team[k],opponent[k],home_away[k],win_loss_v[k],team_score[k,0],team_score[k,1])

with open("game_results.txt","w") as file_name:
    file_name.write(write_file)

