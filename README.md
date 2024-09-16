# KaFin2: AI-Powered Finance Dashboard 🤖📊

KaFin2 is an innovative open-source project that combines cutting-edge AI technology with comprehensive financial data analysis. Analyze and visualize financial data using natural language commands.

## Key Features ✨

- AI-driven natural language interface (OpenAI GPT-4)
- Dynamic dashboard generation
- Comprehensive financial data analysis
- Automatic data updates
- Multi-device support
- Cloud-native architecture
- Free and open-source

## Tech Stack 🛠

- Backend: Python, FastAPI, Pandas, NumPy, yfinance, FRED API, Google Drive API
- AI/ML: OpenAI API (GPT-4), scikit-learn
- Frontend: React, Recharts, Tailwind CSS
- Infrastructure: GitHub, GitHub Actions

## Quick Start 🚀

### Backend Setup

1. Clone the repository:
   ```
   git clone https://github.com/KAFKA2306/kafin2.git
   cd kafin2
   ```

2. Set up a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   - Copy the `.env.example` file to `.env`
   - Fill in your API keys for OpenAI and FRED

5. Run the FastAPI server:
   ```
   uvicorn src.backend.main:app --reload
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```
   cd frontend
   ```

2. Install dependencies:
   ```
   npm install
   ```

3. Start the development server:
   ```
   npm run dev
   ```

4. Open your browser and visit `http://localhost:3000`

## Usage 💡

1. Enter your financial analysis request in natural language.
2. The AI will interpret your request and fetch relevant data.
3. View the generated dashboard with charts and analysis.
4. Explore different visualizations and data points.

## Contributing 🤝

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for more details.

## License 📄

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments 🙏

- OpenAI for providing the GPT-4 API
- Federal Reserve Economic Data (FRED) for economic data
- Yahoo Finance for stock data
- The open-source community for various libraries and tools used in this project
