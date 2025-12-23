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

1. Create a `.github/workflows/deploy.yml` file with the following content:

```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches: [main]
  workflow_dispatch:

jobs:
  deploy:
    name: Deploy to GitHub Pages
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: 18
          cache: yarn
      - name: Install dependencies
        run: yarn install --frozen-lockfile
      - name: Build website
        run: yarn build
      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./frontend/build
```

2. Enable GitHub Pages in your repository settings:
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