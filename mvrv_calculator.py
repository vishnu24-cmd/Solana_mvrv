from solana import SolanaDataFetcher

class MVRVCalculator:
    def __init__(self):
        self.data_fetcher = SolanaDataFetcher()
    
    def calculate_mvrv(self):
        """Calculate MVRV ratio"""
        # Get data
        sol_price = self.data_fetcher.get_sol_price()
        circulating_supply = self.data_fetcher.get_circulating_supply()
        
        # Calculate market cap
        market_cap = sol_price * circulating_supply
        
        # Calculate realized value (simplified)
        realized_value = self.data_fetcher.get_realized_value(market_cap)
        
        # Calculate MVRV ratio
        mvrv_ratio = market_cap / realized_value if realized_value > 0 else 0
        
        return {
            'market_cap': round(market_cap, 2),
            'realized_value': round(realized_value, 2),
            'mvrv_ratio': round(mvrv_ratio, 4),
            'circulating_supply': circulating_supply,
            'sol_price': round(sol_price, 2)
        }