## How to run

Uses the default Django development server

1. Clone the project from `https://github.com/MohsenZarein/bime-bazar.git`.
  ```bash
  $ git clone https://github.com/MohsenZarein/bime-bazar && cd bime-bazar
  ```
2. Update the environment variables in the docker-compose.yml
3. Build the images and run the containers

  ```bash
  $ docker-compose up
  ```
4. Test it out at http://localhost:8000. The "app" folder is mounted into the container and your code changes apply automatically.
5. To cleanup 
  ```bash
    $ docker-compose down
   ```

## Provide initial data for database

 ```bash
  $ docker-compose run app python manage.py loaddata insurances.json coupons.json
  ```
 
## Run tests

```bash
  $ docker-compose run app python manage.py test
  ```

