import React from 'react';
import clsx from 'clsx';
import styles from './TextbookModule.module.css';

type TextbookModuleProps = {
  title: string;
  content: string;
  category?: string;
  estimatedDuration?: number;
};

const TextbookModule: React.FC<TextbookModuleProps> = ({
  title,
  content,
  category,
  estimatedDuration
}) => {
  return (
    <div className={clsx('container', styles.textbookModule)}>
      <header className={styles.header}>
        <h1>{title}</h1>
        {category && (
          <span className={styles.category}>Category: {category}</span>
        )}
        {estimatedDuration && (
          <span className={styles.duration}>
            Estimated time: {estimatedDuration} minutes
          </span>
        )}
      </header>
      <div className={styles.content}>
        <div dangerouslySetInnerHTML={{ __html: content }} />
      </div>
    </div>
  );
};

export default TextbookModule;