# Physical AI Humanoid Robotics

This repository contains the codebase for a Physical AI Humanoid Robotics project, built using modern web technologies. The project follows a microservices architecture with separate backend and frontend components.

## Project Structure

- `backend/` - Contains the backend services and APIs
- `frontend/` - Contains the Docusaurus-based frontend application
- `.specify/` - Contains project specifications and planning artifacts
- `specs/` - Contains feature specifications and plans
- `history/` - Contains prompt history records and architecture decision records

## Frontend Application

The frontend is built using [Docusaurus](https://docusaurus.io/), a modern static website generator.

### Installation

```bash
cd frontend
yarn install
```

### Local Development

```bash
cd frontend
yarn start
```

This command starts a local development server and opens up a browser window. Most changes are reflected live without having to restart the server.

### Building the Project

```bash
cd frontend
yarn build
```

This command generates static content into the `build` directory and can be served using any static content hosting service.

## Deployment to GitHub Pages

The frontend application can be deployed to GitHub Pages using the following methods:

### Method 1: Using GitHub Actions (Recommended)

The GitHub Actions workflow is already configured in `.github/workflows/deploy.yml`. The workflow is properly set up with the correct configuration for your repository. To enable deployment:

1. Make sure the Docusaurus configuration is correct (already updated):
   - baseUrl should be `/Physical-AI-Humanoid-Robotics-/`
   - projectName should be `Physical-AI-Humanoid-Robotics-`
   - organizationName should be `1177rashid`

2. Regenerate the build files to apply configuration changes:
   ```bash
   cd frontend
   npm run build
   ```
   This step is crucial - the build files must be regenerated to reflect the new configuration.

3. Enable GitHub Pages in your repository settings:
   - Go to Settings > Pages
   - Select "GitHub Actions" as the source

### Method 2: Manual Deployment

```bash
cd frontend
GIT_USER=<Your GitHub username> USE_SSH=false yarn deploy
```

This command builds the website and pushes the static files to the `gh-pages` branch, which GitHub automatically serves.

### Method 3: Deploy from Local Build

If you have already built the project locally:

1. Navigate to the `frontend/build` directory
2. Copy the contents to a new branch or directly to the `gh-pages` branch
3. Push the changes to GitHub

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add some amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.