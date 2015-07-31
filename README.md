# EveIntel
Datamining tool for the game "Eve Online" using public pvp data.


<p>This tool pulls public killmail data from https://zkillboard.com/ to analyze PvP activity in wormhole space.</p> 
<p>It is intended to be used as the back end with the <a href="https://github.com/Marclass/limbo/tree/EveIntelBranch" >EveIntel branch of Limbo</a>, a slack client, as the front end, but it is not dependant on slack or any other particular front end</p>

<h3>Requirements</h3>
<p><a href="https://github.com/Marclass/EveCommon">EveCommon library</a> is used to pull killmails from https://zkillboard.com and connect to the Eve static database</p>
<p><a href="https://github.com/eve-val/evelink">EveLink</a> is used to connect to Eve's xml api for some data imports, but may be dropped as a requirement in the future</p>
<p><a href="https://pypi.python.org/pypi/tabulate"> tabulate</a> is used to format reports into nice ascii tables</p>
<p><a href="https://developers.eveonline.com/resource/static-data-export">The Eve Static Data Export</a> (sqlite) is used to help populate the db</p>

<h3>Setup</h3>
<p>EveIntel runs off of a sqlite database that must be populated with data before use. As of 7/30/2015 the db size is 5.25GB for all kills in wspace, so I recommend only downloading what you actually need since Zkillboard is nice enough to offer the killmails for free. </p>

<p>To setup the database: 
<ol><li>create a new sqlite3 db and use the make tables script to setup the schema</li>
<li>modify pullWHKills() in dbpopulate.py/dbpopulateCron to select the systems you want</li>
<li>modify sqlinterface to point to your sqlite3 db</li>
<li>modify sdeinterface to point to your Eve static sqlite db</li>
<li>set a custom useragent in zkillinterface.py</li>
<li>run dbpopulate and wait</li></ol></p>

<h3>Usage</h3>
<p>Once setup, EveIntel is primarally used via the data processing interface. 
<pre>
<code>
from eveIntel.dataprocessinginterface import dataProcessingInterface
data = dataProcessingInterface()
entity="Lazerhawks"
report = data.genReport(entity)
print(report)

System      NumKills+Losses    DaysRepresented    Avg Kill Delta(days)    Confidence Rating  Most recent kill/loss
--------  -----------------  -----------------  ----------------------  -------------------  -----------------------
J151909                 760                215                   0.69           1.23317e+35  2015-7-30
J142528                 569                 16                   0.713     145664            2015-5-19
J222045                 349                 13                   0.588      22336            2015-3-29
J205141                 798                  8                   0.399      12768            2015-2-23
J124046                  95                 14                   0.783      12160            2015-6-3
J100820                  82                 15                   0.189      10496            2015-7-25
Thera                   201                 11                   0.11        6432            2015-7-20
J150020                 182                  9                   0.535       2912            2015-6-4
J125544                  40                 12                   0.408       2560            2015-6-4
J111249                  79                 10                   0.72        2528            2015-6-27
J213125                  70                 11                   0.89        2240            2015-6-19
J105934                  34                 12                   0.442       2176            2015-7-12
J133252                  63                 11                   0.718       2016            2015-5-23
J213226                  93                  9                   0.415       1488            2015-3-22
J110018                  57                  8                   0.729        912            2015-7-25


print(data.genReport("J100820"))

corporation                    Kills+losses    Days Represented    Confidence Rating  Most recent kill/loss
---------------------------  --------------  ------------------  -------------------  -----------------------
Sleeper Social Club________            1848                 481                  inf  2015-07-28
Future Corps_______________            1832                 480                  inf  2015-07-28
Lazerhawks_________________              84                  22               172032  2015-07-25
Ixtab._____________________              52                   9                  208  2015-06-23
Brave Collective___________               9                   5                   36  2015-07-20
Atztech Inc._______________              29                   5                   29  2015-06-23
The Desolate Order_________               7                   4                   28  2015-07-20
Isogen 5___________________               7                   4                   28  2015-07-24
Wormhole Holders___________               6                   4                   24  2015-07-28
Aliastra___________________               7                   2                    7  2015-07-03
</code>
</pre>
Because the db is powered by sqlite it doesn't handle multiple users very well, but a switch to postgres is planned for later.
</p>
