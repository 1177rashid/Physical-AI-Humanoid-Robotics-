import React, { useState, useEffect } from 'react';
import clsx from 'clsx';
import styles from './CapstoneProject.module.css';
import Link from '@docusaurus/Link';

type CapstoneProjectProps = {
  title: string;
  description: string;
  overview: string;
  requirements: string[];
  voiceIntegrationRequired: boolean;
  simulationComponents: string[];
  evaluationCriteria: string[];
  estimatedDuration: number; // in hours
};

const CapstoneProject: React.FC<CapstoneProjectProps> = ({
  title,
  description,
  overview,
  requirements,
  voiceIntegrationRequired,
  simulationComponents,
  evaluationCriteria,
  estimatedDuration,
}) => {
  const [activeTab, setActiveTab] = useState<'overview' | 'requirements' | 'evaluation'>('overview');
  const [isStarted, setIsStarted] = useState(false);

  const handleStartProject = () => {
    setIsStarted(true);
    // In a real app, this would initialize the project tracking
    console.log('Starting capstone project:', title);
  };

  return (
    <div className={clsx('container', styles.capstoneProject)}>
      <header className={styles.header}>
        <h1>{title}</h1>
        <div className={styles.projectMeta}>
          <span className={styles.duration}>
            🕐 ~{estimatedDuration} hours
          </span>
          {voiceIntegrationRequired && (
            <span className={styles.voiceRequired}>
              🎙️ Voice Integration Required
            </span>
          )}
        </div>
      </header>

      <section className={styles.description}>
        <h2>Project Description</h2>
        <p>{description}</p>
      </section>

      <div className={styles.tabs}>
        <button
          className={clsx(styles.tabButton, { [styles.active]: activeTab === 'overview' })}
          onClick={() => setActiveTab('overview')}
        >
          Overview
        </button>
        <button
          className={clsx(styles.tabButton, { [styles.active]: activeTab === 'requirements' })}
          onClick={() => setActiveTab('requirements')}
        >
          Requirements
        </button>
        <button
          className={clsx(styles.tabButton, { [styles.active]: activeTab === 'evaluation' })}
          onClick={() => setActiveTab('evaluation')}
        >
          Evaluation
        </button>
      </div>

      <div className={styles.tabContent}>
        {activeTab === 'overview' && (
          <div className={styles.overviewSection}>
            <h3>Project Overview</h3>
            <div
              className={styles.overviewContent}
              dangerouslySetInnerHTML={{ __html: overview }}
            />

            {simulationComponents.length > 0 && (
              <div className={styles.simulationSection}>
                <h4>Required Simulation Components</h4>
                <ul>
                  {simulationComponents.map((component, index) => (
                    <li key={index}>{component}</li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        )}

        {activeTab === 'requirements' && (
          <div className={styles.requirementsSection}>
            <h3>Project Requirements</h3>
            <ul>
              {requirements.map((requirement, index) => (
                <li key={index} className={styles.requirementItem}>
                  <input type="checkbox" id={`req-${index}`} className={styles.checkbox} />
                  <label htmlFor={`req-${index}`} className={styles.requirementLabel}>
                    {requirement}
                  </label>
                </li>
              ))}
            </ul>
          </div>
        )}

        {activeTab === 'evaluation' && (
          <div className={styles.evaluationSection}>
            <h3>Evaluation Criteria</h3>
            <ul>
              {evaluationCriteria.map((criteria, index) => (
                <li key={index} className={styles.criteriaItem}>
                  {criteria}
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>

      <div className={styles.projectActions}>
        {!isStarted ? (
          <button
            onClick={handleStartProject}
            className={clsx('button button--primary button--lg', styles.startButton)}
          >
            Start Capstone Project
          </button>
        ) : (
          <div className={styles.projectProgress}>
            <div className={clsx('alert alert--success', styles.progressAlert)}>
              <p>Capstone project started! Track your progress below.</p>
            </div>
            <div className={styles.actionButtons}>
              <Link
                to="/docs/capstone/project-steps"
                className={clsx('button button--secondary button--md', styles.continueButton)}
              >
                Continue to Steps
              </Link>
              <Link
                to="/chat"
                className={clsx('button button--primary button--md', styles.chatButton)}
              >
                Ask Questions (Chatbot)
              </Link>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default CapstoneProject;