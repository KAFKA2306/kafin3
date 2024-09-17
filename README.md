# KaFin2: AI-Powered Finance Dashboard

KaFin2 is an advanced financial data analysis dashboard that leverages AI to provide insightful analysis of stock market data and economic indicators. This project combines the power of FastAPI, React, and various financial APIs to deliver a user-friendly interface for financial analysis.

## Features

- Real-time stock data analysis using yfinance
- Economic data retrieval from FRED (Federal Reserve Economic Data)
- AI-powered insights using OpenAI's GPT-4
- Interactive charts and visualizations
- Natural language query interface for financial analysis
- Google Drive integration for data storage and retrieval

## Prerequisites

- Python 3.8+
- Node.js 14+
- npm or yarn
- OpenAI API key
- FRED API key
- Google Cloud Platform account with Drive API enabled

## Setup

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/kafin2.git
   cd kafin2
   ```

2. Set up the backend:
   ```
   cd src/backend
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   Create a `.env` file in the `src/backend` directory with the following content:
   ```
   OPENAI_API_KEY=your_openai_api_key
   FRED_API_KEY=your_fred_api_key
   ```

4. Set up Google Drive API:
   - Follow the [Google Drive API Python Quickstart](https://developers.google.com/drive/api/quickstart/python) to create credentials.
   - Save the `credentials.json` file in the `src/backend` directory.
   - Run the `generate_token.py` script to create `token.json`:
     ```
     python generate_token.py
     ```

5. Set up the frontend:
   ```
   cd ../../frontend
   npm install  # or yarn install
   ```

## Running the Application

1. Start the backend server:
   ```
   cd src/backend
   uvicorn main:app --reload
   ```

2. In a new terminal, start the frontend development server:
   ```
   cd frontend
   npm start  # or yarn start
   ```

3. Open your browser and navigate to `http://localhost:3000` to use the application.

## Usage

1. Enter your financial analysis query in natural language (e.g., "Compare Apple and Microsoft stock prices for the last 6 months").
2. View the generated charts, AI analysis, and financial data on the dashboard.
3. Explore different tabs for more detailed information and insights.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

- OpenAI for providing the GPT-4 API
- Federal Reserve Bank of St. Louis for the FRED API
- Yahoo Finance for real-time stock data
- All other open-source libraries and tools used in this project