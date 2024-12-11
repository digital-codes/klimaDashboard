import { config } from '@vue/test-utils';
import { createPinia } from 'pinia';
import { i18n } from './i18n';

config.global.plugins = [i18n]; // Register i18n globally for all tests

const pinia = createPinia();
config.global.plugins = [pinia]; // Add Pinia to global plugins

