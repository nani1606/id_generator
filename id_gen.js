const PDFDocument = require('pdfkit');
const Jimp = require('jimp');
const fs = require('fs');
const csvParser = require('csv-parser');

async function createIdCards() {
  const doc = new PDFDocument;
  doc.pipe(fs.createWriteStream('output_id_card.pdf'));

  fs.createReadStream('employees.csv')
    .pipe(csvParser())
    .on('data', async (row) => {
      const idCardTemplate = await Jimp.read('id_template.png');
      const photo = await Jimp.read(row.photo_path);
      photo.resize(100, 100);  // Adjust size as needed

      idCardTemplate.composite(photo, 50, 50);  // Adjust coordinates as needed
      const idCardImage = await idCardTemplate.getBufferAsync(Jimp.MIME_PNG);

      doc.image(idCardImage, 0, 0, {width: 595, height: 842});  // A4 size in points
      doc.addPage();
    })
    .on('end', () => {
      doc.end();
    });
}

createIdCards();
