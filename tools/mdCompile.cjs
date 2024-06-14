const fs = require('fs');
const path = require('path');
const marked = require('marked');
const purify = require("isomorphic-dompurify")

//console.log(marked)

const directory = process.cwd();
const cardFile = path.join(directory, 'card.json');


// Read the card.json file
const compile = async () => {

    try {
        const data = await fs.promises.readFile(cardFile, 'utf8');
        const card = await JSON.parse(data);
        const keys = Object.keys(card);
        const languages = keys.filter(key => key !== 'specs');
        console.log(languages)

        // try to read language files
        for (const language of languages) {
            const filePath = path.join(directory, `${language}.md`);
            try {
                const content = await fs.promises.readFile(filePath, 'utf8');
                const markedContent = await marked.parse(content);
                const purifiedContent = await purify.sanitize(markedContent)
                // Insert the marked content into the card.json file
                card[language]["mdpane"] = purifiedContent;
            } catch (err) {
                console.error(`Error reading file: ${err}`);
                return;
            }
        }
        // Write the updated card.json file
        await fs.promises.writeFile(cardFile, JSON.stringify(card, null, 2));
        console.log(`Successfully updated ${cardFile}`);
    } catch (err) {
        console.error(`Error reading card.json: ${err}`);
    }
}

compile()
