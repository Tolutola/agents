# My Git Workflow for the Agents Course

How I keep my practice work safe while pulling the latest course material.

## How it's set up

| Name | What it is |
|---|---|
| `origin` | My fork: https://github.com/Tolutola/agents (my backup) |
| `upstream` | Ed's repo: https://github.com/ed-donner/agents (course source) |
| `my-work` branch | Where I practice. I stay on this branch. |
| `main` branch | Ed's version, kept clean. I don't work here. |

Every lab notebook has a `_mine` copy next to it, for example `1_foundations/1_lab1_mine.ipynb`.
**I only edit and run the `_mine` copies.** The originals stay untouched, so pulling updates never conflicts with my work.

## Get Ed's latest changes

```bash
git pull --no-rebase --no-edit upstream main
```

Updated originals arrive next to my `_mine` copies. Open them side by side to see what changed.

## Save and back up my work

```bash
git add -A
git commit -m "Lab 2 practice"
git push
```

`git push` sends my work to my fork on GitHub.

## Start a new lab

If Ed adds a new notebook, make a `_mine` copy **before** editing or running it. Keep the copy in the same folder, because labs open files by relative path.

- **VS Code:** select the notebook, press Cmd+C then Cmd+V, and rename the copy to end in `_mine.ipynb`.
- **Terminal:** `cp 2_openai/5_lab5.ipynb 2_openai/5_lab5_mine.ipynb`

## Check where I am

```bash
git status      # what's changed, and which branch I'm on
git branch      # the * marks my current branch (should be my-work)
git remote -v   # origin = my fork, upstream = Ed
```

## If something goes wrong

| Problem | Fix |
|---|---|
| `git pull` says local changes "would be overwritten" | I changed or ran an original notebook. To keep the changes, copy it to `_mine` first. Then reset the original with `git restore <file>`. |
| My `_mine` notebooks have disappeared | I'm on `main`. Run `git switch my-work`. |
| A pull stops with a merge conflict | Run `git merge --abort` to undo the pull, then sort out the conflicting file before pulling again. |
| `git push` asks me to sign in | Run `gh auth login`, then push again. |

## Keep secrets out

My fork is **public**, so anyone can see what I push.
- Keep API keys in `.env`. Git ignores it, so it never gets committed.
- Never paste a key into a notebook cell. Load keys with `load_dotenv()` and `os.getenv(...)`.

## Viewing my work on GitHub

My fork opens on `main` (Ed's version). To see my notebooks there, pick **`my-work`** from the branch menu.
