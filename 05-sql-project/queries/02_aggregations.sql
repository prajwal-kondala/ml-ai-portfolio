
-- Q4: Total wins per team
SELECT winner, COUNT(*) as total_wins
FROM matches
WHERE winner IS NOT NULL
GROUP BY winner
ORDER BY total_wins DESC;

-- Q5: IPL titles (Finals only)
SELECT winner, COUNT(*) as titles
FROM matches
WHERE match_type = 'Final'
AND winner IS NOT NULL
GROUP BY winner
ORDER BY titles DESC;

-- Q6: Top 10 batsmen all time
SELECT batter, SUM(batsman_runs) as total_runs
FROM deliveries
GROUP BY batter
ORDER BY total_runs DESC
LIMIT 10;

-- Q7: Top 10 wicket takers
SELECT bowler, COUNT(*) as total_wickets
FROM deliveries
WHERE is_wicket = 1
AND dismissal_kind NOT IN ('run out', 'retired hurt', 'obstructing the field')
GROUP BY bowler
ORDER BY total_wickets DESC
LIMIT 10;

-- Q8: Toss analysis
SELECT 
    COUNT(*) as total_matches,
    SUM(CASE WHEN toss_winner = winner THEN 1 ELSE 0 END) as toss_winner_won,
    ROUND(SUM(CASE WHEN toss_winner = winner THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as win_percentage
FROM matches
WHERE winner IS NOT NULL;

-- Q9: Toss decision preference
SELECT toss_decision, COUNT(*) as count
FROM matches
GROUP BY toss_decision;
