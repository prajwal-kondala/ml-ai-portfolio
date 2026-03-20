
-- Q1: All matches in 2020 season
SELECT * FROM matches WHERE season = '2020';

-- Q2: Matches won by CSK
SELECT * FROM matches
WHERE winner = 'Chennai Super Kings'
ORDER BY date;

-- Q3: Top 10 highest margin wins
SELECT id, team1, team2, winner, result_margin
FROM matches
WHERE result = 'runs'
ORDER BY result_margin DESC
LIMIT 10;
