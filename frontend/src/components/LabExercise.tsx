import React, { useState, useEffect } from 'react';
import clsx from 'clsx';
import styles from './LabExercise.module.css';
import CodeBlock from '@theme/CodeBlock';

type LabExerciseProps = {
  title: string;
  description: string;
  difficulty: 'beginner' | 'intermediate' | 'advanced';
  instructions: string;
  codeSamples?: Array<{
    language: string;
    code: string;
  }>;
  expectedOutcomes?: string[];
  prerequisites?: string[];
  estimatedDuration?: number; // in minutes
  simulationRequired?: boolean;
};

const LabDifficultyBadge = ({ difficulty }: { difficulty: string }) => {
  const getDifficultyStyle = (diff: string) => {
    switch (diff.toLowerCase()) {
      case 'beginner':
        return styles.difficultyBeginner;
      case 'intermediate':
        return styles.difficultyIntermediate;
      case 'advanced':
        return styles.difficultyAdvanced;
      default:
        return styles.difficultyBeginner;
    }
  };

  return (
    <span className={clsx(styles.difficultyBadge, getDifficultyStyle(difficulty))}>
      {difficulty.charAt(0).toUpperCase() + difficulty.slice(1)}
    </span>
  );
};

const LabExercise: React.FC<LabExerciseProps> = ({
  title,
  description,
  difficulty,
  instructions,
  codeSamples = [],
  expectedOutcomes = [],
  prerequisites = [],
  estimatedDuration,
  simulationRequired = false,
}) => {
  const [isSubmitted, setIsSubmitted] = useState(false);
  const [solutionCode, setSolutionCode] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // In a real app, this would submit to the backend
    console.log('Submitting solution:', solutionCode);
    setIsSubmitted(true);
    setTimeout(() => setIsSubmitted(false), 3000); // Reset after 3 seconds
  };

  return (
    <div className={clsx('container', styles.labExercise)}>
      <header className={styles.header}>
        <h1>{title}</h1>
        <div className={styles.metaInfo}>
          <LabDifficultyBadge difficulty={difficulty} />
          {estimatedDuration && (
            <span className={styles.duration}>
              ⏱️ {estimatedDuration} minutes
            </span>
          )}
          {simulationRequired && (
            <span className={styles.simulationRequired}>
              🤖 Simulation Required
            </span>
          )}
        </div>
      </header>

      <section className={styles.description}>
        <h2>Description</h2>
        <p>{description}</p>
      </section>

      {prerequisites.length > 0 && (
        <section className={styles.prerequisites}>
          <h2>Prerequisites</h2>
          <ul>
            {prerequisites.map((req, index) => (
              <li key={index}>{req}</li>
            ))}
          </ul>
        </section>
      )}

      <section className={styles.instructions}>
        <h2>Instructions</h2>
        <div
          className={styles.instructionContent}
          dangerouslySetInnerHTML={{ __html: instructions }}
        />
      </section>

      {codeSamples.length > 0 && (
        <section className={styles.codeSamples}>
          <h2>Code Samples</h2>
          {codeSamples.map((sample, index) => (
            <CodeBlock key={index} language={sample.language}>
              {sample.code}
            </CodeBlock>
          ))}
        </section>
      )}

      {expectedOutcomes.length > 0 && (
        <section className={styles.expectedOutcomes}>
          <h2>Expected Outcomes</h2>
          <ul>
            {expectedOutcomes.map((outcome, index) => (
              <li key={index}>{outcome}</li>
            ))}
          </ul>
        </section>
      )}

      <section className={styles.solutionSubmission}>
        <h2>Your Solution</h2>
        <form onSubmit={handleSubmit} className={styles.solutionForm}>
          <textarea
            value={solutionCode}
            onChange={(e) => setSolutionCode(e.target.value)}
            placeholder="Write your solution code here..."
            rows={15}
            className={styles.solutionTextarea}
          />
          <button
            type="submit"
            className={clsx('button button--primary', styles.submitButton)}
            disabled={!solutionCode.trim()}
          >
            Submit Solution
          </button>
        </form>

        {isSubmitted && (
          <div className={clsx('alert alert--success', styles.successAlert)}>
            Solution submitted successfully! Our system will evaluate your code.
          </div>
        )}
      </section>
    </div>
  );
};

export default LabExercise;