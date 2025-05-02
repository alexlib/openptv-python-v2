# Git Workflow for OpenPTV Python

This document describes the Git workflow for the OpenPTV Python project.

## Branches

The repository has the following main branches:

- **master**: The stable branch that contains production-ready code
- **develop**: The development branch where new features are integrated

## Feature Development

When developing a new feature or fixing a bug, follow these steps:

1. Create a feature branch from `develop`:
   ```bash
   git checkout develop
   git pull
   git checkout -b feature/your-feature-name
   ```

2. Make your changes and commit them with descriptive messages:
   ```bash
   git add .
   git commit -m "Descriptive message about your changes"
   ```

3. Push your feature branch to the remote repository:
   ```bash
   git push -u origin feature/your-feature-name
   ```

4. When the feature is complete, create a pull request to merge it into `develop`.

## Release Process

When ready to release a new version:

1. Create a release branch from `develop`:
   ```bash
   git checkout develop
   git pull
   git checkout -b release/v1.0.0
   ```

2. Update version numbers and make any final adjustments.

3. Merge the release branch into both `master` and `develop`:
   ```bash
   # Merge to master
   git checkout master
   git merge --no-ff release/v1.0.0
   git tag -a v1.0.0 -m "Version 1.0.0"
   git push origin master --tags
   
   # Merge back to develop
   git checkout develop
   git merge --no-ff release/v1.0.0
   git push origin develop
   ```

4. Delete the release branch:
   ```bash
   git branch -d release/v1.0.0
   ```

## Bug Fixes

For urgent bug fixes:

1. Create a hotfix branch from `master`:
   ```bash
   git checkout master
   git pull
   git checkout -b hotfix/bug-description
   ```

2. Fix the bug and commit the changes.

3. Merge the hotfix branch into both `master` and `develop`:
   ```bash
   # Merge to master
   git checkout master
   git merge --no-ff hotfix/bug-description
   git tag -a v1.0.1 -m "Version 1.0.1"
   git push origin master --tags
   
   # Merge to develop
   git checkout develop
   git merge --no-ff hotfix/bug-description
   git push origin develop
   ```

4. Delete the hotfix branch:
   ```bash
   git branch -d hotfix/bug-description
   ```

## Best Practices

1. **Commit Messages**: Write clear, descriptive commit messages that explain what changes were made and why.

2. **Pull Regularly**: Pull from the remote repository regularly to stay up-to-date with changes made by others.

3. **Code Review**: Have your code reviewed by at least one other developer before merging into `develop`.

4. **Testing**: Make sure all tests pass before creating a pull request.

5. **Documentation**: Update documentation when making changes to the codebase.

## Git Commands Reference

- Check status: `git status`
- Create branch: `git checkout -b branch-name`
- Switch branch: `git checkout branch-name`
- Pull changes: `git pull`
- Add files: `git add file-name` or `git add .`
- Commit changes: `git commit -m "Message"`
- Push changes: `git push` or `git push -u origin branch-name`
- View branches: `git branch`
- View commit history: `git log`
- Merge branch: `git merge branch-name`
- Create tag: `git tag -a v1.0.0 -m "Version 1.0.0"`
- Push tags: `git push --tags`
