import React, { useState, useEffect } from 'react';
import Layout from '@theme/Layout';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import CapstoneProject from '../components/CapstoneProject';
import ChatbotWidget from '../components/ChatbotWidget';

const CapstonePage: React.FC = () => {
  const { siteConfig } = useDocusaurusContext();
  const [currentStep, setCurrentStep] = useState(0);
  const [projectStatus, setProjectStatus] = useState<'not-started' | 'in-progress' | 'completed'>('not-started');

  // Mock capstone project data
  const capstoneProject = {
    title: "Voice-Controlled Humanoid Robot Capstone",
    description: "Develop a humanoid robot that responds to voice commands and performs complex tasks using ROS 2, Gazebo, and NVIDIA Isaac.",
    overview: `<h3>Capstone Project Overview</h3>
<p>This project integrates all concepts learned in the textbook to create an autonomous humanoid robot capable of understanding and executing voice commands.</p>

<h4>Key Objectives:</h4>
<ul>
  <li>Implement voice recognition system</li>
  <li>Create motion planning algorithms</li>
  <li>Integrate perception and control systems</li>
  <li>Deploy on simulated humanoid platform</li>
</ul>

<h4>Technologies Used:</h4>
<ul>
  <li>ROS 2 for robot communication</li>
  <li>Gazebo for simulation</li>
  <li>NVIDIA Isaac for perception</li>
  <li>Vision-Language-Action models</li>
</ul>`,
    requirements: [
      "Implement voice recognition system that can understand simple commands",
      "Create motion planning algorithms for navigation",
      "Integrate perception system to recognize objects",
      "Implement control system for robot actuators",
      "Design a state machine for robot behavior",
      "Test in Gazebo simulation environment",
      "Document the entire development process"
    ],
    voiceIntegrationRequired: true,
    simulationComponents: [
      "Gazebo simulation environment",
      "ROS 2 communication framework",
      "NVIDIA Isaac perception stack"
    ],
    evaluationCriteria: [
      "Robot responds correctly to voice commands (>90% accuracy)",
      "Navigation accuracy > 90% in simulation",
      "Task completion rate > 85%",
      "Code quality and documentation standards met",
      "Proper error handling and safety measures implemented"
    ],
    estimatedDuration: 120 // hours
  };

  const projectSteps = [
    {
      title: "Project Planning",
      description: "Define requirements, architecture, and timeline for your humanoid robot project",
      resources: [
        { title: "System Architecture Guide", link: "/docs/capstone/system-architecture" },
        { title: "Requirements Template", link: "/docs/capstone/requirements-template" }
      ]
    },
    {
      title: "Voice Recognition Setup",
      description: "Implement speech-to-text functionality and command interpretation",
      resources: [
        { title: "Voice Recognition Tutorial", link: "/docs/capstone/voice-recognition" },
        { title: "NLP for Commands", link: "/docs/capstone/nlp-commands" }
      ]
    },
    {
      title: "Simulation Environment",
      description: "Set up Gazebo with your humanoid robot model",
      resources: [
        { title: "Gazebo Setup Guide", link: "/docs/capstone/gazebo-setup" },
        { title: "Robot URDF Modeling", link: "/docs/capstone/robot-modeling" }
      ]
    },
    {
      title: "Perception System",
      description: "Implement computer vision and sensor processing",
      resources: [
        { title: "Computer Vision Pipeline", link: "/docs/capstone/perception-pipeline" },
        { title: "Sensor Fusion Techniques", link: "/docs/capstone/sensor-fusion" }
      ]
    },
    {
      title: "Motion Planning",
      description: "Create path planning and locomotion algorithms",
      resources: [
        { title: "Path Planning Algorithms", link: "/docs/capstone/path-planning" },
        { title: "Locomotion Control", link: "/docs/capstone/locomotion" }
      ]
    },
    {
      title: "Integration & Testing",
      description: "Combine all components and test in simulation",
      resources: [
        { title: "Integration Testing", link: "/docs/capstone/integration-testing" },
        { title: "Debugging Strategies", link: "/docs/capstone/debugging" }
      ]
    },
    {
      title: "Documentation & Presentation",
      description: "Document your solution and prepare for evaluation",
      resources: [
        { title: "Project Documentation", link: "/docs/capstone/documentation" },
        { title: "Presentation Template", link: "/docs/capstone/presentation" }
      ]
    }
  ];

  const handleNextStep = () => {
    if (currentStep < projectSteps.length - 1) {
      setCurrentStep(currentStep + 1);
    } else {
      setProjectStatus('completed');
    }
  };

  const handlePrevStep = () => {
    if (currentStep > 0) {
      setCurrentStep(currentStep - 1);
    }
  };

  const handleRestart = () => {
    setCurrentStep(0);
    setProjectStatus('not-started');
  };

  return (
    <Layout
      title={`Capstone Project - ${siteConfig.title}`}
      description="Voice-controlled humanoid robot capstone project">
      <div className="container margin-vert--lg">
        <div className="row">
          <div className="col col--8">
            <CapstoneProject
              title={capstoneProject.title}
              description={capstoneProject.description}
              overview={capstoneProject.overview}
              requirements={capstoneProject.requirements}
              voiceIntegrationRequired={capstoneProject.voiceIntegrationRequired}
              simulationComponents={capstoneProject.simulationComponents}
              evaluationCriteria={capstoneProject.evaluationCriteria}
              estimatedDuration={capstoneProject.estimatedDuration}
            />

            <div className="margin-top--lg">
              <h2>Project Guidance Workflow</h2>

              {projectStatus === 'not-started' && (
                <div className="alert alert--info">
                  <p>Click "Start Project" in the capstone project section above to begin the guided workflow.</p>
                </div>
              )}

              {projectStatus !== 'not-started' && (
                <div className="card">
                  <div className="card__header">
                    <h3>Step {currentStep + 1}: {projectSteps[currentStep].title}</h3>
                  </div>
                  <div className="card__body">
                    <p>{projectSteps[currentStep].description}</p>

                    <h4>Recommended Resources:</h4>
                    <ul>
                      {projectSteps[currentStep].resources.map((resource, idx) => (
                        <li key={idx}>
                          <Link to={resource.link}>{resource.title}</Link>
                        </li>
                      ))}
                    </ul>
                  </div>
                  <div className="card__footer">
                    <div className="button-group button-group--block">
                      <button
                        className="button button--secondary"
                        onClick={handlePrevStep}
                        disabled={currentStep === 0}
                      >
                        Previous
                      </button>
                      {currentStep < projectSteps.length - 1 ? (
                        <button
                          className="button button--primary"
                          onClick={handleNextStep}
                        >
                          Next Step
                        </button>
                      ) : (
                        <button
                          className="button button--success"
                          onClick={() => setProjectStatus('completed')}
                        >
                          Complete Project
                        </button>
                      )}
                    </div>
                  </div>
                </div>
              )}

              {projectStatus === 'completed' && (
                <div className="margin-top--lg">
                  <div className="alert alert--success">
                    <h3>Congratulations! 🎉</h3>
                    <p>You have successfully completed the Voice-Controlled Humanoid Robot Capstone Project!</p>
                    <p>Your robot can now understand voice commands and perform complex tasks.</p>
                  </div>
                  <div className="text--center margin-top--md">
                    <button
                      className="button button--primary"
                      onClick={handleRestart}
                    >
                      Start New Project
                    </button>
                  </div>
                </div>
              )}
            </div>
          </div>

          <div className="col col--4">
            <div className="margin-bottom--lg">
              <h3>Project Progress</h3>
              <div className="progress-container">
                <div className="progress-bar">
                  <div
                    className="progress-bar-fill"
                    style={{ width: `${((currentStep + 1) / projectSteps.length) * 100}%` }}
                  ></div>
                </div>
                <div className="text--center margin-top--sm">
                  Step {currentStep + 1} of {projectSteps.length}
                </div>
              </div>
            </div>

            <div className="margin-bottom--lg">
              <h3>Quick Resources</h3>
              <ul className="clean-list">
                <li><Link to="/docs/ros2-nervous-system/intro">ROS 2 Guide</Link></li>
                <li><Link to="/docs/nvidia-isaac/intro">Isaac SDK</Link></li>
                <li><Link to="/docs/vision-language-action/intro">VLA Models</Link></li>
                <li><Link to="/docs/digital-twins/intro">Simulation Guide</Link></li>
              </ul>
            </div>

            <div className="margin-bottom--lg">
              <h3>Need Help?</h3>
              <p>Ask questions about your capstone project using our AI assistant:</p>
            </div>
          </div>
        </div>
      </div>

      <ChatbotWidget initialContext="capstone-project" />
    </Layout>
  );
};

export default CapstonePage;