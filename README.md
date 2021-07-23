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
  
## Create superuser
```bash
  $ docker-compose run app python manage.py createsuperuser
  ```
 
## Run tests

```bash
  $ docker-compose run app python manage.py test
  ```

## How to use

Here is API documentaion (all protected endpoints support both token and session as authentication method)

   #### Create new user
 ```bash
    $ curl -XPOST -F 'username="test"' -F 'password="test"' localhost:8000/auth/create-user
   ```
   #### Obtain token
 ```bash
    $ curl -XPOST -F 'username="test"' -F 'password="test"' localhost:8000/auth/token/
   ```
   #### Obtain refresh token
 ```bash
    $ curl -XPOST -F 'token="your sliding token"' localhost:8000/auth/token/refresh
   ```
   #### Login (for browser usage, this endpoint will set a session on your browser) 
 ```bash
    $ curl -XPOST -F 'username="test"' -F 'password="test"' localhost:8000/auth/login
   ```
   #### Me 
 ```bash
    $ curl -H "Authorization: Bearer $token" localhost:8000/auth/user
   ```
   #### Get a random coupon for a specific insurance declared by its id in the url 
 ```bash
    $ curl -XPOST -H "Authorization: Bearer $token" localhost:8000/main-api/get-random-coupon/<int:insurance_id>
   ```
   #### As superuser, get total amount of coupons assigned to users at a certain date for a specific insurance declared by its id in the url
 ```bash
    $ curl -XPOST -H "Authorization: Bearer $token" -F 'year=2021' -F 'month=7' -F 'day=23' -F 'hour=18'  localhost:8000/main-api/get-insurance-coupon-info/<int:insurance_id>
   ```
   
   
    

