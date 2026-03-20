
-- Q12: Batsmen who scored more than average
SELECT batter, SUM(batsman_runs) as total_runs
FROM deliveries
GROUP BY batter
HAVING total_runs > (
    SELECT AVG(player_runs)
    FROM (
        SELECT batter, SUM(batsman_runs) as player_runs
        FROM deliveries
        GROUP BY batter
    )
)
ORDER BY total_runs DESC;

-- Q13: Teams with more wins than average
SELECT winner, COUNT(*) as total_wins
FROM matches
WHERE winner IS NOT NULL
GROUP BY winner
HAVING total_wins > (
    SELECT AVG(team_wins)
    FROM (
        SELECT winner, COUNT(*) as team_wins
        FROM matches
        WHERE winner IS NOT NULL
        GROUP BY winner
    )
)
ORDER BY total_wins DESC;
