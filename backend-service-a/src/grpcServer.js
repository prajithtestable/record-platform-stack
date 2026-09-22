const path = require('path');
const grpc = require('@grpc/grpc-js');
const protoLoader = require('@grpc/proto-loader');
const RecordModel = require('./models/record');

const PROTO_PATH = path.join(__dirname, '..', '..', 'shared', 'proto', 'records.proto');

const packageDefinition = protoLoader.loadSync(PROTO_PATH, {
  keepCase: false,
  longs: String,
  enums: String,
  defaults: true,
  oneofs: true,
});

const recordsProto = grpc.loadPackageDefinition(packageDefinition).records;

// Subscribers currently attached to WatchRecords, notified whenever a
// record is created via the REST endpoint.
const watchers = new Set();

function toWireRecord(doc) {
  return {
    id: doc._id.toString(),
    title: doc.title,
    description: doc.description || '',
    created_at: doc.createdAt.toISOString(),
  };
}

// Called by the REST layer right after a record is persisted, so every
// connected WatchRecords stream (service-b) sees it immediately.
function publishRecord(doc) {
  const wireRecord = toWireRecord(doc);
  for (const call of watchers) {
    call.write(wireRecord);
  }
}

async function getRecord(call, callback) {
  try {
    const doc = await RecordModel.findById(call.request.id);
    if (!doc) {
      return callback({ code: grpc.status.NOT_FOUND, message: 'record not found' });
    }
    callback(null, toWireRecord(doc));
  } catch (err) {
    callback({ code: grpc.status.INTERNAL, message: err.message });
  }
}

function watchRecords(call) {
  watchers.add(call);
  call.on('cancelled', () => watchers.delete(call));
  call.on('error', () => watchers.delete(call));
}

function buildServer() {
  const server = new grpc.Server();
  server.addService(recordsProto.RecordService.service, {
    getRecord,
    watchRecords,
  });
  return server;
}

module.exports = { buildServer, publishRecord };
