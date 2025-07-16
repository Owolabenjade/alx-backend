import express from 'express';
import { createClient } from 'redis';
import { promisify } from 'util';
import kue from 'kue';

const app = express();
const client = createClient();
const queue = kue.createQueue();
const getAsync = promisify(client.get).bind(client);

let reservationEnabled = true;

function reserveSeat(number) {
  client.set('available_seats', number);
}

async function getCurrentAvailableSeats() {
  const seats = await getAsync('available_seats');
  return seats ? parseInt(seats) : 0;
}

// Initialize available seats
reserveSeat(50);

app.get('/available_seats', async (req, res) => {
  const numberOfAvailableSeats = await getCurrentAvailableSeats();
  res.json({ numberOfAvailableSeats: numberOfAvailableSeats.toString() });
});

app.get('/reserve_seat', (req, res) => {
  if (!reservationEnabled) {
    res.json({ status: 'Reservation are blocked' });
    return;
  }

  const job = queue.create('reserve_seat')
    .save((err) => {
      if (err) {
        res.json({ status: 'Reservation failed' });
      } else {
        res.json({ status: 'Reservation in process' });
      }
    });

  job.on('complete', () => {
    console.log(`Seat reservation job ${job.id} completed`);
  });

  job.on('failed', (err) => {
    console.log(`Seat reservation job ${job.id} failed: ${err.message}`);
  });
});

app.get('/process', (req, res) => {
  res.json({ status: 'Queue processing' });
  
  queue.process('reserve_seat', async (job, done) => {
    const currentSeats = await getCurrentAvailableSeats();
    const newSeats = currentSeats - 1;
    
    if (newSeats === 0) {
      reservationEnabled = false;
    }
    
    if (newSeats >= 0) {
      reserveSeat(newSeats);
      done();
    } else {
      done(new Error('Not enough seats available'));
    }
  });
});

app.listen(1245, () => {
  console.log('Server running on port 1245');
});
