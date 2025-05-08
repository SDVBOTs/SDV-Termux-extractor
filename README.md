
<h1 align="center">
  âœ¨ TERMUX Courses Extractor âœ¨
</h1>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python">
  <img src="https://img.shields.io/badge/Extractor-Script-success?style=for-the-badge&logo=hackthebox">
  <img src="https://img.shields.io/badge/CLI-Automation-orange?style=for-the-badge&logo=gnome-terminal">
</p>

<div align="center">

> **Smart, Fast & Reliable Extraction of Lecture Videos and Notes**  
> **from Apni Kaksha & PhysicsWallah using Auth Token only.**

</div>

---

## âœ¨ Features

- Automated batch, subject, and topic extraction  
- Extract video URLs (HLS `.m3u8`) and notes as `.txt`  
- Smart token authentication  
- Modern, optimized requests handling  
- Multi-page and multi-subject support  

---

## ðŸ§  How It Works?

<details>
  <summary><strong>Apni Kaksha Extractor (ak2.py)</strong></summary>

```bash
$ python ak2.py
```

1. Enter your Apni Kaksha Token  
2. Select your Batch  
3. Choose between Class or Notes  
4. Automatically saves all content into `<SubjectID>.txt`  
</details>

<details>
  <summary><strong>PhysicsWallah Extractor (pw.py)</strong></summary>

```bash
$ python pw.py
```

1. Enter your PW Auth Code  
2. Select your Batch and Subject  
3. Script fetches all Lecture URLs and saves them into `<BatchName>.txt`  
</details>

---

## ðŸ“‚ Output Example

```
Chemical Bonding - 01: https://...master.m3u8  
Mole Concept Notes: https://.../note.pdf  
```

---

## âš™ï¸ Requirements

Install dependencies:

```bash
pip install requests
```

> Python 3.7+ recommended for best performance

---

## ðŸª„ Fancy Preview

<div align="center">
  <img src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&pause=1000&color=448EE4&center=true&vCenter=true&width=435&lines=Extract+PW+and+ApniKaksha+like+a+Pro!;No+more+manual+copy-paste.;Just+Token+and+Done."/>
</div>

---

## ðŸ›¡ï¸ Disclaimer

This tool is intended for **educational and personal use only**.  
Any misuse for commercial or piracy purposes is strictly prohibited.

---

## â¤ï¸ Support

Star this repo if you found it helpful.  
For issues, feel free to raise an Issue.