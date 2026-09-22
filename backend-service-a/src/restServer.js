const express = require('express');
const cors = require('cors');
const RecordModel = require('./models/record');
const { publishRecord } = require('./grpcServer');

function buildApp() {
  const app = express();
  app.use(cors());
  app.use(express.json());

  app.get('/health', (_req, res) => res.json({ status: 'ok', service: 'backend-service-a' }));

  // List records (used by the Angular frontend to render the table).
  app.get('/records', async (_req, res) => {
    const docs = await RecordModel.find().sort({ createdAt: -1 }).limit(200);
    res.json(docs.map((doc) => doc.toJSON()));
  });

  app.get('/records/:id', async (req, res) => {
    const doc = await RecordModel.findById(req.params.id);
    if (!doc) return res.status(404).json({ error: 'not found' });
    res.json(doc.toJSON());
  });

  // Create a record: persist to MongoDB, then push it down the gRPC
  // WatchRecords stream so service-b can index/notify/publish.
  app.post('/records', async (req, res) => {
    const { title, description } = req.body || {};
    if (!title) return res.status(400).json({ error: 'title is required' });

    const doc = await RecordModel.create({ title, description: description || '' });
    publishRecord(doc);
    res.status(201).json(doc.toJSON());
  });

  return app;
}

module.exports = { buildApp };
