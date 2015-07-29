-- Table definitions for the tournament project.


-- Drop database if exists
DROP DATABASE IF EXISTS tournament;

-- Create database
CREATE DATABASE tournament;

-- Connect to the database tournament
\c tournament;

-- Drop tables if exists
DROP TABLE IF EXISTS players CASCADE;
DROP TABLE IF EXISTS tournaments CASCADE;
DROP TABLE IF EXISTS tournament_players CASCADE;
DROP TABLE IF EXISTS matches CASCADE;

-- Drop views if exists
DROP VIEW IF EXISTS player_matches;
DROP VIEW IF EXISTS player_stats;


-- TABLES --
-- Creates the players table
CREATE TABLE players (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL
);

-- Create table for tournaments
CREATE TABLE tournaments (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL
);

-- Create relational table for tournaments - players
CREATE TABLE tournament_players (
	tournament_id INT REFERENCES tournaments(id) NOT NULL,
	player_id INT REFERENCES players(id) NOT NULL,
	bye INT NOT NULL DEFAULT 0,
	PRIMARY KEY (tournament_id, player_id)
);

-- Create table for matches
CREATE TABLE matches (
	id SERIAL PRIMARY KEY,
	tournament_id INT REFERENCES tournaments(id) NOT NULL,
	player_a INT REFERENCES players(id) NOT NULL,
	player_b INT REFERENCES players(id), -- can be null in case of bye
	winner INT REFERENCES players(id)
);


-- VIEWS --
-- Create view player - matches
CREATE VIEW player_matches AS
SELECT players.id AS player_id, players.name AS player_name, tournament_players.tournament_id, matches.id AS match_id,
CAST (
	CASE
		WHEN players.id = matches.winner
			THEN 1
		ELSE 0
	END AS int) AS Won
FROM players INNER JOIN tournament_players ON players.id = tournament_players.player_id
LEFT JOIN matches ON matches.tournament_id = tournament_players.tournament_id AND (players.id = matches.player_a OR players.id = matches.player_b);


-- Create view player rankings, consider OMW
CREATE VIEW rankings AS
SELECT tournament_id, player_id, player_name, count(match_id) as games, sum(won) as wins,
(
	SELECT COALESCE(sum(won),0) as wins FROM player_matches AS pm
	WHERE pm.tournament_id = player_matches.tournament_id AND pm.player_id IN
	(
		SELECT player_a as opponent FROM matches
		WHERE matches.tournament_id = pm.tournament_id  AND matches.player_b = player_matches.player_id
		UNION
		SELECT player_b as opponent FROM matches
		WHERE matches.tournament_id = pm.tournament_id AND matches.player_a = player_matches.player_id
	)
) AS omw
FROM player_matches
GROUP BY tournament_id, player_id, player_name
ORDER BY wins desc, omw desc;


-- Show tables
\dt;

-- Show views
\dv;