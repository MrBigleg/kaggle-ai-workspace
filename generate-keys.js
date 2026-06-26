const crypto = require('crypto');
const fs = require('fs');
const path = require('path');

const websiteBDir = 'c:\\Users\\craig\\01_Projects\\001_Kaggle\\Concierge-Agent-website-B';
const websiteADir = 'c:\\Users\\craig\\01_Projects\\001_Kaggle\\Titan-Inventory-Agent-Website-A';

const { privateKey, publicKey } = crypto.generateKeyPairSync('rsa', {
  modulusLength: 2048,
  publicKeyEncoding: {
    type: 'spki',
    format: 'pem'
  },
  privateKeyEncoding: {
    type: 'pkcs8',
    format: 'pem'
  }
});

fs.writeFileSync(path.join(websiteBDir, 'private_key.pem'), privateKey);
fs.writeFileSync(path.join(websiteBDir, 'public_key.pem'), publicKey);
fs.writeFileSync(path.join(websiteADir, 'public_key.pem'), publicKey);

console.log('Keys generated and written successfully.');
