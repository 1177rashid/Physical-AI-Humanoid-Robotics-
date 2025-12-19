import React from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import Heading from '@theme/Heading';

import styles from './index.module.css';


const BOOK_COVER_URL = 'https://img.freepik.com/free-photo/technology-concept-with-futuristic-element_23-2151910970.jpg?semt=ais_hybrid&w=740&q=80';

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();

  return (
    <header className={styles.heroBanner}>
      <div className={styles.container}>
        {/* Top small text */}
        <p className={styles.seriesTag}>Physical AI & Humanoid Robotics Book</p>

        <div className={styles.heroContent}>
          {/* Left: Book Cover */}
          <div className={styles.bookCoverWrapper}>
            <img 
              src={BOOK_COVER_URL} 
              alt="AI Native Software Development Book Cover" 
              className={styles.bookCover}
            />
          </div>

          {/* Right: Text & Buttons */}
          <div className={styles.textContent}>
            <Heading as="h1" className={styles.mainTitle}>
              Physical AI & Humanoid Robotics
            </Heading>
            <p className={styles.subtitle}>
              Embodying intelligence in human-like forms to conquer the real world.
            </p>

            {/* Buttons */}
            <div className={styles.buttons}>
              <Link
                className={clsx('button button--primary button--lg', styles.startBtn)}
                to="/docs/intro">
                Start Reading →
              </Link>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
}

export default function Home(): React.ReactNode {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={siteConfig.title}
      description={siteConfig.tagline}>
      <HomepageHeader />
      <main>
        {/* Yahan aap features ya TOC add kar sakte hain */}
      </main>
    </Layout>
  );
}