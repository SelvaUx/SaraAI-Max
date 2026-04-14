# SaraAI Max — Example Commands

Because SaraAI Max is an **Autonomous Intelligence**, you don't need to write code or memorize strict syntax to use her tools! You simply talk to her in natural language, and her Agentic Loop automatically figures out which tool to call, constructs the arguments, and executes it.

Here are highly detailed examples of how you can instruct Sara to trigger every single tool:

### 1. `read_file`
**What it does:** Reads the raw text contents of any file on your computer so Sara can analyze the code or text.
**Example Prompt:**
> *"Sara, read the `sara/agent.py` file and explain how the tool-calling loop works. Are there any bugs in it?"*
*(Sara will autonomously call `read_file(filepath="sara/agent.py")`, analyze the returned text, and explain it to you.)*

### 2. `write_file`
**What it does:** Allows Sara to create brand new files or completely overwrite existing files with new code/text.
**Example Prompt:**
> *"Create a new Python script named `scraper.py`. It should use BeautifulSoup to scrape Hacker News and print the top 5 titles. Once you write the code, save it to my Desktop."*
*(Sara will generate the Python code, then call `write_file(filepath="C:/Users/SelvaUx/Desktop/scraper.py", content="...")` to save it.)*

### 3. `search_files`
**What it does:** Uses glob pattern matching to search through directories to find specific files based on extensions or names.
**Example Prompt:**
> *"Look through my entire `SaraAI-Max` project directory and find all the `.json` configuration files."*
*(Sara will call `search_files(directory=".", pattern="**/*.json")` and list out every JSON file she finds.)*

### 4. `run_command`
**What it does:** Executes raw shell/PowerShell commands in your terminal. This allows Sara to run code, install pip packages, or move files.
**Example Prompt:**
> *"Run my `scraper.py` file and tell me what the output is. If it throws an error, install the missing Pip requirements."*
*(Sara will call `run_command(command="python scraper.py")`. If it fails because of missing BS4, she will call `run_command(command="pip install beautifulsoup4")` and try again!)*

### 5. `web_search`
**What it does:** Performs a live DuckDuckGo internet search to fetch real-time data that isn't in her AI training data.
**Example Prompt:**
> *"Search the web for the latest patch notes for React version 19 and summarize the biggest breaking changes."*
*(Sara will call `web_search(query="React 19 patch notes breaking changes")`, read the live results, and summarize them.)*

### 6. `wikipedia`
**What it does:** Looks up and reads the summary of Wikipedia articles for highly factual, encyclopedic knowledge.
**Example Prompt:**
> *"Look up 'Quantum Entanglement' on Wikipedia and explain it to me like I'm a 5-year-old."*
*(Sara will call `wikipedia(query="Quantum Entanglement")` and synthesize the factual summary for you.)*

### 7. `open_app`
**What it does:** Interacts with the Windows operating system to launch desktop applications.
**Example Prompt:**
> *"I need to write some notes. Please open Notepad for me."*
*(Sara will call `open_app(app_name="notepad")` and the Notepad application will instantly pop up on your screen.)*

### 8. `get_sysinfo`
**What it does:** Checks your machine's hardware stats, verifying CPU load, total memory, available RAM, and OS version.
**Example Prompt:**
> *"Check my system specs. Do I have enough available RAM right now to run a heavy 14B parameter Ollama model?"*
*(Sara will call `get_sysinfo()` to check your RAM. If you only have 2GB free, she will politely advise you that your PC might struggle.)*

### 9. `calculate`
**What it does:** Evaluates complex math expressions securely. LLMs are historically bad at math, so this gives Sara a built-in calculator for absolute precision.
**Example Prompt:**
> *"If I invest 5000 at a 7% annual interest rate, compounded monthly, exactly how much will I have in 10 years?"*
*(Sara will construct the algebraic formula and call `calculate(expression="5000 * (1 + 0.07/12)**(12 * 10)")` to get the flawless mathematical answer.)*

### 10. `take_screenshot`
**What it does:** Captures an image of your current Windows desktop and saves it.
**Example Prompt:**
> *"Take a screenshot of my screen right now and save it as `desktop_proof.png` in my current folder."*
*(Sara will call `take_screenshot(save_path="desktop_proof.png")` to execute the screen grab.)*

### 11. `get_datetime`
**What it does:** Retrieves the exact current local system time.
**Example Prompt:**
> *"What time is it right now, and how many days are left until New Year's?"*
*(Sara will call `get_datetime()` to fetch today's date, then optionally call `calculate()` to subtract the days, returning the exact countdown.)*

### 12. `list_processes`
**What it does:** Scans your Windows Task Manager process lists natively.
**Example Prompt:**
> *"Is Google Chrome currently running on my computer? If so, how much memory is it eating up?"*
*(Sara will call `list_processes()` and filter the list to find `chrome.exe`, returning both its PID and RAM usage.)*

---

### **The Power of Chaining (Agentic Loop)**

The true brilliance of SaraAI Max is that she can **chain these tools together** without you asking.

**Master Prompt Example:**
> *"Check if Chrome is running. If it is, kill the process. Then, take a screenshot of my desktop, upload it to my desktop folder, and search the web for 'cool desktop wallpapers'."*

Sara will autonomously:
1. `list_processes()` -> spots Chrome.
2. `run_command(command="taskkill /IM chrome.exe /F")` -> kills it.
3. `take_screenshot(save_path="C:/Users/SelvaUx/Desktop/snap.png")` -> takes the picture.
4. `web_search(query="cool desktop wallpapers")` -> finds wallpapers and reports back!
