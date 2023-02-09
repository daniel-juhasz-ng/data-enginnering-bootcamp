-- Q1
select count(*) from `de-bootcamp.trips_data_all.fhv_taxi_data_2019`;

-- Q2
select count(distinct affiliated_base_number) from `de-bootcamp.trips_data_all.fhv_taxi_data_2019`;

-- Q5
create table
  `de-bootcamp.trips_data_all.fhv_taxi_data_2019_int_part`
  (
    dispatching_base_num STRING,
    pickup_datetime timestamp,
    dropOff_datetime timestamp,
    PUlocationID integer,
    DOlocationID integer,
    SR_Flag	string,
    Affiliated_base_number string
  )
partition by
  timestamp_trunc(pickup_datetime, day)
cluster by
  Affiliated_base_number
as (select * from `de-bootcamp.trips_data_all.fhv_taxi_data_2019_int`);

select distinct affiliated_base_number from `de-bootcamp.trips_data_all.fhv_taxi_data_2019_int` where pickup_datetime between '2019-03-01' and '2019-03-31';

-- Q3
select count(*) from `de-bootcamp.trips_data_all.fhv_taxi_data_2019`
where PUlocationID is null and DOlocationID is null;
