// index.js
const { Firestore } = require('@google-cloud/firestore');
const { PubSub } = require('@google-cloud/pubsub');

const firestore = new Firestore();
const pubsub = new PubSub();

const OUTPUT_TOPIC = 'podcastLanguageResult';

/**
 * Cloud Function 2nd Gen activada por Pub/Sub
 */
exports.getEpisodeLanguage = async (message, context) => {
  try {
    // Decode the Pub/Sub message
    const msgStr = Buffer.from(message.data, 'base64').toString();
    const data = JSON.parse(msgStr);

    const { episode_id } = data;
    if (!episode_id) {
      console.error("No se recibió episode_id en el mensaje");
      return;
    }

    console.log(`Buscando lenguaje para episode_id: ${episode_id}`);

    //Firestore
    const querySnapshot = await firestore
      .collection('transcripciones')
      .where('episode_id', '==', episode_id)
      .limit(1)
      .get();

    if (querySnapshot.empty) {
      console.log(`No se encontró transcripción para episode_id: ${episode_id}`);
      return;
    }

    const doc = querySnapshot.docs[0];
    const episodeData = doc.data();
    const language = episodeData.language;

    console.log(`Idioma del episodio ${episode_id}: ${language}`);

    // Publish the language in another Pub/Sub topic.
    const payload = {
      episode_id,
      language
    };

    const dataBuffer = Buffer.from(JSON.stringify(payload));
    await pubsub.topic(OUTPUT_TOPIC).publish(dataBuffer);

    console.log(`Idioma publicado en topic ${OUTPUT_TOPIC}`);

    return `Idioma procesado: ${language}`;
  } catch (error) {
    console.error("Error al procesar el mensaje:", error);
    throw error;
  }
};
