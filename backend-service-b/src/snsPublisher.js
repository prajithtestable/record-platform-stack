const { SNSClient, PublishCommand } = require('@aws-sdk/client-sns');

function buildSnsClient({ endpoint, region }) {
  return new SNSClient({ endpoint, region });
}

async function publishRecordCreated(snsClient, topicArn, record) {
  const command = new PublishCommand({
    TopicArn: topicArn,
    Message: JSON.stringify({
      event: 'record.created',
      record,
    }),
    MessageAttributes: {
      eventType: { DataType: 'String', StringValue: 'record.created' },
    },
  });
  return snsClient.send(command);
}

module.exports = { buildSnsClient, publishRecordCreated };
