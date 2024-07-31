// Implementing a seat reservation system using Redis.
const express = require('express');
const redis = require('redis');
const { promisify } = require('util');
const kue = require('kue');


const client = redis.createClient();

client.on('connect', () => {
    console.log('Connected to Redis');
});

client.on('error', (err) => {
    console.error('Redis error:', err);
});

const getAsync = promisify(client.get).bind(client);
const setAsync = promisify(client.set).bind(client);

function reserveSeat(number) {
    client.set('available_seats', number);
}

function getCurrentAvailableSeats() {
    return getAsync('available_seats');
}

reserveSeat(50);

let reservationEnabled = true;

const queue = kue.createQueue();


const app = express();
const port = 1245;

app.get('/available_seats', async (req, res) => {
    const availableSeats = await getCurrentAvailableSeats();
    res.json({ availableSeats });
});

app.get('/reserve_seat', async (req, res) => {
    if (!reservationEnabled) {
        return res.json({ status: 'Reservation are blocked' });
    }

    const job = queue.create('reserve_seat').save((err) => {
        if (err) {
            return res.json({ status: 'Reservation failed' });
        }
        res.json({ status: 'Reservation in process' });
    });

    job.on('complete', () => {
        console.log(`Seat reservation job ${job.id} completed`);
    });
    job.on('failed', (err) => {
        console.log(`Seat reservation job ${job.id} failed: ${err}`);
    });
});


app.get('/process', async (req, res) => {
    queue.process('reserve_seat', async (job, done) => {
        let availableSeats = await getCurrentAvailableSeats();
        availableSeats = parseInt(availableSeats, 10);
        if (availableSeats <= 0) {
            done(Error('Not enough seats available'));
        } else {
            availableSeats -= 1;
            await setAsync('available_seats', availableSeats);
            if (availableSeats === 0) {
                reservationEnabled = false;
            }
            done();
        }
    });

    res.json({ status: 'Queue processing' });
});

app.listen(port, () => {
    console.log(`Server running on port ${port}`);
});