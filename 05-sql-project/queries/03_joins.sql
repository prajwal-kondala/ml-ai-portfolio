
-- Q10: Season wise batting stats (INNER JOIN)
SELECT m.season, 
       d.batter,
       SUM(d.batsman_runs) as season_runs
FROM matches m
INNER JOIN deliveries d ON m.id = d.match_id
GROUP BY m.season, d.batter
ORDER BY m.season, season_runs DESC
LIMIT 20;

-- Q11: Player of match with match details
SELECT m.date, m.team1, m.team2,
       m.player_of_match, m.winner
FROM matches m
WHERE m.player_of_match IS NOT NULL
ORDER BY m.date DESC
LIMIT 20;
