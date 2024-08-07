# Savsa

<div style="text-align: center;"><p>
    <img src="https://github.com/HarbourHeading/savsa/assets/69332989/b7593a05-bc83-41aa-ac92-f8c20da33964" width="1080" height="400" alt="project preview"/>
</p></div>

<small><i>
    Example image. Entire website not shown. [Preview project](http://18.197.222.75/).
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
mkdir -p -- data/docker-entrypoint-initdb.d ; cd data/docker-entrypoint-initdb.d ; vim mongo-init.js
```

Edit `mongo-init.js`, and copy the data below:

```
db = db.getSiblingDB(dbName);

// Create a database user. Edit credentials to fit your own.
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

// Create MongoDB collection to store steamIDs
db.createCollection("profiles")

// 2 Sample steamID values
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
