# Savsa

<p align="center">
    <img src="https://github.com/HarbourHeading/savsa/assets/69332989/b7593a05-bc83-41aa-ac92-f8c20da33964" width="1080" height="500"/>
</p>

<small><i>
    Example image. Entire website not shown.
</small></i>

## Introduction

A fun twist of the popular web game genre "Guess the rank" where you guess the age of a steam account based on level, recent games and more. As per [Steam's Web API Terms of Use](https://steamcommunity.com/dev/apiterms), the sample profiles are added with explicit permission from all parties involved.

## Getting started

### Docker

Clone the repository:

```
git clone https://github.com/HarbourHeading/savsa
```

Change directory to the project's root directory:

```
cd savsa
```

Rename `.env.example` to `.env` and add credentials:

```
mv .env.example .env
```

Create a `/data/docker-entrypoint-initdb.d/` directory with a `mongo-init.js` file inside:

```
mkdir -p -- data/docker-entrypoint-initdb.d ; cd data/docker-entrypoint-initdb.d ; touch mongo-init.js
```

To `mongo-init.js`, Add an account and sample data. Replace user credentials:

```
db = db.getSiblingDB(dbName);

db.createUser(
    {
        user: user,
        pwd: password,
        roles: [
            {
                role: "readWrite",
                db: dbName
            }
        ]
    }
)

db.createCollection("profiles")

// 2 Sample values
db.profiles.insertMany([{steamid: "76561198247488342"}, {steamid: "76561198987276257"}])
```

Run `docker-compose.yml`:

```
docker-compose up -d
```

## Contributing

- Fork the repository.

- Don’t forget to add tests.

- Submit a pull request.

## License

MIT License.
