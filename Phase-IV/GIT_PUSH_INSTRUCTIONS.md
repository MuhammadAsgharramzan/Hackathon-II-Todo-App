# How to Push Changes to GitHub

The `git` command is not available in the current environment. Please follow these steps to manually push your changes.

## Prerequisites
1.  **Install Git**: Download and install from [git-scm.com](https://git-scm.com/downloads).
2.  **Verify Installation**: Open a new terminal and run `git --version`.

## Steps to Push

1.  **Open Terminal** in the project directory:
    ```bash
    cd h:\GIAIC\Todo-app-hackathon-II
    ```

2.  **Initialize/Check Git Status**:
    ```bash
    git status
    ```
    *(If not a git repo, run `git init` and add the remote)*

3.  **Add All Changes**:
    ```bash
    git add .
    ```

4.  **Commit Changes**:
    ```bash
    git commit -m "Phase IV: Cloud Native Deployment Artifacts"
    ```

5.  **Push to Remote**:
    ```bash
    git push origin main
    # Or if you need to set upstream:
    # git push -u origin main
    ```

## Remote URL
Ensure your remote is set correctly:
```bash
git remote set-url origin https://github.com/MuhammadAsgharramzan/Hackathon-II-Todo-App.git
```
