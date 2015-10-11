# EveIntel
Datamining tool for the game "Eve Online" using public pvp data.


<p>This tool pulls public killmail data from https://zkillboard.com/ to analyze PvP activity in wormhole space.</p> 
<p>It is intended to be used as the back end with the <a href="https://github.com/Marclass/limbo/tree/EveIntelBranch" >EveIntel branch of Limbo</a>, a slack client, as the front end, but it is not dependant on slack or any other particular front end</p>

<h3>Requirements</h3>
<p><a href="https://github.com/Marclass/EveCommon">EveCommon library</a> is used to pull killmails from https://zkillboard.com and connect to the Eve static database</p>
<p><a href="https://github.com/eve-val/evelink">EveLink</a> is used to connect to Eve's xml api for some data imports, but may be dropped as a requirement in the future</p>
<p><a href="https://developers.eveonline.com/resource/static-data-export">The Eve Static Data Export</a> (sqlite) is used to help populate the db</p>
<p><a href="https://pypi.python.org/pypi/tabulate"> tabulate</a> is used to format reports into nice ascii tables</p>
<p><a href="https://pypi.python.org/pypi/ascii_graph/0.2.1">ascii_graph</a> is used to graph certain reports for easy representation on slack</p>

<h3>Setup</h3>
<p>EveIntel runs off of a sqlite database that must be populated with data before use. As of 7/30/2015 the db size is 5.25GB for all kills in wspace, so I recommend only downloading what you actually need since Zkillboard is nice enough to offer the killmails for free. </p>

<p>To setup the database: 
<ol><li>create a new sqlite3 db and use the make tables script to setup the schema</li>
<li>modify pullWHKills() in dbpopulate.py/dbpopulateCron to select the systems you want</li>
<li>modify sqlinterface to point to your sqlite3 db</li>
<li>modify sdeinterface to point to your Eve static sqlite db</li>
<li>populate systems in the db</li>
<li>set a custom useragent in zkillinterface.py</li>
<li>run dbpopulate and wait</li></ol></p>

<h3>Usage</h3>
<p>Once setup, EveIntel is primarally used via the report interface.</p>
<p>Current reports:
<ol>
<li>Entity home report: find entity home</li>
<li>Solar system report: find entity that lives in system</li>
<li>FC/PvP report: find players best at following primaries. FCs tend to rank highly</li>
<li>Hr report: creates a graph showing when entity is most active</li>
<li>Siege report: lists who has sieged who in the last two days and killed structures</li>
</ol></p>
<p> Example usage:
All reports are called via a reportInterface() object.
<pre>
<code>
from eveIntel.reportinterface import reportInterface
data = reportInterface()
entity="Lazerhawks"
report = data.getHomeReport(entity)
print(report)

System      NumKills+Losses    DaysRepresented  Class         Confidence Rating  Most recent kill/loss
--------  -----------------  -----------------  ----------  -------------------  -----------------------
J151909                 792                225  C5 (buggy)           4.1123e+36  2015-9-14
J124046                 130                 16  C5 (buggy)       33280           2015-9-16
J105934                 173                 15  C6 (buggy)       22144           2015-9-13
Thera                   205                 13  Thera             1640           2015-8-24
J125544                  56                 15  C5 (buggy)         896           2015-8-25
J110018                  62                 10  C5 (buggy)         496           2015-9-1
J213226                  98                 10  C5 (buggy)         196           2015-8-13
J115405                  48                  6  C5 (buggy)         192           2015-9-3
J170540                  46                  7  C5 (buggy)         184           2015-9-5
J164430                  71                  9  C5 (buggy)         142           2015-8-22
J171013                  35                  7  C5 (buggy)         140           2015-9-4
J152820                 136                  5  C5 (buggy)         136           2015-8-30
J152111                  59                  6  C5 (buggy)         118           2015-8-28
J135540                  50                  9  C5 (buggy)         100           2015-8-22
J111518                  25                  7  C5 (buggy)         100           2015-9-5

print(data.getSolReport("J100820"))

corporation                                      Kills+losses    Days Represented    Confidence Rating  Most recent kill/loss
---------------------------------------------  --------------  ------------------  -------------------  -----------------------
Sleeper Social Club                                      1882                 497                  inf  2015-09-13
Future Corps                                             1866                 496                  inf  2015-09-13
Lazerhawks                                                 84                  22                21504  2015-07-25
R3d Fire                                                   16                   3                   32  2015-09-09
Vision Inc                                                 16                   4                   32  2015-08-24
Hole Control                                               16                   4                   32  2015-08-24
WormHole Occupation and Resource Exploitation               8                   4                   16  2015-08-21
Ixtab.                                                     52                   9                   13  2015-06-23
Ministry of War                                             6                   4                    6  2015-08-16
Radical Astronauts Plundering Eve                           6                   3                    6  2015-08-21

print(data.getLeadershipReport("hard knocks inc."))

Pilot              KillCount    PossibleKills    Whore %    NumFights        Confidence
---------------  -----------  ---------------  ---------  -----------  ----------------
Braxus Deninard          847             1173   0.72208           115       1.55933e+06
sHanQ Myteia             710              988   0.718623          105       1.10559e+06
Gewik O'Drakar           418              740   0.564865           64  603912
NoobMan                  406              726   0.559229           66  580710
DaJokr                   308              684   0.450292           52  505825
Josh Tsutola             469              636   0.737421           47  459632
Pantuf                   369              555   0.664865           48  345638
gr33nCO                  301              548   0.54927            62  330292
Jaiimez Skor             305              547   0.557587           47  329562
Franky Saken             246              546   0.450549           35  322324
J3rz11                   278              493   0.563895           42  267998
Blizzaro                 215              493   0.436105           39  262128
matt jaker               358              476   0.752101           53  258116
Turd Destroyer           207              483   0.428571           33  251274
EMU EVIL                 191              466   0.409871           31  233140

print(data.getSiegeReport())

System    Besieged                 Siege Date    Siegers                                             num Structures killed    num Attackers
--------  -----------------------  ------------  ------------------------------------------------  -----------------------  ---------------
J212319   Sacred Soldiers          2015-09-15    SUPREME MATHEMATICS                                                    39                8
J113701   Sleeper Slumber Party    2015-09-15    Hard Knocks Inc.                                                       23                4
J110016   G.F.Y                    2015-09-15    Bros Before Holes                                                      12                2
J125634   Dredge X INC             2015-09-16    Haywire.                                                               11                2
J164613   FREE BURRITO LTD.        2015-09-15    Blackwater Associates                                                   8                1
J231137   Night cats               2015-09-16    SUPREME MATHEMATICS                                                     8                1
J144153   NanoTapkiCorp            2015-09-16    Exit-Strategy                                                           7                1
J123249   Chaos Order              2015-09-15    EyEs.FR                                                                 7                3
J163641   Panga Management         2015-09-16    Polarized                                                               7                2
J212906   Orcus Initiative         2015-09-15    Funny Scramble Inc.                                                     6                1
J155616   The Alabaster Albatross  2015-09-15    Russian industrial corporation a name of G-gurda                        5                1
J132458   Low-Life Mining Company  2015-09-15    Nehalem Inc.                                                            5                7
J100237   D.I.E.S.E.L.             2015-09-16    The Short Bus Squad                                                     5                2
J133613   Revelaetions             2015-09-16    Major League Infidels                                                   4                3
J145848   JinRoh Raiding Command   2015-09-15    Polarized                                                               3                4

</pre>
Because the db is powered by sqlite it doesn't handle multiple users very well, but a switch to postgres is planned for later.
</p>
