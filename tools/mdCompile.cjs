const fs = require('fs');
const path = require('path');
const marked = require('marked');

//console.log(marked)

const directory = process.cwd();
const cardFile = path.join(directory, 'card.json');

// Read the card.json file
fs.readFile(cardFile, 'utf8', async (err, data) => {
    if (err) {
        console.error(`Error reading card.json: ${err}`);
        return;
    }

    const card = JSON.parse(data);
    const languages = Object.keys(card);
    console.log(languages);

    // try to read language files
    for (const language of languages) {
    //languages.forEach(language => {
        const filePath = path.join(directory, `${language}.md`);
        fs.readFile(filePath, 'utf8', async (err, content) => {
            if (err) {
                console.error(`Error reading file: ${err}`);
                return;
            }

            // Run marked on the file content
            const markedContent = await marked.parse(content);
            console.log(markedContent)

            // Insert the marked content into the card.json file
            card[language]["mdpane"] = markedContent;

        })
    }

    console.log(JSON.stringify(card, null, 2))

    // Write the updated card.json file
    fs.writeFile(cardFile, JSON.stringify(card, null, 2), err => {
        if (err) {
            console.error(`Error writing card.json: ${err}`);
            return;
        }

        console.log(`Successfully updated card.json`);
    });

});