-- Question 3.
select count(1) from green_taxi_trips
where
	lpep_pickup_datetime >= '2019-01-15'
	and lpep_pickup_datetime < '2019-01-16'
	and lpep_dropoff_datetime >= '2019-01-15'
	and lpep_dropoff_datetime < '2019-01-16'

-- Question 4.
select lpep_pickup_datetime from green_taxi_trips
order by trip_distance desc
limit 1

-- Question 5.
select count(1) from green_taxi_trips
where
	lpep_pickup_datetime >= '2019-01-01'
	and lpep_pickup_datetime < '2019-01-02'
	and lpep_dropoff_datetime >= '2019-01-01'
	and lpep_dropoff_datetime < '2019-01-02'
	and passenger_count = 2

select count(1) from green_taxi_trips
where
	lpep_pickup_datetime >= '2019-01-01'
	and lpep_pickup_datetime < '2019-01-02'
	and lpep_dropoff_datetime >= '2019-01-01'
	and lpep_dropoff_datetime < '2019-01-02'
	and passenger_count = 3

-- Question 6.
select dotz."Zone"
from green_taxi_trips t
	join taxi_zone putz on t."PULocationID" = putz."LocationID"
	join taxi_zone dotz on t."DOLocationID" = dotz."LocationID"
where putz."Zone" = 'Astoria'
order by t.tip_amount desc
limit 1