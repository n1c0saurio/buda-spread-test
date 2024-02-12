# Spread API

Buda.com coding test, that consist on create an API that calculate the spread of all cryptocurrency markets available through the [Buda API](https://api.buda.com/#la-api-de-buda-com), also allowing to save a spread of a specific market to compare it later with the current one.

This API was developed in Django, with Django Rest Framework and DRF Spectacular for the documentation, using a PostgreSQL database for persistence. You can recreate the develop environment by cloning this repository, creating a `.env` file in the root directory, containing all the environment variables used in the `compose.yml` already included, and then running it.

The environment variables that needs to be set are the following ones:

-   `APP_SECRET`
-   `APP_EXPOSED`
-   `DB_PORT`
-   `DB_NAME`
-   `DB_USER`
-   `DB_PASSWORD`
-   `DB_EXPOSED`

<!-- Alternatively, you can run this proyect directly through the image [available on Docker Hub](), using this `compose.yml` as a base:

```yaml
version: "3"
services:
    web:
        image: n1c0saurio/buda_spread_api:latest
        environment:
            - SESSION_SECRET=keyboardcat
            - DB_HOST=db
            - DB_PORT=5432
            - DB_NAME=buda
            - DB_USER=satoshi
            - DB_PASSWORD=bananacat
        ports:
            - 8000:8000
    db:
        image: postgres:16.1-alpine3.19
        environment:
            - POSTGRES_DB=buda
            - POSTGRES_USER=satoshi
            - POSTGRES_PASSWORD=bananacat
        ports:
            - 5432:5432
``` -->

Deleveloped using [Codium](https://github.com/VSCodium/vscodium/) and Docker under Fedora Linux.
