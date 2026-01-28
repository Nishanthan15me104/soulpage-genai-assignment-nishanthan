# src/data/mock_db.py
from src.state import CompanyResearchDoc, StockData, NewsItem

# A dictionary mimicking a database or local file store
MOCK_DATABASE = {
    "Tesla": CompanyResearchDoc(
        company_name="Tesla",
        source="mock_local_cache",
        stock_data=StockData(symbol="TSLA", current_price=210.50),
        latest_news=[
            NewsItem(
                title="Tesla expands Giga Texas",
                summary="Tesla plans to add a new battery line in Texas.",
                source="TechCrunch"
            ),
            NewsItem(
                title="EV Market Competition Heats Up",
                summary="BYD overtakes Tesla in global sales for Q4.",
                source="Bloomberg"
            )
        ]
    ),
    "Apple": CompanyResearchDoc(
        company_name="Apple",
        source="mock_local_cache",
        stock_data=StockData(symbol="AAPL", current_price=185.00),
        latest_news=[
            NewsItem(
                title="Vision Pro Release Date",
                summary="Apple announces Vision Pro availability in US stores.",
                source="TheVerge"
            )
        ]
    )
}

def get_mock_data(company_name: str) -> CompanyResearchDoc:
    """Fallback function to retrieve local data"""
    return MOCK_DATABASE.get(company_name)