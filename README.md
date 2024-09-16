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

- Backend: Python, Streamlit, Pandas, NumPy, yfinance
- Data Sources: yfinance, FRED API, Google Drive API
- AI/ML: OpenAI API (GPT-4)
- Frontend: Streamlit, Plotly, Tailwind CSS
- Infrastructure: Streamlit Cloud, GitHub, GitHub Actions

## Quick Start 🚀

1. Visit [https://kafin2-c4yymao99f2tnx8vdflb7o.streamlit.app](https://kafin2-c4yymao99f2tnx8vdflb7o.streamlit.app)
2. Enter a stock ticker (e.g., AAPL, GOOGL) in the sidebar
3. Adjust the number of days for analysis using the slider
4. Explore the generated stock chart and financial analysis

## For Developers 🖥

1. Clone the repository:
   ```
   git clone https://github.com/KAFKA2306/kafin2.git
   cd kafin2
   ```

2. Set up the environment:
   ```
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Set environment variables:
   ```
   export OPENAI_API_KEY=your_openai_api_key
   export FRED_API_KEY=your_fred_api_key
   export GOOGLE_DRIVE_CREDENTIALS='{your_google_drive_credentials_json}'
   ```

4. Run locally:
   ```
   streamlit run src/streamlit_app.py
   ```

## Deployment 🌐

To deploy KaFin2 on Streamlit Cloud:

1. Fork this repository to your GitHub account.
2. Sign up for a [Streamlit Cloud account](https://streamlit.io/cloud).
3. Click on "New app" and select your forked repository.
4. Set the main file path to `src/streamlit_app.py`.
5. (Optional) Configure your app's subdomain.
6. Click "Deploy!" to launch your app.

## Future Improvements 🚀

- Enhanced natural language processing for more complex financial queries
- Integration with additional financial data sources
- Advanced AI-driven financial forecasting and recommendations
- User authentication and personalized dashboards
- Mobile app development for on-the-go analysis

Contribute to KaFin2 and help revolutionize financial analysis with AI!

## License 📄

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments 🙏

- OpenAI for providing the GPT-4 API
- Streamlit for their excellent app framework
- The open-source community for various libraries and tools used in this project
