# (Swiss) Tournament Planner

This application will simulate a Swiss Tournament Planner.

## Table of contents

- [Project Specification](#project-specification)
- [How to run](#how-to-run)
- [Requirements](#python-requirements)
- [Shoutouts & References](#shoutouts-references)

## Project Specification
Develop a database schema to store details of a games matches between players.
Then write a Python module to rank the players and pair them up in matches in a tournament.
Further information: [Udacity Full Stack developer project 2](https://www.udacity.com/course/viewer#!/c-ud197-nd/ )

## How to run

### Install Virtualbox
https://www.virtualbox.org/wiki/Downloads


### Install Vagrant
https://www.vagrantup.com/downloads

Verify that Vagrant is installed and working by typing in the terminal:

	vagrant -v   # will print out the Vagrant version number

### Clone the Repository
Once you are sure that VirtualBox and Vagrant are installed correctly execute the following:

	git clone https://github.com/alinr/Udacity_FSWDN_P2_Tournament_Results.git
	cd Udacity_FSWDN_P2_Tournament_Results

### Verify that these files exist in the newly cloned repository:

	--tournament             #folder containing tournament files
	----tournament.py        #file that contains the python functions which unit tests will run on
	----tournament_test.py   #unit tests for tournament.py
	----tournament.sql       #postgresql database
	--Vagrantfile            #template that launches the Vagrant environment
	--pg_config.sh           #shell script provisioner called by Vagrantfile that performs
                              some configurations

### Launch the Vagrant Box

	vagrant up   #to launch and provision the vagrant environment
	vagrant ssh  #to login to your vagrant environment

### Enter the Swiss Tournament

	cd /
	cd vagrant
	cd tournament

### Initialize the database

	psql
	vagrant=> \i tournament.sql
	vagrant=> \q

	or

	psql -f tournament.sql


### Run the unit tests

	python tournament_test.py

You should see these results:

	1. Old matches can be deleted.
	2. Player records can be deleted.
	3. After deleting, countPlayers() returns zero.
	4. After registering a player, countPlayers() returns 1.
	5. Players can be registered and deleted.
	6. Newly registered players appear in the standings with no matches.
	7. After a match, players have updated standings.
	8. After one match, players with one win are paired.
	Success!  All tests pass!
	Additional tests to pass:
	9. Pairings with odd number of players: one player get a bye     and will be excluded from getting another bye.
	10. After having a draw match, both players have one match and no wins
	11. After playing four matches (including one draw)     the player standings are in the correct order.
	Success!  All additional tests pass!

### Shutdown Vagrant machine

	vagrant halt


### Destroy the Vagrant machine

	vagrant destroy


## Python Requirements

- Python 2.7.9
- psycopg2 module for python installed
- POSTGRESQL 9.3.9 installed
- Bleach 1.4.1 - download: https://pypi.python.org/pypi/bleach


## Shoutouts & References
- [Swiss-Style Pairing System](http://www.wizards.com/dci/downloads/swiss_pairings.pdf)
- PostgreSQL: [Create Cast](http://www.postgresql.org/docs/8.1/static/sql-createcast.html)
- PostgreSQL: [Conditional Expressions](http://www.postgresql.org/docs/8.1/static/functions-conditional.html)
- Stackoverflow: [...display matches won, matches played and matches drawed...](http://stackoverflow.com/questions/31484776/cant-display-matches-won-matches-played-and-matches-drawed-by-each-player)
- GitHub: [Thanks to Frederik Knust for SQL View](https://github.com/fknx/udacity-tournament/blob/master/tournament.sql)
