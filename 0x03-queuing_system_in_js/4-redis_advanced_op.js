import { createClient } from 'redis';

const client = createClient();

client.on('connect', () => {
  console.log('Redis client connected to the server');
});

client.on('error', (err) => {
  console.log(`Redis client not connected to the server: ${err}`);
});

// Create Hash
client.hset('ALX', 'Portland', 50, (err, reply) => {
  if (err) console.log(err);
  else console.log(`Reply: ${reply}`);
});

client.hset('ALX', 'Seattle', 80, (err, reply) => {
  if (err) console.log(err);
  else console.log(`Reply: ${reply}`);
});

client.hset('ALX', 'New York', 20, (err, reply) => {
  if (err) console.log(err);
  else console.log(`Reply: ${reply}`);
});

client.hset('ALX', 'Bogota', 20, (err, reply) => {
  if (err) console.log(err);
  else console.log(`Reply: ${reply}`);
});

client.hset('ALX', 'Cali', 40, (err, reply) => {
  if (err) console.log(err);
  else console.log(`Reply: ${reply}`);
});

client.hset('ALX', 'Paris', 2, (err, reply) => {
  if (err) console.log(err);
  else console.log(`Reply: ${reply}`);
});

// Display Hash
client.hgetall('ALX', (err, result) => {
  if (err) {
    console.log(err);
  } else {
    console.log(result);
  }
});
