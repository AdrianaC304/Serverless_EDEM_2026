const { Storage } = require('@google-cloud/storage');
const storage = new Storage();

exports.copyImage = async (req, res) => {
  const event = req.body;

  // GCS_NOTIFICATION: data comes in the root of the payload
  const fileName = event.name;
  const sourceBucketName = event.bucket;

  // Validate that the payload contains the required fields
  if (!fileName || !sourceBucketName) {
    console.log('No file name or bucket provided, aborting function.');
    console.log('Received payload:', JSON.stringify(event, null, 2));
    res.status(400).send('Bad request');
    return;
  }

  console.log(`Copying file: ${fileName} from bucket ${sourceBucketName}`);

  // Get the source bucket and file
  const sourceBucket = storage.bucket(sourceBucketName);
  const file = sourceBucket.file(fileName);

  // Define the destination bucket
  const destinationBucket = storage.bucket('imagenes-miniaturas');

  try {
    // Copy the file to the destination bucket
    await file.copy(destinationBucket.file(fileName));
    console.log(`File copied to bucket 'imagenes-miniaturas': ${fileName}`);
    res.status(200).send('OK');
  } catch (err) {
    console.error('Error copying the image:', err);
    res.status(500).send('Error copying the image');
  }
};
