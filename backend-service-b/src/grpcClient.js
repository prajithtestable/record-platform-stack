const path = require('path');
const grpc = require('@grpc/grpc-js');
const protoLoader = require('@grpc/proto-loader');

const PROTO_PATH = path.join(__dirname, '..', '..', 'shared', 'proto', 'records.proto');

const packageDefinition = protoLoader.loadSync(PROTO_PATH, {
  keepCase: false,
  longs: String,
  enums: String,
  defaults: true,
  oneofs: true,
});

const recordsProto = grpc.loadPackageDefinition(packageDefinition).records;

function buildClient(address) {
  return new recordsProto.RecordService(address, grpc.credentials.createInsecure());
}

// Point lookup against service-a, exposed for completeness / future use.
function getRecord(client, id) {
  return new Promise((resolve, reject) => {
    client.getRecord({ id }, (err, response) => {
      if (err) return reject(err);
      resolve(response);
    });
  });
}

// Subscribes to service-a's WatchRecords stream and invokes onRecord for
// each record as it arrives. Reconnects with backoff if the stream drops.
function watchRecords(client, onRecord) {
  const call = client.watchRecords({});

  call.on('data', (record) => onRecord(record));
  call.on('error', (err) => {
    console.error('[service-b] WatchRecords stream error, reconnecting in 3s:', err.message);
    setTimeout(() => watchRecords(client, onRecord), 3000);
  });
  call.on('end', () => {
    console.warn('[service-b] WatchRecords stream ended, reconnecting in 3s');
    setTimeout(() => watchRecords(client, onRecord), 3000);
  });
}

module.exports = { buildClient, getRecord, watchRecords };
