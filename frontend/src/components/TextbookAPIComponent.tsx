import React, { useState, useEffect } from 'react';
import { useLocation } from '@docusaurus/router';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Loading from './Loading';

interface TextbookModule {
  id: string;
  title: string;
  slug: string;
  content: string;
  category: string;
  prerequisites: string[];
  learning_objectives: string[];
  estimated_duration: number | null;
  is_published: boolean;
  created_at: string;
  updated_at: string;
}

interface TextbookModuleResponse {
  data: TextbookModule[];
  total: number;
  skip: number;
  limit: number;
}

const TextbookAPIComponent: React.FC = () => {
  const [modules, setModules] = useState<TextbookModule[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const location = useLocation();
  const { siteConfig } = useDocusaurusContext();

  // Get API base URL from site config or default to development server
  const apiBaseUrl = siteConfig.customFields?.apiBaseUrl || 'http://localhost:8000/v1';

  useEffect(() => {
    const fetchTextbookModules = async () => {
      try {
        setLoading(true);
        const response = await fetch(`${apiBaseUrl}/textbook/modules`);

        if (!response.ok) {
          throw new Error(`API request failed with status ${response.status}`);
        }

        const data: TextbookModuleResponse = await response.json();
        setModules(data.data);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Unknown error occurred');
      } finally {
        setLoading(false);
      }
    };

    fetchTextbookModules();
  }, [apiBaseUrl]);

  if (loading) {
    return <Loading />;
  }

  if (error) {
    return (
      <div className="alert alert--danger">
        <h3>Error loading textbook modules</h3>
        <p>{error}</p>
        <p>Make sure the backend server is running at {apiBaseUrl}</p>
      </div>
    );
  }

  return (
    <div className="container margin-vert--lg">
      <h1>Textbook Modules</h1>
      <p>Below are the available textbook modules from the backend API:</p>

      {modules.length === 0 ? (
        <p>No textbook modules available.</p>
      ) : (
        <div className="row">
          {modules.map((module) => (
            <div key={module.id} className="col col--12 margin-vert--md">
              <div className="card">
                <div className="card__header">
                  <h3>{module.title}</h3>
                  <small>Category: {module.category}</small>
                </div>
                <div className="card__body">
                  <p dangerouslySetInnerHTML={{ __html: module.content.substring(0, 200) + '...' }} />
                  <ul>
                    {module.learning_objectives.slice(0, 3).map((objective, idx) => (
                      <li key={idx}>{objective}</li>
                    ))}
                  </ul>
                  {module.estimated_duration && (
                    <p><strong>Estimated Duration:</strong> {module.estimated_duration} minutes</p>
                  )}
                </div>
                <div className="card__footer">
                  <button className="button button--secondary button--sm">
                    View Full Module
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default TextbookAPIComponent;