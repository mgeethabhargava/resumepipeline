"# resumepipeline" 
This code is developed on windows system
Install the requirements using pip
install tesseract
✅ Step-by-Step Fix on Windows
✅ 1. Install Tesseract for Windows

🔗 Download from official repo:
https://github.com/UB-Mannheim/tesseract/wiki

Choose the latest .exe installer (e.g., tesseract-ocr-w64-setup-5.3.1.20230401.exe)

⚙️ This version is optimized for Windows.

✅ 2. Install It

Run the installer.

✅ 3. (Optional) Add Tesseract to PATH Manually

a. Find install path

Default path:

C:\Program Files\Tesseract-OCR\

b. Add it to PATH:

Open Start Menu > Environment Variables

Click Environment Variables

Under System Variables, find and edit Path

Click New and add:

C:\Program Files\Tesseract-OCR\


Click OK and close all windows.

✅ 4. Verify Installation

Open Command Prompt and type:

tesseract --version


You should see version info like:
tesseract v5.3.1
 leptonica-1.82.0

 Update .env file with openai key 
 place images or pdf of resumes in main.py directory to parse
 update filepath of resume in main.py file
 run main.py file in command prompt 



tesseract v5.3.1
 leptonica-1.82.0
