# bigPDFmaker

This Python CLI program combines PDF documents from a folder (non-recursively) into a big PDF (sorted by filename).

Bookmarks will be created for each document added to the big PDF.

## Run on Windows with uv

1. Install uv using PowerShell (see https://docs.astral.sh/uv/getting-started/installation/ for full instructions):

```powershell
PS> powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

2. Verify uv installed correctly:

```powershell
PS> uv --version
```

3. Navigate to your workspace directory. Below is an example, but you can use whichever directory you want:

```powershell
PS> Set-Location C:\Users\micha\workspace\github.com\the-chicken-leg\
```

4. Clone github repository and navigate to directory:

```powershell
PS> git clone https://github.com/the-chicken-leg/bigPDFmaker
PS> Set-Location .\bigPDFmaker\
```

5. Run using uv:

```powershell
PS> uv run main.py
```
