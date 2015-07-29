#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament


from random import shuffle
import psycopg2
import bleach

def connect(db="tournament"):
    """Connect to the PostgreSQL database tournament.  Returns a database
     connection and cursor object. If any connection error happens an
     exception will be thrown."""

    try:
        db_connect = psycopg2.connect("dbname={}".format(db))
        cursor = db_connect.cursor()
        return db_connect, cursor
    except psycopg2.Error:
        print "Error! Connection to database fails."


def deleteMatches():
    """Remove all the match records from the database."""
    db_connect, cursor = connect()
    query = ("DELETE FROM matches;")
    cursor.execute(query)
    db_connect.commit()
    db_connect.close()


def deletePlayers():
    """
    Remove all the player records from the database.
    First, remove all player records from the relational table
    """

    # Remove relational data
    deleteTournamentPlayers()

    # Remove all the player records from the database.
    db_connect, cursor = connect()
    query = ("DELETE FROM players;")
    cursor.execute(query)
    db_connect.commit()
    db_connect.close()


def deleteTournamentPlayers():
    """Remove all the tournament player records from the database."""
    db_connect, cursor = connect()
    query = ("DELETE FROM tournament_players;")
    cursor.execute(query)
    db_connect.commit()
    db_connect.close()


def deleteTournaments():
    """Remove all tournaments records from the database."""
    db_connect, cursor = connect()
    query = ("DELETE FROM tournaments;")
    cursor.execute(query)
    db_connect.commit()
    db_connect.close()


def countPlayers():
    """Returns the number of players currently registered."""
    db_connect, cursor = connect()
    query = ("SELECT count(id) AS num FROM players;")
    cursor.execute(query)
    count = cursor.fetchone()[0]
    db_connect.close()
    return count



def registerTournament(name, tournament_id=None):
    """Creates a new tournament.
    Args:
        name: name of the tournament
        tournament_id: (int) the tournament's id (optional)
    """

    bleached_name = bleach.clean(name, strip=True)

    db_connect, cursor = connect()

    if tournament_id is None:
        query = ("INSERT INTO tournaments VALUES (%s);")
        cursor.execute(query, (bleached_name,))
    else:
        query = ("INSERT INTO tournaments VALUES (%s, %s);")
        cursor.execute(query, (tournament_id, bleached_name,))

    db_connect.commit()
    db_connect.close()



def registerPlayer(name, tournament_id=1):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.
    Use bleach.clean() for HTML sanitization.

    Args:
        name: the player's full name (need not be unique).
    """

    # HTML sanitization
    bleached_name = bleach.clean(name, strip=True)

    db_connect, cursor = connect()
    query = ("INSERT INTO players (name) VALUES (%s);")
    cursor.execute(query, (bleached_name,))

    # Add player's value to relational table tournament_players
    if tournament_id is not None:
        # Get player's ID from the last insert
        query = ("SELECT currval(pg_get_serial_sequence('players', 'id'));")
        cursor.execute(query)
        player_id = int(cursor.fetchall()[0][0])

        query = ("INSERT INTO tournament_players VALUES (%s, %s, default);")
        cursor.execute(query, (tournament_id, player_id))

    db_connect.commit()
    db_connect.close()


def playerStandings(tournament_id=1):
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Args:
        tournament_id: (int) the tournament's id (optional)

    Returns:
        A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """

    db_connect, cursor = connect()
    query = ("SELECT player_id, player_name, wins, games \
             FROM rankings WHERE tournament_id = %s;")
    cursor.execute(query, (tournament_id,))
    result = cursor.fetchall()
    db_connect.close()

    players = list()

    for player in result:
        players.append((int(player[0]), player[1], int(player[2]), int(player[3])))

    return players


def reportMatch(player_a, player_b, winner, tournament_id=1):
    """Records the outcome of a single match between two players.
    Prevent rematches between players.

    Args:
        player_a: the id of the first player
        player_b: the id of the second player
        winner: the id of the winner (or None in case of a draw)
        tournament_id: the id of the matche's tournament
    """

    if isinstance(player_a, int) and \
            (isinstance(player_a, int) or player_b is None) and \
            (isinstance(winner, int) or winner is None):
        db_connect, cursor = connect()

        # Prevent rematches between players.
        query = ("SELECT tournament_id, player_a, player_b FROM matches \
                  WHERE tournament_id = %s AND player_a = %s AND player_b = %s \
                  OR player_a = %s AND player_b = %s")
        cursor.execute(query, (tournament_id, player_a, player_b, player_b, player_a,))
        result = cursor.fetchall()

        if len(result) > 0:
            return False
        else:
            query = ("INSERT INTO matches (tournament_id, player_a, player_b, winner) \
                      VALUES (%s, %s, %s, %s);")
            cursor.execute(query, (tournament_id, player_a, player_b, winner))
            db_connect.commit()
            db_connect.close()
    else:
        print "Error! Players ID should be type integer!"


def swissPairings(tournament_id=1):
    """Returns a list of pairs of players for the next round of a match.
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Args:
        tournament_id: the id of the tournament the players shall be found for

    Returns:
        A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """

    standings = playerStandings(tournament_id)

    if len(standings) % 2 != 0:
        # there is an odd number of players
        players = playersWithoutBye()
        shuffle(players)

        random_player = players.pop()
        setByeForPlayer(random_player[0])

        # directly report the match and remove the lucky player from the standings
        reportMatch(random_player[0], None, random_player[0])
        standings = [player for player in standings if player[0] != random_player[0]]

    l = list()

    while len(standings) >= 2:
        player_a = standings.pop(0)
        player_b = standings.pop(0)

        l.append((player_a[0], player_a[1], player_b[0], player_b[1]))

    return l


def playersWithoutBye(tournament_id=1):
    """Returns a list of player ids which did not have a bye in this tournament.
    Args:
      tournament_id: the id of the tournament
    """
    db_connect, cursor = connect()

    query = ("SELECT player_id, name FROM tournament_players \
             INNER JOIN players ON tournament_players.player_id = players.id \
             WHERE bye = 0 AND tournament_id = %s;")
    cursor.execute(query, (tournament_id,))

    result = cursor.fetchall()
    db_connect.close()

    return [(int(row[0]), row[1]) for row in result]


def setByeForPlayer(player_id, tournament_id=1):
    """Sets free game to one of the given player.
    Args:
      player_id: the id of the player which just used a bye
      tournament_id: the id of the tournament
    """
    db_connect, cursor = connect()

    query = ("UPDATE tournament_players SET bye = 1 \
              WHERE tournament_id = %s AND player_id = %s;")
    cursor.execute(query, (tournament_id, int(player_id),))
    db_connect.commit()
    db_connect.close()
