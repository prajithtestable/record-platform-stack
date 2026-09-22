require('dotenv').config();
const { buildClient, watchRecords } = require('./grpcClient');
const { buildEsClient, ensureIndex, indexRecord } = require('./esIndexer');
const { buildSnsClient, publishRecordCreated } = require('./snsPublisher');
const { buildSesClient, sendRecordCreatedEmail } = require('./sesNotifier');

const SERVICE_A_GRPC_ADDR = process.env.SERVICE_A_GRPC_ADDR || 'localhost:50051';
const ELASTICSEARCH_NODE = process.env.ELASTICSEARCH_NODE || 'http://localhost:9200';
const AWS_ENDPOINT = process.env.AWS_ENDPOINT || 'http://localhost:4566';
const AWS_REGION = process.env.AWS_REGION || 'us-east-1';
const SNS_TOPIC_ARN = process.env.SNS_TOPIC_ARN || 'arn:aws:sns:us-east-1:000000000000:record-created';
const SES_FROM_EMAIL = process.env.SES_FROM_EMAIL || 'notifications@record-platform.local';
const SES_TO_EMAIL = process.env.SES_TO_EMAIL || 'ops@record-platform.local';

async function main() {
  const esClient = buildEsClient(ELASTICSEARCH_NODE);
  await ensureIndex(esClient);

  const snsClient = buildSnsClient({ endpoint: AWS_ENDPOINT, region: AWS_REGION });
  const sesClient = buildSesClient({ endpoint: AWS_ENDPOINT, region: AWS_REGION });

  const grpcClient = buildClient(SERVICE_A_GRPC_ADDR);
  console.log(`[service-b] watching service-a at ${SERVICE_A_GRPC_ADDR}`);

  watchRecords(grpcClient, async (record) => {
    console.log(`[service-b] received record ${record.id} ("${record.title}")`);

    try {
      await indexRecord(esClient, record);
      console.log(`[service-b] indexed record ${record.id} into Elasticsearch`);
    } catch (err) {
      console.error(`[service-b] failed to index record ${record.id}`, err.message);
    }

    try {
      await publishRecordCreated(snsClient, SNS_TOPIC_ARN, record);
      console.log(`[service-b] published record.created for ${record.id} to SNS`);
    } catch (err) {
      console.error(`[service-b] failed to publish SNS event for ${record.id}`, err.message);
    }

    try {
      await sendRecordCreatedEmail(sesClient, { from: SES_FROM_EMAIL, to: SES_TO_EMAIL, record });
      console.log(`[service-b] sent SES notification for ${record.id}`);
    } catch (err) {
      console.error(`[service-b] failed to send SES email for ${record.id}`, err.message);
    }
  });
}

main().catch((err) => {
  console.error('[service-b] fatal startup error', err);
  process.exit(1);
});
