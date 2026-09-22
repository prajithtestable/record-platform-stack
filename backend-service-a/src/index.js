require('dotenv').config();
const mongoose = require('mongoose');
const { buildServer } = require('./grpcServer');
const { buildApp } = require('./restServer');

const MONGO_URI = process.env.MONGO_URI || 'mongodb://localhost:27017/records';
const GRPC_PORT = process.env.GRPC_PORT || '50051';
const HTTP_PORT = process.env.HTTP_PORT || '3001';

async function main() {
  await mongoose.connect(MONGO_URI);
  console.log(`[service-a] connected to MongoDB at ${MONGO_URI}`);

  const grpcServer = buildServer();
  grpcServer.bindAsync(
    `0.0.0.0:${GRPC_PORT}`,
    require('@grpc/grpc-js').ServerCredentials.createInsecure(),
    (err, port) => {
      if (err) throw err;
      console.log(`[service-a] gRPC server listening on ${port}`);
    },
  );

  const app = buildApp();
  app.listen(HTTP_PORT, () => {
    console.log(`[service-a] REST API listening on ${HTTP_PORT}`);
  });
}

main().catch((err) => {
  console.error('[service-a] fatal startup error', err);
  process.exit(1);
});
