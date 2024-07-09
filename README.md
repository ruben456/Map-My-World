# MAP MY WORLD - APP

Technical Test proyect made by Ruben Hernandez

# REQUERIMENTS

```bash
docker
docker-compose
```

# INSTALATION AND SET UP

Build the containers

```bash
docker compose build
```

Run the proyect containers

```bash
docker compose up
```

# USE 

If you prefer you can populate the database with the following sql commands in order:

``` sql
insert into categories (name) 
values ('Restaurants'), ('Museums'), ('Bars')
```

``` sql
insert into locations (latitude, longitude, category_id) 
values ('4.61501', '-74.114209', 2), ('4.601847', '-74.110715', 4), ('4.614843', '-74.069306', 3)
```

``` sql
insert into location_category_reviewed (location_id, category_id, reviewed, review_at) 
values (4, 2, false, null), (5, 4, false, null), (6, 3, false, null)
```

After run the proyect, go to http://localhost:8080/docs

Use the documentation to request the diferent endpoints

# TEST

To run test, use the next command in a terminal when the container is running:

```bash
docker run mapmyworld-map_my_world pytest
```