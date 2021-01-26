import pandas as pd
import matplotlib.pyplot as plt

# see: https://towardsdatascience.com/simple-little-tables-with-matplotlib-9780ef5d0bc4

players = pd.DataFrame([
        ("McDavid", "Connor"), \
        ("MacKinnon", "Nathan"), \
        ("Matthews", "Auston") \
        ], columns=["name", "prename"])

col = ["id", "number"]
roster_home = pd.DataFrame([
        (0, 97),
        (2, 34)
        ], columns=col)
roster_away = pd.DataFrame([
        (1, 29),
        (0, 97)
        ], columns=col)

goals = pd.DataFrame([
        ("00:13", "home", 97, 34),
        ("19:58", "home", 34, 97),
        ("31:42", "away", 29, 97),
        ("42:13", "home", 97, 34),
        ("", "", 0, 0)
        ], columns=["time", "team", "goal", "assi"])

evt = goals.iloc[0]
nbr = evt.goal
pid = roster_home[roster_home.number==nbr].iloc[0].id
nms = players.iloc[pid]


cell_text = [
                ['# 4 a. player (#10 b. player)', '1-0', ''],
                ['#17 c. player (# 9 d. player)', '2-0', ''],
                ['', '2-1', '# 6 e. player (#26 f. player)'],
                ['#10 b. player (# 4 a. player)', '3-1', ''],
                ['', '', '']
            ]
columns = ('away team', '@', 'home team')
times = ('00:25', '19:58', '25:42', '42:25', '')

the_table = plt.table(cellText=cell_text,
                      rowLabels=goals.time,
                      #rowLabels=times,
                      colLabels=columns,
                      loc='center')
#the_table.auto_set_font_size(False)
#the_table.set_fontsize(12)
the_table.scale(1, 1.5)

ax = plt.gca()
ax.get_xaxis().set_visible(False)
ax.get_yaxis().set_visible(False)
plt.box(on=None)

fig = plt.gcf()
plt.savefig('output/iBoxscore.png', bbox_inches='tight', dpi=150)
