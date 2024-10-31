const fs = require('fs');
const https = require('https');
const path = require('path');

const version = require('pdfjs-dist/package.json').version;
const workerPath = path.join(__dirname, '../public/pdf.worker.min.js');

// Ensure the worker version matches your pdfjs-dist version
const workerUrl = `https://unpkg.com/pdfjs-dist@${version}/build/pdf.worker.min.js`;

https.get(workerUrl, (response) => {
  const file = fs.createWriteStream(workerPath);
  response.pipe(file);
  
  file.on('finish', () => {
    file.close();
    console.log('PDF.js worker downloaded successfully');
  });
}).on('error', (err) => {
  console.error('Error downloading PDF.js worker:', err);
  process.exit(1);
});