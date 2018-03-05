# SQL tips

## Expand the row by differet field type

table `user_action`: 
```
|  user_id | key_type   | key_id |  action   |
|    123   | 'topic'    |  12    |  'click'  |
|    123   | 'topic'    |  13    |  'browse' |
|    123   | 'category' |  14    |  'click'  |
```

get the aggr table:
```
SELECT
    a.user_id,
    CASE
      WHEN a.key_type = 'topic' THEN t.name
      WHEN a.key_type = 'category' THEN c.name
      ELSE 'unknown'
    END type_name,
    a.action,
    COUNT(*) cnt
FROM user_action a
LEFT JOIN topic t ON (a.key_id = t.id)
LEFT JOIN category c ON (a.key_id = c.id)
GROUP BY 1, 2, 3
```

Unfortunately, this is not correct...

Because if topic and category tables share the same id, the `user_action` will expand to multiple duplicated rows.

The right solution is either with `DISTINCT` then `GROUP BY`
```
SELECT q.user_id, q.type_name, q.action, COUNT(*) cnt
FROM (
    SELECT DISTINCT
        a.user_id,
        CASE
          WHEN a.key_type = 'topic' THEN t.name
          WHEN a.key_type = 'category' THEN c.name
          ELSE 'unknown'
        END type_name,
        a.action
    FROM user_action a
    LEFT JOIN topic t ON (a.key_id = t.id)
    LEFT JOIN category c ON (a.key_id = c.id)
) q
GROUP BY 1, 2, 3
```
or divide and with `UNION ALL`
```
SELECT
    q.user_id,
    t.name type_name,
    q.action,
    COUNT(*) cnt
FROM user_action a
INNER JOIN topic t ON (a.key_id = t.id)
GROUP BY 1, 2, 3

UNION ALL

SELECT
    q.user_id,
    c.name type_name,
    q.action,
    COUNT(*) cnt
FROM user_action a
INNER JOIN category c ON (a.key_id = c.id)
GROUP BY 1, 2, 3
```
