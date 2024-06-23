module.exports = {
    apps: [
      {
        name: 'astro',
        script: 'npx',
        args: 'astro dev',
        interpreter: 'none',
      },
      {
        name: 'flask',
        script: 'server.py',
        interpreter: 'python',
      },
    ],
  };
  