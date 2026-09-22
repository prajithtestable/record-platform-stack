const mongoose = require('mongoose');

const recordSchema = new mongoose.Schema({
  title: { type: String, required: true },
  description: { type: String, default: '' },
  createdAt: { type: Date, default: Date.now },
});

recordSchema.set('toJSON', {
  transform: (_doc, ret) => ({
    id: ret._id.toString(),
    title: ret.title,
    description: ret.description,
    createdAt: ret.createdAt.toISOString(),
  }),
});

module.exports = mongoose.model('Record', recordSchema);
