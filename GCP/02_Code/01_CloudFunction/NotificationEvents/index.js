// index.js
const { Firestore } = require('@google-cloud/firestore');

const firestore = new Firestore();

/**
 * 2nd Gen Cloud Function triggered by Pub/Sub
 */
exports.getEpisodeLanguage = async (message, context) => {
  try {
    // Decode the Pub/Sub message
    const msgStr = Buffer.from(message.data, 'base64').toString();
    const data = JSON.parse(msgStr);

    // Extract required fields from the message
    const user_id = data.user_id;
    const type = data.type;
    const episode_id = data.payload?.episode_id;

    if (!user_id || !episode_id || !type) {
      console.error("Missing required fields: user_id, episode_id or type");
      return;
    }

    console.log(
      `Processing notification ${type} for user ${user_id} and episode ${episode_id}`
    );

    // Read the user's language from the 'users' collection
    const userDoc = await firestore.collection('users').doc(user_id).get();

    if (!userDoc.exists) {
      console.log(`User ${user_id} not found in Firestore`);
      return;
    }

    const userData = userDoc.data();
    const language = userData.language;

    console.log(`User ${user_id} language: ${language}`);

    // Store the result in the 'notifications' collection
    await firestore.collection('notifications').add({
      user_id,
      episode_id,
      language,
      type
    });

    console.log(`Notification successfully stored in notifications`);

    return `Notification processed successfully`;

  } catch (error) {
    console.error("Error while processing the message:", error);
    throw error;
  }
};
