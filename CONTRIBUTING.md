# Contributing to Angry Smurf Bot

Thank you for your interest in contributing! Here are some guidelines to help you get started.

## Development Setup

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/yourusername/angry-smurf.git
   cd angry-smurf
   ```
3. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Set up your testing environment with `.env`

## Making Changes

1. Create a feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```
2. Make your changes
3. Test thoroughly in a private Discord server
4. Commit your changes:
   ```bash
   git add .
   git commit -m "Add your descriptive commit message"
   ```
5. Push to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```
6. Open a Pull Request

## Code Style

- Follow PEP 8 Python style guidelines
- Use descriptive variable and function names
- Add comments for complex logic
- Keep functions focused and single-purpose

## Testing

- Always test your changes in a private Discord server first
- Use `TESTING_MODE=true` for rapid testing
- Verify both normal probability triggers and mention triggers work
- Test error handling and edge cases

## Types of Contributions

### Bug Fixes
- Fix existing functionality that isn't working correctly
- Improve error handling
- Performance optimizations

### Features
- New trigger mechanisms
- Additional response formats
- Configuration options
- Monitoring/logging improvements

### Documentation
- README improvements
- Code comments
- Setup guides
- Example configurations

## Submitting Pull Requests

Please include:
- **Clear description** of what your change does
- **Testing steps** you performed
- **Any new configuration** options added
- **Screenshots/logs** if relevant

## Questions?

Feel free to open an issue for:
- Bug reports
- Feature requests
- Questions about the codebase
- General discussion

## Code of Conduct

- Be respectful and constructive
- Focus on the code, not the person
- Help others learn and grow
- Keep discussions relevant to the project

Thank you for contributing! 🎭