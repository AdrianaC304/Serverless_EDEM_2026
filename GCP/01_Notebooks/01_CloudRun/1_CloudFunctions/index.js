// index.js
exports.randomJoke = (req, res) => {
  const jokes = [
    "¿Por qué el computador fue al doctor? ¡Porque tenía un virus!",
    "¿Por qué los servidores nunca se pelean? Porque mantienen la calma en la nube.",
    "¿Qué le dice un algoritmo a otro? Nos vemos en el loop."
  ];

  const randomIndex = Math.floor(Math.random() * jokes.length);
  const joke = jokes[randomIndex];

  res.status(200).json({ joke });
};
