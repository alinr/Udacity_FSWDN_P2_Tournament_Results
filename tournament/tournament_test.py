#!/usr/bin/env python
#
# Test cases for tournament.py

from tournament import *

def testDeleteMatches():
    """Test if the match records can be deleted from database."""
    deleteMatches()
    print "1. Old matches can be deleted."


def testDelete():
    """Test if player records can be deleted from database."""
    deleteMatches()
    deleteTournamentPlayers()
    deletePlayers()
    print "2. Player records can be deleted."


def testCount():
    """Test if the count function works."""
    deleteMatches()
    deletePlayers()
    c = countPlayers()
    if c == '0':
        raise TypeError(
            "countPlayers() should return numeric zero, not string '0'.")
    if c != 0:
        raise ValueError("After deleting, countPlayers should return zero.")
    print "3. After deleting, countPlayers() returns zero."


def testRegister():
    """Test if players can be registered to database."""
    deleteMatches()
    deletePlayers()
    registerPlayer("Chandra Nalaar")
    c = countPlayers()
    if c != 1:
        raise ValueError(
            "After one player registers, countPlayers() should be 1.")
    print "4. After registering a player, countPlayers() returns 1."


def testRegisterCountDelete():
    """Test if players can be registered and deleted from database."""
    deleteMatches()
    deletePlayers()
    registerPlayer("Markov Chaney")
    registerPlayer("Joe Malik")
    registerPlayer("Mao Tsu-hsi")
    registerPlayer("Atlanta Hope")
    c = countPlayers()
    if c != 4:
        raise ValueError(
            "After registering four players, countPlayers should be 4.")
    deletePlayers()
    c = countPlayers()
    if c != 0:
        raise ValueError("After deleting, countPlayers should return zero.")
    print "5. Players can be registered and deleted."


def testStandingsBeforeMatches():
    """Test if players Newly registered players appear
    in the standings with no matches."""
    deleteMatches()
    deletePlayers()
    registerPlayer("Melpomene Murray")
    registerPlayer("Randy Schwartz")
    standings = playerStandings()
    if len(standings) < 2:
        raise ValueError("Players should appear in playerStandings even before "
                         "they have played any matches.")
    elif len(standings) > 2:
        raise ValueError("Only registered players should appear in standings.")
    if len(standings[0]) != 4:
        raise ValueError("Each playerStandings row should have four columns.")
    [(id1, name1, wins1, matches1), (id2, name2, wins2, matches2)] = standings
    if matches1 != 0 or matches2 != 0 or wins1 != 0 or wins2 != 0:
        raise ValueError(
            "Newly registered players should have no matches or wins.")
    if set([name1, name2]) != set(["Melpomene Murray", "Randy Schwartz"]):
        raise ValueError("Registered players' names should appear in standings, "
                         "even if they have no matches played.")
    print "6. Newly registered players appear in the standings with no matches."


def testReportMatches():
    """Test if after a match, players have updated standings."""
    deleteMatches()
    deletePlayers()
    registerPlayer("Bruno Walton")
    registerPlayer("Boots O'Neal")
    registerPlayer("Cathy Burton")
    registerPlayer("Diane Grant")
    standings = playerStandings()
    [id1, id2, id3, id4] = [row[0] for row in standings]
    reportMatch(id1, id2, id1)
    reportMatch(id3, id4, id3)

    standings = playerStandings()
    for (i, n, w, m) in standings:
        if m != 1:
            raise ValueError("Each player should have one match recorded.")
        if i in (id1, id3) and w != 1:
            raise ValueError("Each match winner should have one win recorded.")
        elif i in (id2, id4) and w != 0:
            raise ValueError("Each match loser should have zero wins recorded.")
    print "7. After a match, players have updated standings."


