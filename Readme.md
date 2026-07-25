# John the Ripper - Automated Hash Cracking Labs

This directory contains my automation scripts and notes developed while completing the **John the Ripper** labs on **TryHackMe**. 

Instead of manually analyzing every hash and copy-pasting commands, I built automation tools to streamline the penetration testing workflow.

---

## 🛠️ The Challenge & Automation Idea

During cybersecurity labs, a common bottleneck is manually identifying hash types before cracking them. 
* Manually checking hash lengths takes extra time.
* Forgetting or mistyping the exact JtR format flag (like `--format=raw-md5` vs `md5`) causes errors.
* Misidentifying non-standard hashes (like the 9-letter **Whirlpool** algorithm used in advanced tasks) leads to hours of wasted CPU cycles on wrong bruteforce modes.

To solve this, I developed lightweight helper scripts that automatically analyze the hash structure and pass the correct configuration to John the Ripper.

---

## 📂 Directory Structure

```text
John-The-Ripper/
├── README.md              # Project documentation and write-up
├── crack_assistant.sh     # Bash automation wrapper for Linux environments
└── crack_assistant.py     # Python script using subprocess for advanced parsing
```

---

## 🚀 How the Scripts Work

Both scripts follow a 3-step SecOps automation logic:
1. **Length & Structure Analysis:** The script reads the hash from a file and counts the character length (e.g., 32 characters for MD5, 40 for SHA-1, 128 for Whirlpool/SHA-512).
2. **Dynamic Format Mapping:** It matches the length against known John the Ripper format identifiers. If it detects ambiguities (like a 128-character hash), it prompts the user to choose between `raw-whirlpool` or `raw-sha512`.
3. **Execution & Reporting:** It automatically fires up John the Ripper using the optimized `rockyou.txt` wordlist, completes the session, and immediately triggers `john --show` to print the cracked password in cleartext.

### Example Usage:
```bash
chmod +x crack_assistant.sh
./crack_assistant.sh hash_file.txt
```

---

## 🎯 Key Takeaways & Skills Learned

* **Hash Identification:** Mastered manual and automated recognition of cryptography standards (MD5, SHA-1, SHA-512, MD5Crypt, and Whirlpool).
* **Scripting for CyberSec:** Practiced Python (`subprocess` module) and Bash scripting to automate repetitive tasks in terminal environments.
* **Efficient Wordlist Auditing:** Learned how to correctly leverage wordlists instead of relying on resource-heavy incremental bruteforcing.
