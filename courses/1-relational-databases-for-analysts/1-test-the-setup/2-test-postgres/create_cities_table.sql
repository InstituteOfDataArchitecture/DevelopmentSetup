create table if not exists one_one.cities as
select
    1 as city_id,
    'Greater Copenhagen' as city,
    2000000 as population
union all
select
    2 as city_id,
    'Dubai' as city,
    3300000 as population
union all
select
    3 as city_id,
    'Bangkok' as city,
    10700000 as population
union all
select
    4 as city_id,
    'Metro Manila' as city,
    13500000 as population;
