
const htmlContent = () => {
    return `
<h2>MD Text EN</h2>
<p>bla bla bla</p>
<p><a href="https://www.google.com">link</a></p>
<ul>
<li>123</li>
<li>456<ul>
<li>789</li>
</ul>
</li>
</ul>
<p><img alt="image" src="/images/testing.jpg">  </p>
<p>bla bla bla</p>
<h2>Source</h2>
<p><a href="https://transparenz.karlsruhe.de/dataset/7306d25b-8b18-445f-9351-6eec030c7753/resource/fd9de911-5142-4083-9d1b-5e09788022b3/download/treibhausgase.csv">Treibhausgasbilanz Karlsruhe</a></p>
<p><a href="https://transparenz.karlsruhe.de/dataset/ad0659b0-9e4b-408a-8840-3f19d5ec743d/resource/df843a83-b3f6-4929-b6a8-96471508f6f2/download/sensordaten_karlsruhe_bodentemperatur_bodenfeuchte_oct_2023.csv">Sensoren  Friedrichsplatz 10/23</a></p>

    `
}
export default htmlContent;
