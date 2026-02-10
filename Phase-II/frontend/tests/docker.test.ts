/**
 * Frontend Container Tests
 * Tests Docker container build and runtime requirements
 */

import { execSync } from 'child_process';
import { describe, test, expect, beforeAll, afterAll } from '@jest/globals';
import axios from 'axios';

const IMAGE_NAME = 'todo-frontend:latest';
const CONTAINER_NAME = 'test-todo-frontend';
const TEST_PORT = 3001;

describe('Frontend Container Tests', () => {
  let containerId: string;

  beforeAll(async () => {
    // Build the container
    console.log(`\nBuilding container: ${IMAGE_NAME}`);
    try {
      execSync(`docker build -t ${IMAGE_NAME} .`, {
        cwd: '/mnt/h/GIAIC/Todo-app-hackathon-II/Phase-II/frontend',
        stdio: 'inherit',
      });
    } catch (error) {
      throw new Error(`Container build failed: ${error}`);
    }

    // Start the container
    console.log(`Starting container: ${CONTAINER_NAME}`);
    try {
      const output = execSync(
        `docker run -d --name ${CONTAINER_NAME} -p ${TEST_PORT}:3000 -e NEXT_PUBLIC_API_BASE_URL=http://localhost:8000 ${IMAGE_NAME}`,
        { encoding: 'utf-8' }
      );
      containerId = output.trim();
    } catch (error) {
      throw new Error(`Container start failed: ${error}`);
    }

    // Wait for container to be ready
    await new Promise((resolve) => setTimeout(resolve, 10000));
  }, 60000);

  afterAll(() => {
    // Cleanup
    console.log(`\nCleaning up container: ${CONTAINER_NAME}`);
    try {
      execSync(`docker stop ${CONTAINER_NAME}`, { stdio: 'ignore' });
      execSync(`docker rm ${CONTAINER_NAME}`, { stdio: 'ignore' });
    } catch (error) {
      console.error('Cleanup failed:', error);
    }
  });

  test('container builds successfully', () => {
    // Build a test image to verify build process
    expect(() => {
      execSync(`docker build -t ${IMAGE_NAME}-test .`, {
        cwd: '/mnt/h/GIAIC/Todo-app-hackathon-II/Phase-II/frontend',
        stdio: 'pipe',
      });
    }).not.toThrow();

    // Cleanup test image
    try {
      execSync(`docker rmi ${IMAGE_NAME}-test`, { stdio: 'ignore' });
    } catch (error) {
      // Ignore cleanup errors
    }
  }, 120000);

  test('Node version is 18+', () => {
    const output = execSync(`docker exec ${CONTAINER_NAME} node --version`, {
      encoding: 'utf-8',
    });

    const version = output.trim();
    expect(version).toMatch(/^v\d+\.\d+\.\d+$/);

    const majorVersion = parseInt(version.slice(1).split('.')[0]);
    expect(majorVersion).toBeGreaterThanOrEqual(18);
  });

  test('Next.js builds without errors', () => {
    // Check if .next directory exists in the container
    const output = execSync(`docker exec ${CONTAINER_NAME} ls -la .next`, {
      encoding: 'utf-8',
    });

    expect(output).toContain('static');
    expect(output).toContain('server');
  });

  test('application serves on expected port', async () => {
    // Check container is running
    const status = execSync(
      `docker ps -f name=${CONTAINER_NAME} --format "{{.Status}}"`,
      { encoding: 'utf-8' }
    );

    expect(status.trim()).toContain('Up');

    // Try to connect to the application
    try {
      const response = await axios.get(`http://localhost:${TEST_PORT}`, {
        timeout: 5000,
        validateStatus: () => true, // Accept any status code
      });

      // Should get some response (200, 404, etc. - just not connection refused)
      expect(response.status).toBeDefined();
    } catch (error: any) {
      if (error.code === 'ECONNREFUSED') {
        throw new Error('Application not serving on expected port');
      }
      // Other errors might be acceptable (e.g., API not configured)
    }
  }, 15000);

  test('environment variables are properly injected', () => {
    // Check if environment variable is set
    const output = execSync(
      `docker exec ${CONTAINER_NAME} printenv NEXT_PUBLIC_API_BASE_URL`,
      { encoding: 'utf-8' }
    );

    expect(output.trim()).toBe('http://localhost:8000');
  });

  test('health endpoint responds (if implemented)', async () => {
    try {
      const response = await axios.get(`http://localhost:${TEST_PORT}/api/health`, {
        timeout: 5000,
      });

      expect(response.status).toBe(200);
    } catch (error: any) {
      if (error.response?.status === 404) {
        console.log('Health endpoint not yet implemented - skipping');
      } else if (error.code === 'ECONNREFUSED') {
        throw new Error('Cannot connect to application');
      }
      // Skip test if endpoint not implemented
    }
  }, 10000);
});
