with data(id, name, score, flag, note, created_at, metadata, linked_ids) as (
    values
        (1, 'a', 1.1, true,  'some,comment', '2000-01-01', {'ip': 'dip', 'key': 0}, [1, 2, 3]),
        (2, 'z', 2.2, false, 'another,note', '9999-12-31', {'ip': 'doo', 'key': 1}, [4, 5, 6])
)

select *
from data
