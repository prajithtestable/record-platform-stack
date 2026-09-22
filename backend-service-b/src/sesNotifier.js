const { SESClient, SendEmailCommand } = require('@aws-sdk/client-ses');

function buildSesClient({ endpoint, region }) {
  return new SESClient({ endpoint, region });
}

async function sendRecordCreatedEmail(sesClient, { from, to, record }) {
  const command = new SendEmailCommand({
    Source: from,
    Destination: { ToAddresses: [to] },
    Message: {
      Subject: { Data: `New record created: ${record.title}` },
      Body: {
        Text: {
          Data: `A new record was created.\n\nID: ${record.id}\nTitle: ${record.title}\nDescription: ${record.description}\nCreated: ${record.created_at}`,
        },
      },
    },
  });
  return sesClient.send(command);
}

module.exports = { buildSesClient, sendRecordCreatedEmail };
