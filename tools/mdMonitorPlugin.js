import { exec } from 'child_process';
import path from 'path';

// Define the directories containing markdown files
const markdownDirs = [
  path.resolve(__dirname, '../src/locales'),
  path.resolve(__dirname, '../src/components/home'),
  path.resolve(__dirname, '../src/components/header'),
  path.resolve(__dirname, '../src/components/header/configs/home'),
  path.resolve(__dirname, '../src/components/header/configs/gdpr'),
  path.resolve(__dirname, '../src/components/header/configs/imprint'),
  path.resolve(__dirname, '../src/components/header/configs/wheather'),
  path.resolve(__dirname, '../src/components/header/configs/protpriv'),
  path.resolve(__dirname, '../src/components/header/configs/protpub'),
  path.resolve(__dirname, '../src/components/header/configs/ghg'),
  path.resolve(__dirname, '../src/components/header/configs/adapt'),
  path.resolve(__dirname, '../src/components/footer'),
  path.resolve(__dirname, '../src/components/sidebar'),
  path.resolve(__dirname, '../src/components/tiles/test/dummyCustom'),
  path.resolve(__dirname, '../src/components/tiles/test/dummyGraphics'),
  path.resolve(__dirname, '../src/components/tiles/test/dummyGauge'),
  path.resolve(__dirname, '../src/components/tiles/test/dummyLine'),
  path.resolve(__dirname, '../src/components/tiles/test/dummyLineCjs'),
  path.resolve(__dirname, '../src/components/tiles/test/dummyLineApx'),
  path.resolve(__dirname, '../src/components/tiles/test/dummyMap'),
  path.resolve(__dirname, '../src/components/tiles/test/dummyTable'),
  path.resolve(__dirname, '../src/components/tiles/protect/actions/KskKa_d_consulting'),
  path.resolve(__dirname, '../src/components/tiles/protect/actions/KskKa_d_electricity'),
  path.resolve(__dirname, '../src/components/tiles/protect/actions/KskKa_d_energy'),
  path.resolve(__dirname, '../src/components/tiles/protect/thg/KskKa_d_ghg'),
  path.resolve(__dirname, '../src/components/tiles/protect/actions/KskKa_d_heat'),
  path.resolve(__dirname, '../src/components/tiles/protect/actions/KskKa_d_mobility'),
  path.resolve(__dirname, '../src/components/tiles/protect/actions/KskKa_d_pv'),
  path.resolve(__dirname, '../src/components/tiles/protect/actions/KskKa_d_stwkenergy'),
  path.resolve(__dirname, '../src/components/tiles/protect/actions/a2_1_fernwaerme'),
  path.resolve(__dirname, '../src/components/tiles/conditions/weather/current'),
  path.resolve(__dirname, '../src/components/tiles/conditions/energyCharts/renewableShare'),
  path.resolve(__dirname, '../src/components/tiles/conditions/statistics/energyQuarters'),

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
