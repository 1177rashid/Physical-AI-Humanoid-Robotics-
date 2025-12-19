import React, { useState, useEffect } from 'react';
import Layout from '@theme/Layout';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import LabExercise from '../components/LabExercise';

const LabsPage: React.FC = () => {
  const { siteConfig } = useDocusaurusContext();
  const [selectedLab, setSelectedLab] = useState<any>(null);
  const [labs, setLabs] = useState<any[]>([]);

  // Mock data for demonstration
  const mockLabs = [
    {
      id: '1',
      title: 'ROS 2 Publisher/Subscriber Lab',
      description: 'Create a simple publisher and subscriber in ROS 2 to understand basic communication patterns.',
      difficulty: 'intermediate',
      instructions: `
        <h3>Lab Objectives</h3>
        <ol>
          <li>Create a publisher node that publishes messages to a topic</li>
          <li>Create a subscriber node that listens to the same topic</li>
          <li>Test the communication between nodes</li>
        </ol>

        <h3>Steps</h3>
        <ol>
          <li>Create a new ROS 2 package for this lab</li>
          <li>Implement the publisher node in Python</li>
          <li>Implement the subscriber node in Python</li>
          <li>Test the communication using ROS 2 tools</li>
        </ol>
      `,
      codeSamples: [
        {
          language: 'python',
          code: `#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class MinimalPublisher(Node):
    def __init__(self):
        super().__init__('minimal_publisher')
        self.publisher_ = self.create_publisher(String, 'topic', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        msg = String()
        msg.data = 'Hello World: %d' % self.i
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: "%s"' % msg.data)
        self.i += 1

def main(args=None):
    rclpy.init(args=args)
    minimal_publisher = MinimalPublisher()
    rclpy.spin(minimal_publisher)
    minimal_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()`
        }
      ],
      expectedOutcomes: [
        'Successfully publish messages to a ROS 2 topic',
        'Successfully subscribe to messages from a ROS 2 topic',
        'Understand the pub/sub communication pattern in ROS 2'
      ],
      prerequisites: [
        'Basic understanding of ROS 2 concepts',
        'ROS 2 environment setup',
        'Python programming basics'
      ],
      estimatedDuration: 90,
      simulationRequired: false
    },
    {
      id: '2',
      title: 'Gazebo Simulation Integration Lab',
      description: 'Integrate a robot model with Gazebo simulator to test navigation algorithms.',
      difficulty: 'advanced',
      instructions: `
        <h3>Lab Objectives</h3>
        <ol>
          <li>Load a robot model in Gazebo</li>
          <li>Implement navigation algorithms</li>
          <li>Test the robot in simulated environment</li>
        </ol>
      `,
      codeSamples: [],
      expectedOutcomes: [
        'Robot model loaded successfully in Gazebo',
        'Navigation algorithms working in simulation',
        'Understanding of simulation environments'
      ],
      prerequisites: [
        'Gazebo installed',
        'Robot model ready',
        'Basic navigation knowledge'
      ],
      estimatedDuration: 120,
      simulationRequired: true
    }
  ];

  useEffect(() => {
    // In a real app, this would fetch from the backend API
    setLabs(mockLabs);
  }, []);

  return (
    <Layout
      title={`Labs - ${siteConfig.title}`}
      description="Interactive lab exercises for the AI-Native Textbook">
      <main className="container margin-vert--lg">
        <div className="row">
          <div className="col col--4">
            <h2>Available Labs</h2>
            <ul className="list-group">
              {labs.map((lab) => (
                <li key={lab.id} className="list-group-item margin-bottom--sm">
                  <button
                    onClick={() => setSelectedLab(lab)}
                    className={`button button--${selectedLab?.id === lab.id ? 'primary' : 'outline'} button--block`}
                  >
                    {lab.title}
                    <br />
                    <small>({lab.difficulty})</small>
                  </button>
                </li>
              ))}
            </ul>

            {!selectedLab && (
              <div className="alert alert--info margin-top--md">
                <p>Select a lab exercise from the list to get started.</p>
              </div>
            )}
          </div>

          <div className="col col--8">
            {selectedLab ? (
              <LabExercise
                title={selectedLab.title}
                description={selectedLab.description}
                difficulty={selectedLab.difficulty}
                instructions={selectedLab.instructions}
                codeSamples={selectedLab.codeSamples}
                expectedOutcomes={selectedLab.expectedOutcomes}
                prerequisites={selectedLab.prerequisites}
                estimatedDuration={selectedLab.estimatedDuration}
                simulationRequired={selectedLab.simulationRequired}
              />
            ) : (
              <div className="text--center padding-vert--xl">
                <h2>Welcome to Lab Exercises</h2>
                <p>Choose a lab from the sidebar to begin your hands-on learning experience.</p>
                <p>Labs are designed to reinforce the concepts learned in the textbook modules through practical implementation.</p>
              </div>
            )}
          </div>
        </div>
      </main>
    </Layout>
  );
};

export default LabsPage;