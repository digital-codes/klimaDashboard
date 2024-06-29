import { exec } from 'child_process';
import path from 'path';

// Define the directories containing markdown files
const markdownDirs = [
  path.resolve(__dirname, '../src/components/home'),
  path.resolve(__dirname, '../src/components/header'),
  path.resolve(__dirname, '../src/components/footer'),
  path.resolve(__dirname, '../src/components/tiles/dummyCustom'),
  path.resolve(__dirname, '../src/components/tiles/dummyGraphics'),
  path.resolve(__dirname, '../src/components/tiles/dummyLine'),
  path.resolve(__dirname, '../src/components/tiles/dummyMap'),
  path.resolve(__dirname, '../src/components/tiles/dummyTable'),
];

// Define the bash script to execute
const bashScript = path.resolve(__dirname, './mdCompileAll.sh');

const customMarkdownPlugin = () => ({
  name: 'custom-markdown-plugin',
  handleHotUpdate({ file, server }) {
    if (file.endsWith('.md') && markdownDirs.some(dir => file.startsWith(dir))) {
      // Execute the bash script
      exec(bashScript, (error, stdout, stderr) => {
        if (error) {
          console.error(`Error executing script: ${error}`);
          return;
        }
        if (stderr) {
          console.error(`Script stderr: ${stderr}`);
          return;
        }
        console.log(`Script stdout: ${stdout}`);
      });

      // Reload the server
      server.ws.send({
        type: 'full-reload',
      });
    }
  },
});

export default customMarkdownPlugin;
