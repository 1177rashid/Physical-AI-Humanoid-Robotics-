import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

/**
 * Creating a sidebar enables you to:
 - create an ordered group of docs
 - render a sidebar for each doc of that group
 - provide next/previous navigation

 The sidebars can be generated from the filesystem, or explicitly defined here.

 Create as many sidebars as you want.
 */
const sidebars: SidebarsConfig = {
  // By default, Docusaurus generates a sidebar from the docs folder structure
  textbookSidebar: [
    'intro',
    {
      type: 'category',
      label: 'Foundations',
      items: ['foundations/intro'],
    },
    {
      type: 'category',
      label: 'ROS 2 Nervous System',
      items: ['ros2-nervous-system/intro'],
    },
    {
      type: 'category',
      label: 'Digital Twins',
      items: ['digital-twins/intro'], // Will add content later
    },
    {
      type: 'category',
      label: 'NVIDIA Isaac',
      items: ['nvidia-isaac/intro'], // Will add content later
    },
    {
      type: 'category',
      label: 'Vision-Language-Action',
      items: ['vision-language-action/intro'], // Will add content later
    },
    {
      type: 'category',
      label: 'Humanoid Control',
      items: ['humanoid-control/intro'], // Will add content later
    },
    {
      type: 'category',
      label: 'Capstone Project',
      items: ['capstone/intro'], // Will add content later
    },
  ],

  // But you can create a sidebar manually
  /*
  tutorialSidebar: [
    'intro',
    'hello',
    {
      type: 'category',
      label: 'Tutorial',
      items: ['tutorial-basics/create-a-document'],
    },
  ],
   */
};

export default sidebars;
