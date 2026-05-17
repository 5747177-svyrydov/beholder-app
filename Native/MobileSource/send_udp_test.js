const dgram = require('dgram');
const argv = process.argv.slice(2);

// Usage: node send_udp_test.js [TARGET_IP] [PORT]
// Defaults: TARGET_IP=127.0.0.1 PORT=8484

const TARGET = argv[0] || '127.0.0.1';
const PORT = parseInt(argv[1] || '8484', 10);

const client = dgram.createSocket('udp4');

// Example payload: two markers: "0 320 240 1.57,1 100 200 0.78"
const payload = argv[2] || '0 320 240 1.57,1 100 200 0.78';

const message = Buffer.from(payload);
client.send(message, PORT, TARGET, (err) => {
  if (err) {
    console.error('Send error:', err);
    client.close();
    process.exit(1);
  }
  console.log(`Sent to ${TARGET}:${PORT} -> ${payload}`);
  client.close();
});
