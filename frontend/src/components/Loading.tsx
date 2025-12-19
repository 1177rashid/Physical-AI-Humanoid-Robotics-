import React from 'react';

const Loading: React.FC = () => {
  return (
    <div className="container margin-vert--lg">
      <div className="row">
        <div className="col col--12 text--center">
          <div className="margin-vert--lg">
            <div className="loading-spinner">
              <div className="spinner-border" role="status">
                <span className="sr-only">Loading...</span>
              </div>
            </div>
            <p>Loading textbook content...</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Loading;