const express = require('express');
const fetch = require('node-fetch');
const cheerio = require('cheerio');

const app = express();
const port = process.env.PORT || 3000;

app.get('/', async (req, res) => {
  try {
    const url = 'https://moonani.com/PokeList/quest.php';
    const response = await fetch(url);
    const html = await response.text();

    const $ = cheerio.load(html);
    const table = $('#customers');

    if (!table) {
      return res.json({ error: 'No se encontró la tabla.' });
    }

    const headers = table.find('thead th').map((_, th) => $(th).text()).get();
    
    const data = table.find('tbody tr').map((_, tr) => {
      const rowData = {};
      $(tr).find('td').each((index, td) => {
        const header = headers[index];
        rowData[header] = $(td).text().trim();
      });
      return rowData;
    }).get();

    res.json({ data });
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: 'Error interno del servidor' });
  }
});

app.listen(port, () => {
  console.log(`Servidor en línea en http://localhost:${port}`);
});
