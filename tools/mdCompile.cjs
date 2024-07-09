const fs = require('fs');
const path = require('path');
const marked = require('marked');
const purify = require("isomorphic-dompurify")

//console.log(marked)

const directory = process.cwd();
const cardFile = path.join(directory, 'card.json');
const contentFile = path.join(directory, 'text.json');
const theContent = {} 

// Read the card.json file
const compile = async () => {

    try {
        const data = await fs.promises.readFile(cardFile, 'utf8');
        const card = await JSON.parse(data);
        const keys = Object.keys(card);
        const languages = keys.filter(key => key !== 'specs');
        console.log(languages)

        const specs = card.specs || {}
        // to insert urls we need data from specs.data and specs.control
        const dataSpecs = specs.data || []
        const controls = specs.controls || {}
        const dataLinks = []
        if (dataSpecs && controls ) {
            for (const i in dataSpecs) {
                const url = dataSpecs[i].url || ""
                const name = dataSpecs[i].name || ""

                if (url != "") {
                    dataLinks.push({ url: url, name: name })
                }

                const ds = ((controls.dataswitch && controls.dataswitch.present) || false)
                if (!ds) {
                    break
                }
            }
        }
        //console.log("DataLinks:",dataLinks)

        // try to read language files
        for (const language of languages) {
            const filePath = path.join(directory, `${language}.md`);
            try {
                let content = await fs.promises.readFile(filePath, 'utf8');
                // append dataLinks to the content
                if (dataLinks.length > 0) {
                    // localized source tag
                    const tag = card[language]["source"] || "Source"
                    content += `\n\n## ${tag}\n\n`
                    const dsindex = dataLinks.length == 2 ? [card[language]["dsleft"] + ": ",card[language]["dsright"] + ": "] : ["",""]
                    const dsnames = card[language]["dsname"] || ["",""]
                    const dataLinksContent = dataLinks.map((link,index) => {
                        return `${dsindex[index]}[${dsnames[index]}](${link.url})`
                    }).join("\n\n")
                    content += dataLinksContent
                }
                const markedContent = await marked.parse(content);
                const purifiedContent = await purify.sanitize(markedContent)
                // set language content into content file
                theContent[language] = purifiedContent;
            } catch (err) {
                console.error(`Error reading file: ${err}`);
                return;
            }
        }
        // Write the content.json file
        await fs.promises.writeFile(contentFile, JSON.stringify(theContent, null, 2));
        console.log(`Successfully updated ${contentFile}`);
    } catch (err) {
        console.error(`Error reading card.json: ${err}`);
    }
}

compile()
