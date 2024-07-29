# README

## 1. How to Run a Redis Server on Your Machine

### Installation
- Install Redis on your machine (Linux, macOS, or Windows).
- You can download the Redis .msi file for Windows or follow instructions for other platforms from the [official Redis documentation](https://redis.io/docs/latest/operate/oss_and_stack/install/install-redis/).

### Starting the Redis Server
1. Turn on Windows Subsystem for Linux (WSL) if using Windows.
2. Launch the Redis CLI application.
3. Verify if Redis is working by sending a PING command:
   ```bash
   $ redis-cli ping
   # Should return "PONG"
   ```

## 2. How to Run Simple Operations with the Redis Client

### Basic Commands
- Use `SET` to store a value: `SET key value`
- Retrieve a value with `GET`: `GET key`
- Explore other commands like `HMSET`, `HGET`, and `HINCRBY` for hash operations.

## 3. How to Use a Redis Client with Node.js for Basic Operations

### Installation
- Install the `redis` package using npm:
  ```bash
  $ npm install redis
  ```

### Example Usage
```javascript
const redis = require('redis');
const client = redis.createClient();

// Set a value
client.set('myKey', 'myValue');

// Retrieve a value
client.get('myKey', (err, value) => {
  console.log('Value:', value);
});

// More advanced operations with hashes, lists, etc.
// ...

// Don't forget to handle errors and disconnect gracefully!
```

## 4. How to Store Hash Values in Redis

### Hashes
- Redis hashes are collections of field-value pairs.
- Use `HSET` to set fields within a hash.
- Retrieve values with `HGET` or multiple values with `HMGET`.

## 5. How to Deal with Async Operations with Redis

### Asynchronous Clients
- Redis is single-threaded, but it can manage many client connections concurrently.
- Asynchronous clients (e.g., using Node.js and `async/await`) help maximize performance by handling I/O efficiently.
- Consider pipelining, non-blocking I/O, and multiple client connections.

## 6. How to Use Kue as a Queue System

### Installation
- Install the `kue` package using npm:
  ```bash
  $ npm install kue
  ```

### Example Usage
```javascript
const kue = require('kue');
const queue = kue.createQueue();

// Create a job
const job = queue.create('myJob', { title: 'My Job Title' }).save();

// Process the job
queue.process('myJob', (job, done) => {
  console.log('Processing job:', job.data.title);
  done();
});

// Don't forget to handle errors and shutdown gracefully!
```


## 7. How to Build a Basic Express App Interacting with a Redis Server

### Installation
- Install the `express` and `body-parser` packages using npm:
  ```bash
  $ npm install express body-parser
  ```
- Install the `redis` package if you haven't already:
  ```bash
    $ npm install redis
    ```
- Install the `dotenv` package to manage environment variables:
    ```bash
        $ npm install dotenv
        ```
- Create a `.env` file in the root directory of your project and add the following:
    ```bash
    REDIS_URL=redis://localhost:6379
    ```
- Create a `server.js` file and add the following code:
    ```javascript
    require('dotenv').config();
    const express = require('express');
    const bodyParser = require('body-parser');
    const redis = require('redis');

    const app = express();

    app.use(bodyParser.json());

    const client = redis.createClient(process.env.REDIS_URL);

    app.get('/get/:key', (req, res) => {
      const { key } = req.params;
      client.get(key, (err, value) => {
        if (err) {
          res.status(500).send('Error retrieving value from Redis');
        } else {
          res.send(value);
        }
      });
    });

    app.post('/set', (req, res) => {
      const { key, value } = req.body;
      client.set(key, value, (err) => {
        if (err) {
          res.status(500).send('Error setting value in Redis');
        } else {
          res.send('Value set successfully');
        }
      });
    });

    app.listen(3000, () => {
      console.log('Server running on port 3000');
    });
    ```
- Run the server using `node server.js` and test the endpoints using a tool like Postman.