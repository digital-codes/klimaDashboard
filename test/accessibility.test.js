import { vi, describe, it, expect, beforeEach, afterAll } from 'vitest';
import { render } from '@testing-library/vue';
import { config } from '@vue/test-utils'; // Import test-utils config
import axe from 'axe-core';
import fs from 'fs';
import path from 'path';
import { JSDOM } from 'jsdom';



vi.mock('vue-i18n', () => ({
  useI18n: () => ({
    t: (key) => key // Simple mock of the `t` function
  })
}));

// Add the $t mock globally
config.global.mocks = {
  $t: (msg) => msg, // Mock translation to return the key
  $d: (date) => date, // Optional mock for $d (date formatter)
  locale: { // Mock the locale object globally
    value: 'en' // Default locale value
  }
};

// Mock vue-router and define useRouter and useRoute
vi.mock('vue-router', () => ({
  useRoute: () => ({
    params: { topic: 'mocked-topic' }, // Mock route params
  }),
  useRouter: () => ({
    push: vi.fn(), // Mock router push
    replace: vi.fn(), // Mock router replace
  })
}));



// Path to the components and views directories
const componentsPath = path.resolve(__dirname, '../src/components');
const viewsPath = path.resolve(__dirname, '../src/views');

// Helper function to get all .vue files from a directory
const getVueFiles = (directory) => {
  const files = fs.readdirSync(directory);
  return files
    .filter(file => file.endsWith('.vue'))
    .map(file => path.join(directory, file));
};

// Get all .vue files from components and views directories
const componentFiles = getVueFiles(componentsPath);
const viewFiles = getVueFiles(viewsPath);
const allVueFiles = [...componentFiles, ...viewFiles];

// Store test results in a summary object
const summary = [];




// Process each Vue file
allVueFiles.forEach(filePath => {
  const componentName = path.basename(filePath, '.vue');

  describe(`${componentName} Accessibility Tests`, () => {

    let component;

    beforeEach(async () => {
      const module = await import(filePath);
      component = module.default;
      // Set up the JSDOM environment manually
      const dom = new JSDOM('<!DOCTYPE html><html><body></body></html>', {
        url: 'http://localhost/'
      });
      global.window = dom.window;
      global.document = dom.window.document;
      global.navigator = dom.window.navigator;
    });

    it('should have no axe-core accessibility violations', async () => {
      const { container } = render(component);
      const results = await axe.run(container);
      
      // Log the results to the summary
      summary.push({
        component: componentName,
        violations: results.violations.map(v => ({
          description: v.description,
          helpUrl: v.helpUrl,
          impact: v.impact,
          nodes: v.nodes.map(n => n.html)
        }))
      });

      expect(results.violations).toHaveLength(0);
    });

    it('should have no missing alt text in images', async () => {
      const { container } = render(component);
      const images = container.querySelectorAll('img');
      
      images.forEach(image => {
        const altText = image.getAttribute('alt');
        expect(altText).not.toBeNull();
        expect(altText.trim().length).toBeGreaterThan(0);
      });
    });

    it('should have accessible names for buttons', async () => {
      const { container } = render(component);
      const buttons = container.querySelectorAll('button');
      
      buttons.forEach(button => {
        const accessibleName = button.getAttribute('aria-label') || button.textContent.trim();
        expect(accessibleName).not.toBe('');
      });
    });

    it('should have appropriate ARIA roles for key regions', async () => {
      const { container } = render(component);
      const navigation = container.querySelector('[role="navigation"]');
      const main = container.querySelector('[role="main"]');
      
      expect(navigation).not.toBeNull();
      expect(main).not.toBeNull();
    });
  });
});

// After all tests, write the summary to a JSON file
afterAll(() => {
  const outputPath = path.resolve(__dirname, 'accessibility-summary.json');
  fs.writeFileSync(outputPath, JSON.stringify(summary, null, 2));
  console.log(`Accessibility test summary written to ${outputPath}`);
});
