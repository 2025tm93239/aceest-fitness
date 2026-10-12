# Jenkins BUILD & Quality Gate (Assignment 1 — Step 5)

Jenkins is the **secondary** validation layer: it pulls fresh code from GitHub and runs a **clean** build (install → compile → pytest → Docker) on the Jenkins machine.

GitHub Actions = CI on every push/PR.  
Jenkins = controlled BUILD server (same checks, different environment).

---

## 1. What you need

| Item | Purpose |
|------|---------|
| Jenkins (LTS) | Build server |
| Git plugin | Clone from GitHub |
| Pipeline plugin | Run `Jenkinsfile` |
| Python 3.9 on Jenkins agent | `pip`, `pytest`, `compileall` |
| Docker (optional but recommended) | Docker build + tests in container |
| GitHub repo URL | Source for SCM |

`Jenkinsfile` at repo root defines the pipeline stages.

---

## 2. Install Jenkins on Windows (local lab)

1. Download **Jenkins LTS** (Windows installer): https://www.jenkins.io/download/
2. Install and open http://localhost:8080
3. Unlock with initial admin password (installer shows path).
4. Install suggested plugins → create admin user.

**Plugins (Manage Jenkins → Plugins):**

- Git
- Pipeline
- GitHub (optional, for webhooks)
- Docker Pipeline (optional)

**Tools on the same PC:**

- Python 3.9 (`python3` and `pip` on PATH; lab VM: 3.9.21)
- Docker Desktop running (for Docker stages)

---

## 3. GitHub access from Jenkins

### Public repository

No credentials required for read-only clone.

### Private repository

1. GitHub → **Settings → Developer settings → Personal access tokens**
2. Create token with `repo` scope
3. Jenkins → **Manage Jenkins → Credentials → Add**
   - Kind: **Username with password**
   - Username: your GitHub username
   - Password: the **token** (not your GitHub password)
   - ID: e.g. `github-aceest`

---

## 4. Create the Jenkins job

1. **New Item** → name: `aceest-fitness-build` → type **Pipeline** → OK
2. **Build Triggers** (optional):
   - *Poll SCM*: `H/5 * * * *` (check GitHub every ~5 min), or
   - GitHub webhook `http://JENKINS_URL/github-webhook/` when Jenkins is reachable
3. **Pipeline** section:
   - Definition: **Pipeline script from SCM**
   - SCM: **Git**
   - Repository URL: `https://github.com/<YOUR_USER>/aceest-fitness.git`
   - Credentials: (if private)
   - Branch: `*/main` (or your default branch)
   - Script Path: `Jenkinsfile`
4. **Save** → **Build Now**

---

## 5. What each stage does (quality gate)

| Stage | Assignment meaning |
|-------|-------------------|
| Checkout | Fresh copy from GitHub (clean workspace) |
| Install dependencies | `pip install -r requirements.txt` |
| Build (compile) | `python -m compileall` — syntax / compile check |
| Quality gate — unit tests | `pytest -v` on agent |
| Docker build | Portable image assembly |
| Tests in container | `pytest` inside image (stability in container) |

`post { always { cleanWs() } }` removes workspace after build so the next run is clean.

---

## 6. Success criteria for submission

- Screenshot: Jenkins job **#n** with all stages green
- README note: Jenkins job name, GitHub repo URL, that pipeline uses `Jenkinsfile`
- `Jenkinsfile` committed and pushed to GitHub

---

## 7. Commit and push Jenkinsfile

```bash
cd aceest-fitness
git add Jenkinsfile docs/JENKINS-SETUP.md
git commit -m "Add Jenkins pipeline for build and quality gate"
git push origin main
```

---

## 8. Troubleshooting

| Problem | Fix |
|---------|-----|
| `No module named pip` on Jenkins agent | Install system package: `sudo yum install python3-pip` or `sudo apt install python3-pip`, then restart Jenkins. Or push latest `Jenkinsfile` (bootstraps pip via `ensurepip` / `get-pip.py --user`). |
| `python` not found | Install Python; add to PATH; restart Jenkins service |
| `pytest` not found | Pipeline uses `python3 -m pytest` after `pip install --user` |
| `permission denied` on `/var/run/docker.sock` | Jenkins user is not in the `docker` group — see **Docker access for Jenkins** below |
| `docker` not found | Install Docker and start the service: `sudo systemctl enable --now docker` |

### Docker access for Jenkins (required for Docker build stage)

Jenkins runs as user **`jenkins`**. By default it cannot use Docker.

On the **Jenkins Linux VM** (needs `sudo`):

```bash
# 1) Ensure Docker is installed and running
sudo systemctl enable --now docker

# 2) Allow the jenkins user to use Docker
sudo usermod -aG docker jenkins

# 3) Apply the new group (restart Jenkins service)
sudo systemctl restart jenkins

# 4) Verify (must succeed without errors)
sudo -u jenkins docker ps
sudo -u jenkins docker run --rm hello-world
```

Then run **Build Now** again in Jenkins.

If step 4 still fails, log out/in is not enough for the service — **`systemctl restart jenkins`** is required after `usermod`.

**Lab / no sudo:** Ask the VM administrator (e.g. course cloud admin) to run the commands above. Your pipeline is already correct through the pytest stage.
| `curl: command not found` during pip bootstrap | Ask admin to install `python3-pip`, or install `curl` on the agent |
| Wrong branch | Set Branch Specifier to `*/main` or your branch |
| Pipeline not found | Script Path must be exactly `Jenkinsfile` (capital J) |

---

## 9. Alternative: Jenkins in Docker (Linux)

```bash
docker run -d -p 8080:8080 -p 50000:50000 \
  -v jenkins_home:/var/jenkins_home \
  jenkins/jenkins:lts
```

Mount the Docker socket only if you understand the security implications (lab use). On a Linux agent, the `Jenkinsfile` `sh` stages match this setup directly.
