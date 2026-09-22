const { Client } = require('@elastic/elasticsearch');

const INDEX_NAME = 'records';

function buildEsClient(node) {
  return new Client({ node });
}

async function ensureIndex(esClient) {
  const exists = await esClient.indices.exists({ index: INDEX_NAME });
  if (!exists) {
    await esClient.indices.create({ index: INDEX_NAME });
    console.log(`[service-b] created Elasticsearch index "${INDEX_NAME}"`);
  }
}

async function indexRecord(esClient, record) {
  await esClient.index({
    index: INDEX_NAME,
    id: record.id,
    document: {
      title: record.title,
      description: record.description,
      createdAt: record.created_at,
    },
    refresh: true,
  });
}

module.exports = { buildEsClient, ensureIndex, indexRecord };
