// index.js
const { Firestore } = require('@google-cloud/firestore');

const firestore = new Firestore();

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

    // Firestore: Buscar el episodio en la colección 'transcripciones'
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

    // Guardar el resultado en la colección 'UserLanguage'
    const userLanguageRef = firestore.collection('UserLanguage').doc(episode_id);
    await userLanguageRef.set({
      episode_id,
      language,
      processed_at: Firestore.Timestamp.now()
    });

    console.log(`Idioma guardado en la colección 'UserLanguage'`);

    return `Idioma procesado: ${language}`;
  } catch (error) {
    console.error("Error al procesar el mensaje:", error);
    throw error;
  }
};
