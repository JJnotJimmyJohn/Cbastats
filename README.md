# cbastats

---

cbastats可用于获取CBA相关数据，包括每48分钟回合数，进攻评分和防守评分等。

Python package to access CBA stats, including advance stats like pace, offensive rating and defensive rating etc..

 ## 安装 Installation

 可以使用如下命令从[PyPI](https://pypi.org/project/cbastats/)下载
 
 You can install the package from [PyPI](https://pypi.org/project/cbastats/) using command below 
 
 
    pip install cbastats
    
这个包是用3.7开发的，不过只要你用的是python 3就应该不会有兼容性问题，可能python 2也可以。

 The package is developed using python 3.7 but there shouldn't be compatibility issue as long as you are using python 3
 (or even python 2).
 
 很快这个包也可在conda中下载安装。
 
 The package will be available in conda in the near future.
 
 ## 使用说明 How to Use
 
 设计的时候并没有把这个包设计成一个命令行工具，不过我还是尽量让数据的输出对命令行更友好。
 
 It's not meant to be used as a command line application due to the width of the data. However, efforts were made to 
 optimize the output under a command line environment by using [tabulate](https://pypi.org/project/tabulate/).
 
 目前为止（2020年3月15号）唯一一种实例化的方法是用pandas dataframe。尽管我其实写了一个直接从csv文件导入数据的方法，由于篮球统计数据的
 复杂性，还是建议大家直接使用我提供的AWS MySQL数据库。Guest账号在下面有提供。
 
 At this point (3/15/2020), the only entry point is pandas dataframe, meaning you can only 
 instantiate an object from a pandas dataframe. Although a convenient function to load directly from csv file is 
 provided, due to the intrinsic complexity of basketball stats, the preferred way to load CBA stats is through my hosted
  AWS MySQL database. A guest account is provided below. 
  
 不推荐用csv文件的原因是这个包的底层是pandas，如果要运算的话每一列的名字都必须与我的数据相同，所以就不推荐大家用了。
  
 The reason csv file is not recommended is, for the stats to calculate correctly, your column names will have to 
 exactly match the column names of my data and there are over 15 basic stats are used, 3 point made, 3 point 
 missed, minutes played, steals etc.. 
 
 #### 载入数据 Load Data
 
 所有数据都在 AWS MySQL 上，未来会写一个API来提供数据。
 
All the data are hosted on an AWS MySQL server. A REST API will be built to distribute 
 the data in the future. 
 
 载入下面这些包
 
 Import these packages
   
    from CBAStats.Player import *
    from CBAStats.Team import *
    import datetime
    from sqlalchemy import create_engine
  
  把数据放入一个pandas dataframe
 Run commands below to load the data into a pandas dataframe
  
    user_name = 'guest'
    passcode = 'Guest123456'
    endpoint = 'cbashuju.ctkaehd5rxxe.us-east-1.rds.amazonaws.com'
    database = 'CBA_Data'
    engine = create_engine(f'mysql+pymysql://{user_name}:{passcode}@{endpoint}/{database}')    
    connection= engine.connect()
    df = pd.read_sql("select * from CBA_Data.PlayerStatsPerGame", connection)
    connection.close()

#### 所有球队数据 All Teams Stats
Run commands below to get advance team stats

    teams = Team('',df)
    teams_df = pd.concat([teams.mov, teams.tm_pace, teams.tm_ortg, teams.tm_drtg, teams.tm_nrtg], axis=1)
    teams_df.columns=['场均净胜分MOV', 'Pace', 'OffensiveRating', 'DefensiveRating', 'NetRating']
    teams_df = teams_df.sort_values(by='NetRating',ascending=False)
    teams_df

Output

|球队|场均净胜分MOV|	Pace	|OffensiveRating|	DefensiveRating|	NetRating|
|---|---|---|---|---|---|
|广东|	16.9|	97.3	|127.1|	109.2|	17.8|
|新疆|	9.2|	95.6|	122.8|	113.0|	9.7
|青岛|	6.5|	96.0|	121.4|	114.5|	6.9
|浙江|	5.4|	92.1|	123.6|	117.5|	6.0
|山东|	4.9|	91.9|	118.4|	112.9|	5.4
|辽宁|	4.5|	94.5|	118.7|	113.8|	4.9
|广厦|	4.5|	94.6|	113.9|	109.0|	4.8
|吉林|	4.3|	92.5|	119.3|	114.5|	4.7
|山西|	3.3|	91.3|	117.1|	113.4|	3.7

#### 所有球员数据 All Players Stats

    players = Player('',df)
    players_df = pd.concat([players.plr_ortg, players.plr_drtg, players.plr_nrtg,players.plr_usg], axis=1)
  
    players_df.columns=['OffensiveRating', 'DefensiveRating', 'NetRating','UsagePercent']
    players_df = players_df.sort_values(by=['NetRating','UsagePercent'],ascending=False)
    
    
    players_df = pd.merge(players_df,players.plr_total_stats,left_index=True,right_index=True)
    players_df.reset_index(inplace=True)
    players_df.sort_values(by=['球队','NetRating','UsagePercent'],ascending=False,inplace=True)
    players_df
    
#### 单个球队数据 Single Team Stats


    teams = Team('广东',df)
    
    teams_df = pd.concat([teams.mov, teams.tm_pace, teams.tm_ortg, teams.tm_drtg, teams.tm_nrtg], axis=1)
    teams_df.columns=['场均净胜分MOV', 'Pace', 'OffensiveRating', 'DefensiveRating', 'NetRating']
    teams_df = teams_df.sort_values(by='NetRating',ascending=False)
    teams_df


#### 单个球员高阶数据 Single Player Stats

    players = Player('易建联',df)
    
    players_df = pd.concat([players.plr_ortg, players.plr_drtg, players.plr_nrtg,players.plr_usg], axis=1)
    
    players_df.columns=['OffensiveRating', 'DefensiveRating', 'NetRating','UsagePercent']
    players_df = players_df.sort_values(by=['NetRating','UsagePercent'],ascending=False)
    
    players_df = pd.merge(players_df,players.plr_total_stats,left_index=True,right_index=True)
    players_df    


## Working Items:
1. Rebuild data loading into a REST API
2. Migrate data to a MongoDB
3. Obtain historical CBA data
4. Develop an anecdote discover system - e.g. Jian is the first player to get 40+ points, 10+ rebounds and 10+ assits