def testPairings():
    """Test if after one match, players with one win are paired."""
    deleteMatches()
    deletePlayers()
    registerPlayer("Bruno Walton")
    registerPlayer("Boots O'Neal")
    registerPlayer("Cathy Burton")
    registerPlayer("Diane Grant")
    standings = playerStandings()
    [id1, id2, id3, id4] = [row[0] for row in standings]
    reportMatch(id1, id2, id1)
    reportMatch(id3, id4, id3)
    pairings = swissPairings()
    if len(pairings) != 2:
        raise ValueError(
            "For four players, swissPairings should return two pairs.")
    [(pid1, pname1, pid2, pname2), (pid3, pname3, pid4, pname4)] = pairings
    correct_pairs = set([frozenset([id1, id3]), frozenset([id2, id4])])
    actual_pairs = set([frozenset([pid1, pid2]), frozenset([pid3, pid4])])
    if correct_pairs != actual_pairs:
        raise ValueError(
            "After one match, players with one win should be paired.")
    print "8. After one match, players with one win are paired."



def testOddPairings():
    """Test if pairing of odd numbers of players works. One player should
    get bye and should be excluded from getting another bye."""
    deleteMatches()
    deletePlayers()
    registerPlayer("Bruno Walton")
    registerPlayer("Boots O'Neal")
    registerPlayer("Cathy Burton")
    registerPlayer("Diane Grant")
    registerPlayer("John Doe")

    pairings = swissPairings()
    if len(pairings) != 2:
        raise ValueError("For five players, swissPairings should return two pairs.")

    standings = playerStandings()

    playerWithBye = [(row[0], row[1]) for row in standings if row[2] == 1]

    otherPlayers = playersWithoutBye()

    if playerWithBye in otherPlayers:
        raise ValueError("Player with bye contained in collection of players without bye.")
    print "9. Pairings with odd number of players: one player get a bye \
    and will be excluded from getting another bye."


def testDraw():
    """Test if after having a draw match, both players have one
    match and no wins"""
    deleteMatches()
    deletePlayers()
    registerPlayer("Bruno Walton")
    registerPlayer("Boots O'Neal")

    standings = playerStandings()
    [id1, id2] = [row[0] for row in standings]
    reportMatch(id1, id2, None)

    standings = playerStandings()
    for row in standings:
        if row[2] != 0:
            raise ValueError(str.format("Player '{0}' has a win.", row[1]))
        if row[3] != 1:
            raise ValueError(str.format("Player '{0}' has an invalid number of games.", row[1]))

    print "10. After having a draw match, both players have one match and no wins"


def testRankingOrder():
    """Test if After playing four matches (including one draw)
    the player standings are in the correct order. """
    deleteMatches()
    deletePlayers()
    registerPlayer("Bruno Walton")
    registerPlayer("Boots O'Neal")
    registerPlayer("Cathy Burton")
    registerPlayer("Diane Grant")

    standings = playerStandings()

    [id1, id2, id3, id4] = [row[0] for row in standings]

    reportMatch(id1, id2, id1) # Boots O'Neal wins
    reportMatch(id3, id4, id3) # Bruno Walton wins

    reportMatch(id1, id3, id1) # Boots O'Neal wins
    reportMatch(id2, id4, None) # draw


    standings = playerStandings()

    if standings[0][0] != id1:
        raise ValueError("The first player must be 'Boots O'Neal'.")

    if standings[1][0] != id3:
        raise ValueError("The second player must be 'Bruno Walton'.")

    if standings[2][0] != id2:
        # as she lost against the player with the most wins
        raise ValueError("The third player must be 'Diane Grant'.")

    if standings[3][0] != id4:
        raise ValueError("The fourth player must be 'Cathy Burton'.")

    print "11. After playing four matches (including one draw) \
    the player standings are in the correct order."

if __name__ == '__main__':
    testDeleteMatches()
    testDelete()
    testCount()

    # delete & register Dummy tournament, so that the test user can be created
    deleteTournaments()
    registerTournament("Tournament ABC", 1)

    testRegister()
    testRegisterCountDelete()
    testStandingsBeforeMatches()
    testReportMatches()
    testPairings()
    print "Success!  All tests pass!"

    print "Additional tests to pass:"
    testOddPairings()
    testDraw()
    testRankingOrder()
    print "Success!  All additional tests pass!"
