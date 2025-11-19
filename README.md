# Github Workflow

To keep work streamlined, accessible and to reduce risk of data loss, follow these recommendations before any action:

1. Short commentary format for updates/features/bug fixes
   - Use this required short-comment template for commits, PR descriptions and issue summaries:
     [Type] (Location): Short description. [Status]
     - Type: Fix | Feat | Docs | Refactor | Chore | Test
     - Location: folder, file path or branch (e.g. backend/api, ui/login, branch:feature/x)
     - Status: WIP | tested | not tested | reviewed
   - Examples:
     - Fix (backend/api): handle null user in login endpoint. [tested]
     - Feat (ui/login): add remember-me checkbox. [WIP]
     - Docs (README): clarify workflow examples. [not tested]

2. Local clones & backups
   - Keep a current local clone and push changes frequently.
   - Do not rely solely on GitHub as a single backup — keep local and (if needed) external backups.