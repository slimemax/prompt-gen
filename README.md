Here is a `README.md` file for your project:

```markdown
# Visual Descriptor Prompt Builder

This project is a **Visual Descriptor Prompt Builder** built with `Tkinter` for creating structured prompts based on XML files. It allows users to dynamically load XML files containing categories and words, add words to a prompt, and then auto-type or copy the prompt to the clipboard.

## Features

- **XML File Support**: Automatically scan the working directory for XML files to load word categories.
- **Dynamic UI**: Category buttons are created dynamically based on the loaded XML, with the categories displayed in a structured layout.
- **Prompt Building**: Users can build prompts using buttons that add pre-defined words from categories.
- **Auto Typing**: Automatically type the generated prompt with a customizable time delay.
- **Copy to Clipboard**: Quickly copy the constructed prompt to the clipboard for later use.
- **Alerts**: An alert box displays important messages, such as errors or informational alerts.
- **Abort Auto Typing**: Ability to stop the auto-typing process at any point.

## How to Use

### 1. XML File Structure
The XML file should be structured like this:
```xml
<categories>
    <category name="Category 1">
        <word>word1</word>
        <word>word2</word>
    </category>
    <category name="Category 2">
        <word>word3</word>
        <word>word4</word>
    </category>
</categories>
```
Place the XML files in the same directory as the script.

### 2. Running the Program
1. Clone the repository:
   ```bash
    git clone https://github.com/slimemax/prompt-gen.git
    cd prompt-gen
   ```
2. Install required dependencies:
   ```bash
   pip install pyperclip pyautogui
   ```
3. Run the script:
   ```bash
   python main.py
   ```

### 3. Building Prompts
- Select an XML file from the dropdown and click "Load XML".
- Categories and words will be displayed as buttons.
- Click on the buttons to add words to the prompt.
- Use the "Auto Comma" checkbox to control comma placement.
- Use the "Copy to Clipboard" button to copy the prompt.
- Use the "Auto Type" button to auto-type the generated prompt.

## Requirements

- Python 3.x
- Tkinter (comes pre-installed with Python)
- pyperclip
- pyautogui

## Contributions

Contributions are welcome! Please open an issue or submit a pull request if you have suggestions or improvements.

## License

This project is licensed under the MIT License.
```

You can replace `YOUR_USERNAME` and `YOUR_REPOSITORY_NAME` with your actual GitHub username and repository name before uploading it.
