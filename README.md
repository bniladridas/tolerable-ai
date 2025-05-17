
---

<div align="center">
  <img src="static/images/logo.svg" alt="Tolerable AI Logo" width="120" height="120">
  <h1>Tolerable AI</h1>
  <p>Explore media with intelligence. Simple. Thoughtful. Yours.</p>
  <p>
    <a href="https://github.com/tolerable-ai/tolerable-ai/stargazers"><img src="https://img.shields.io/github/stars/tolerable-ai/tolerable-ai" alt="Stars Badge"/></a>
    <a href="https://github.com/tolerable-ai/tolerable-ai/network/members"><img src="https://img.shields.io/github/forks/tolerable-ai/tolerable-ai" alt="Forks Badge"/></a>
    <a href="https://github.com/tolerable-ai/tolerable-ai/issues"><img src="https://img.shields.io/github/issues/tolerable-ai/tolerable-ai" alt="Issues Badge"/></a>
    <a href="https://github.com/tolerable-ai/tolerable-ai/blob/main/LICENSE"><img src="https://img.shields.io/github/license/tolerable-ai/tolerable-ai" alt="License Badge"/></a>
  </p>
</div>

## A New Way to Discover

Tolerable AI is a minimalist web app that brings you closer to the media you love—movies, music, books, and games. Powered by Perplexity AI through the Together API, it delivers thoughtful, balanced insights in a clean, distraction-free interface.

## Designed for You

- **Elegant Simplicity**: A clutter-free UI that puts content first.
- **Media Focused**: Get curated AI responses tailored to your interests.
- **Seamless Interaction**: Keyboard shortcuts and intuitive controls.
- **Reliable & Transparent**: Graceful error handling with clear feedback.
- **Bot Protection**: GIPHY-based human verification to prevent automated access.
- **Compliant & Secure**: Includes Terms of Service and Privacy Statement.
- **Effortless Deployment**: Ready for Vercel in just a few steps.

## Get Started

### What You Need
- Python 3.8 or later
- A [Together API](https://www.together.ai/) key

### Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/tolerable-ai/tolerable-ai.git
   cd tolerable-ai
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Add your API key to a `.env` file:
   ```
   TOGETHER_API_KEY=your-api-key
   ```
4. Launch the app:
   ```bash
   python app.py
   ```
5. Visit `http://127.0.0.1:5000` in your browser.

## Deploy with Ease

### Vercel Deployment
1. Install Vercel CLI:
   ```bash
   npm install -g vercel
   ```
2. Log in:
   ```bash
   vercel login
   ```
3. Deploy:
   ```bash
   vercel
   ```
4. Set your API key:
   ```bash
   vercel env add TOGETHER_API_KEY
   ```
5. Go live:
   ```bash
   vercel --prod
   ```

## How It Works

- First-time visitors complete a simple GIPHY-based human verification.
- Enter a query and hit Enter (or press `/` to focus).
- Perplexity AI processes your request, delivering insights instantly.
- View responses in a sleek, highlighted display.
- Press `Esc` to dismiss modals.
- For development, use `/bypass-verification` to skip the verification step.

### Human Verification

The verification system uses a GIPHY showing someone falling. Valid answers include:
- "fall" or "falling"
- "trip" or "tripping"
- "slip" or "slipping"
- "stumble" or "stumbling"

Any description containing these keywords will pass verification. This information is included here for documentation purposes only.

## Inside Tolerable AI

```
tolerable-ai/
├── app.py                 # Core Flask app
├── templates/
│   ├── index.html         # Main UI template
│   ├── terms.html         # Terms of Service template
│   ├── privacy.html       # Privacy Statement template
│   └── verify.html        # Human verification template
├── static/
│   ├── css/               # Stylesheets
│   └── images/
│       ├── favicon.svg    # SVG favicon
│       ├── logo.svg       # Logo for README and UI
│       └── og-image.png   # Open Graph image for social sharing
├── vercel.json            # Vercel configuration
├── requirements.txt       # Dependencies
├── LICENSE                # MIT License
└── README.md              # This guide
```

## Thoughtful Error Handling

Errors are handled with care:
- Rate limits trigger a calm modal with an hourglass.
- Network issues show a pause icon and clear guidance.
- Logs capture technical details, keeping the UI serene.

## License

Open and free under the [MIT License](LICENSE).

## Connect

- [LinkedIn: Niladri Das](https://www.linkedin.com/in/bniladridas)
- [GitHub: tolerable-ai/tolerable-ai](https://github.com/tolerable-ai/tolerable-ai)

## Gratitude

Built with the brilliance of:
- [Together AI](https://www.together.ai/)
- [Perplexity AI](https://www.perplexity.ai/)
- [Flask](https://flask.palletsprojects.com/)
- [Vercel](https://vercel.com/)
