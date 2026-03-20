
-- Q14: Season wise top scorer (CTE + Window Function)
WITH season_runs AS (
    SELECT m.season,
           d.batter,
           SUM(d.batsman_runs) as total_runs
    FROM deliveries d
    JOIN matches m ON d.match_id = m.id
    GROUP BY m.season, d.batter
),
ranked AS (
    SELECT season, batter, total_runs,
           RANK() OVER (
               PARTITION BY season 
               ORDER BY total_runs DESC
           ) as rnk
    FROM season_runs
)
SELECT season, batter, total_runs
FROM ranked
WHERE rnk = 1
ORDER BY season;

-- Q15: Running total of team wins per season
SELECT season, winner,
       COUNT(*) as season_wins,
       SUM(COUNT(*)) OVER (
           PARTITION BY winner
           ORDER BY season
       ) as cumulative_wins
FROM matches
WHERE winner IS NOT NULL
GROUP BY season, winner
ORDER BY winner, season;
