create database cbb_records;
use cbb_records;

create table records (team_code INT,
                      team_name varchar(40),
                      games INT,
                      wins INT,
                      loss INT,
                      wp float,
                      weighted_wp float,
                      sos float,
                      conf_wins INT,
                      conf_loss INT,
                      home_wins INT,
                      home_loss INT,
                      away_wins INT,
                      away_loss INT,
                      points_scored INT,
                      points_allowed INT,
                      fg INT,
                      fga INT,
                      fgp float,
                      threep INT,
                      threepa INT,
                      threepp float,
                      ft INT,
                      fta INT,
                      ftp float,
                      orb INT,
                      trb INT,
                      ast INT,
                      stl INT,
                      blk INT,
                      tov INT,
                      fouls INT,
                      d_fg INT,
                      d_fga INT,
                      d_fgp float,
                      d_threep INT,
                      d_threepa INT,
                      d_threepp float,
                      d_ft INT,
                      d_fta INT,
                      d_ftp float,
                      d_orb INT,
                      d_trb INT,
                      d_ast INT,
                      d_stl INT,
                      d_blk INT,
                      d_tov INT,
                      d_fouls INT,
                      pace float,
                      points_100 float,
                      ft_rate float,
                      threep_rate float,
                      tsp float,
                      rebp float,
                      astp float,
                      stlp float,
                      blkp float,
                      efgp float,
                      tovp float,
                      orbp float,
                      ftpfg float,
                      d_pace float,
                      d_points_100 float,
                      d_ft_rate float,
                      d_threep_rate float,
                      d_tsp float,
                      d_rebp float,
                      d_astp float,
                      d_stlp float,
                      d_blkp float,
                      d_efgp float,
                      d_tovp float,
                      d_orbp float,
                      d_ftpfg float
                      );

create table games (team_name varchar(40),
                    opponent varchar(40),
                    game_site char,
                    result char,
                    team_score int,
                    opponent_score int);

load data local infile '/home/tim/college_bball/all_stats.txt'
into table records
columns terminated by '\t'
lines terminated by '\n'
ignore 0 lines;

load data local infile '/home/tim/college_bball/game_results.txt'
into table games
columns terminated by '\t'
lines terminated by '\n'
ignore 1 lines;
