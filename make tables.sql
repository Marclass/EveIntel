
create table if not exists alliances(
	ID integer primary key,
	ccpID integer not null unique,
	name varchar(35) not null
);

create table if not exists corporations(
	ID integer primary key,
	ccpID integer not null unique,
	name varchar(35) not null,
	alliance integer,
	foreign key(alliance) references alliances(id)
	
);

create table if not exists players (
	ID integer primary key,
	ccpID integer not null unique,
	name varchar(35) not null,
	corporation integer not null,
	foreign key(corporation) references corporations(id)
	
	
);

create table if not exists systems(
	id integer primary key,
	ccpID integer not null unique,
	name varchar(35) not null,
	lastPulled datetime
);

create table if not exists ships(
	id integer primary key,
	ccpID integer not null unique,
	name varchar(35) not null
);

create table if not exists Structures(
	id integer primary key,
	ccpID integer not null unique,
	name varchar(35),
	corporation integer,
	player integer,
	foreign key(corporation) references corporations(id),
	foreign key (player) references players(id)
);

create table if not exists items(
	id integer primary key,
	ccpID integer not null unique,
	name varchar(100)
);

create table if not exists kills (
	id integer primary key,
	zKillID integer not null unique,
	victim integer,
	ship integer,
	[structure] integer,
	timeOfDeath datetime not null,
	system integer not null,
	corporation integer not null,
	alliance integer,
	isk integer,
	
	foreign key (alliance) references alliances(ccpid),
	foreign key (corporation) references corporation(ccpID),
	foreign key (system) references systems(ccpID),
	foreign key(victim) references players(ccpID)
	--foreign key(ship) references ships(id),
	--foreign key(structure) references Structures(id)
	
);

create table if not exists attackers (
	id integer primary key,
	player integer,
	[structure] integer,
	kill integer not null,
	damage integer,
	corporation integer,
	alliance integer,
	ship integer,
	foreign key (alliance) references alliances(ccpid),
	foreign key(corporation) references corporations(ccpID),
	foreign key(player) references players(ccpID),
	foreign key(structure) references structures(ccpID),
	foreign key(kill) references kills(zKillID)
	
	
);

create table if not exists fitting(
	id integer primary key,
	kill integer not null,
	foreign key (kill) references kills(id)
);
create table if not exists killsRaw(
	id integer primary key,
	zKillID integer not null unique,
	killmail varchar(MAX) not null, --sqlite ignores len and lets you store as much as you want
	processed boolean not null default false,
	skipped boolean not null default false
	
);

create table if not exists reportCache(
	id integer primary key,
	reportType int not null,
	entityID int not null,
	cacheTime datetime not null,
	content varchar not null,
	valid boolean not null
);


create index if not exists attackersCorporation on attackers (corporation);
create index if not exists attackerszKill on attackers (kill);
create index if not exists attackersPlayer on attackers (player);
create index if not exists attackersAlliance on attackers (alliance);

create index if not exists attackersKillPlayer on attackers (player, kill);
create index if not exists attackersKillCorporation on attackers (corporation, kill);
create index if not exists attackersKillAlliance on attackers (alliance, kill);

create index if not exists killsCorporation on kills (corporation);
create unique index if not exists killszKill on kills (zKillID);
create index if not exists killsSystem on kills (system);
create index if not exists killsAlliance on kills (alliance);
create index if not exists killsVictim on kills (victim);

create index if not exists killsZkillVictim on kills (zKillID, victim);
create index if not exists killsZkillAlliance on kills (zkillid, alliance);
create index if not exists killsZkillCorporation on kills (zkillid, corporation);


create unique index if not exists playersCCPID on players (ccpid);
create unique index if not exists corporationsCCPID on corporations (ccpid);
create unique index if not exists alliancesCCPID on alliances (ccpid);

create index if not exists playersName on players (name);
create index if not exists corporationsName on corporations (name);
create index if not exists alliancesName on alliances (name);

create index if not exists killsrawZkill on killsraw (zkillid);
create index if not exists killsrawProcessed on killsraw (processed);
create index if not exists killsrawSkipped on killsraw (skipped);

create index if not exists killsSystemCorporation on kills(system, corporation);
create index if not exists killsSystemAlliance on kills(system, alliance);
create index if not exists attackersSystemCorporation on attackers (kill, corporation);
create index if not exists attackersSystemAlliance on attackers (kill, alliance);

create index if not exists reportCacheAll on reportCache (reportType, entityID, cacheTime, valid);
