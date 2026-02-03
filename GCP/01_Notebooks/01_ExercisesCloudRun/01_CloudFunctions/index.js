// index.js

// Export a Cloud Function named 'randomJoke'
exports.randomJoke = (req, res) => {
  // Array of jokes
  const jokes = [
    "¿Por qué el computador fue al doctor? ¡Porque tenía un virus!",
    "¿Por qué los servidores nunca se pelean? Porque mantienen la calma en la nube.",
    "¿Qué le dice un algoritmo a otro? Nos vemos en el loop."
  ];

  // Generate a random index to select a joke
  const randomIndex = Math.floor(Math.random() * jokes.length);
  const joke = jokes[randomIndex];

  // Return the selected joke as JSON with HTTP status 200
  res.status(200).json({ joke });
};
