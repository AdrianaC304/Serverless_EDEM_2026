const { Storage } = require('@google-cloud/storage');
const storage = new Storage();

exports.copyImage = async (req, res) => {
  const event = req.body;

  // GCS_NOTIFICATION: los datos vienen en la raíz
  const fileName = event.name;
  const sourceBucketName = event.bucket;

  if (!fileName || !sourceBucketName) {
    console.log('No hay nombre de archivo o bucket, abortando función.');
    console.log('Payload recibido:', JSON.stringify(event, null, 2));
    res.status(400).send('Bad request');
    return;
  }

  console.log(`Copiando archivo: ${fileName} del bucket ${sourceBucketName}`);

  const sourceBucket = storage.bucket(sourceBucketName);
  const file = sourceBucket.file(fileName);
  const destinationBucket = storage.bucket('imagenes-miniaturas');

  try {
    await file.copy(destinationBucket.file(fileName));
    console.log(`Archivo copiado al bucket imagenes-miniaturas': ${fileName}`);
    res.status(200).send('OK');
  } catch (err) {
    console.error('Error copiando la imagen:', err);
    res.status(500).send('Error copiando la imagen');
  }
};