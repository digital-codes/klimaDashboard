const fs = require('fs');
const path = require('path');
const marked = require('marked');
const purify = require("isomorphic-dompurify")

//console.log(marked)
/*
detailsCompile.cjs ../src/assets/details/en ../public/details/en

*/


const args = process.argv.slice(2);
const srcdir = args[0] || process.cwd();
const dstdir = args[1] || process.cwd();

console.log(`Source directory: ${srcdir}`);
console.log(`Destination directory: ${dstdir}`);
if (!fs.existsSync(dstdir)) {
    fs.mkdirSync(dstdir, { recursive: true });
}

const getMarkdownFiles = (dir) => {
    let results = [];
    const list = fs.readdirSync(dir);
    list.forEach((file) => {
        file = path.resolve(dir, file);
        const stat = fs.statSync(file);
        if (stat && stat.isDirectory()) {
            results = results.concat(getMarkdownFiles(file));
        } else if (file.endsWith('.md')) {
            results.push(file);
        }
    });
    return results;
};

// Read the card.json file
const compile = async (filePath) => {
    try {
        console.log(`Reading ${filePath}`);
        let content = await fs.promises.readFile(filePath, 'utf8');
        const markedContent = await marked.parse(content);
        const purifiedContent = await purify.sanitize(markedContent)
        return purifiedContent
    } catch (err) {
        console.error(`Error reading file: ${err}`);
        return null;
    }
}



const markdownFiles = getMarkdownFiles(srcdir);
console.log(`Found ${markdownFiles.length} markdown files`);

for (const file of markdownFiles) {
    console.log(`Processing ${file}`);
    compile(file).then((content) => {
    if (content) {
        try {
        // Write the content.json file
        const targetFile = path.join(dstdir,path.basename(file, '.md')) + ".html";
        console.log(`Writing ${targetFile}`);
        fs.promises.writeFile(targetFile, content, 'utf8');
            } catch (err) {
            console.error(`Error writing ${targetFile}: ${err}`);
        }
    }
})
}


