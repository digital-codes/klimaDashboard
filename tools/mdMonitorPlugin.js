import { exec } from 'child_process';
import path from 'path';

// Define the directories containing markdown files
const markdownDirs = [
  path.resolve(__dirname, '../src/components/home'),
  path.resolve(__dirname, '../src/components/header'),
  path.resolve(__dirname, '../src/components/footer'),
  path.resolve(__dirname, '../src/components/sidebar'),
  path.resolve(__dirname, '../src/components/tiles/dummyCustom'),
  path.resolve(__dirname, '../src/components/tiles/dummyGraphics'),
  path.resolve(__dirname, '../src/components/tiles/dummyLine'),
  path.resolve(__dirname, '../src/components/tiles/dummyLineCjs'),
  path.resolve(__dirname, '../src/components/tiles/dummyLineApx'),
  path.resolve(__dirname, '../src/components/tiles/dummyMap'),
  path.resolve(__dirname, '../src/components/tiles/dummyTable'),
  path.resolve(__dirname, '../src/components/tiles/KskKa_d_consulting'),
  path.resolve(__dirname, '../src/components/tiles/KskKa_d_electricity'),
  path.resolve(__dirname, '../src/components/tiles/KskKa_d_energy'),
  path.resolve(__dirname, '../src/components/tiles/KskKa_d_ghg'),
  path.resolve(__dirname, '../src/components/tiles/KskKa_d_heat'),
  path.resolve(__dirname, '../src/components/tiles/KskKa_d_mobility'),
  path.resolve(__dirname, '../src/components/tiles/KskKa_d_pv'),
];

// Define the bash script to execute
const bashScript = path.resolve(__dirname, './mdCompileAll.sh');

const customMarkdownPlugin = () => ({
  name: 'custom-markdown-plugin',
  handleHotUpdate({ file, server }) {
    if ((file.endsWith("card.json") || file.endsWith("lang.json")) && markdownDirs.some(dir => file.startsWith(dir))) {
      // Reload the server
      server.ws.send({
        type: 'full-reload',
      });
    } else {
      if (file.endsWith('.md') && markdownDirs.some(dir => file.startsWith(dir))) {
        // Execute the bash script
        //exec(`${bashScript} ${dir} ${file}`, (error, stdout, stderr) => {
        exec(`${bashScript} ${file}`, (error, stdout, stderr) => {
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
    }
  }
});

export default customMarkdownPlugin;
