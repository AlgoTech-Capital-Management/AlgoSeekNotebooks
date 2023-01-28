# AlgoSeek Datasets

## US Equity Reference Data

### SEC Master Base

| Field | Type (format) | Missing | Description |
|-------|---------------|---------|-------------|
| SecId | integer | Never | algoseek unique security identifier |
| Tickers | string (tricker1; ticker2;…) | Never | List of symbol names used. If security had its ticker changed, the field will have multiple tickers separated by a semicolon “;” |
| TickersStartToEndDate | string (yyyymmdd:yyyymmdd;…) | Never | Start and end dates for each ticker. EndDate = 20991231 when the ticker is still being used |
| Name | string (name1; name2;…) | Never | List of security names used. If security had its name changed, the field will have multiple tickers separated by a semicolon “;” |
| NameStartToEndDate | string (yyyymmdd:yyyymmdd;…) | Never | Start and end dates for each name. EndDate = 20991231 when the name is still being used |
| ISIN | string (ISIN1;ISIN2;…) | Blank | List of ISIN codes used. If security had its ISINchanged, the field will have multiple tickers separated by a semicolon “;”|
| ISINStartToEndDate | string (yyyymmdd:yyyymmdd;…)| Blank | Start and end dates for each ISIN. EndDate = 20991231 when the ISIN is still being used |
| ListStatus | string | Blank | Current list status. D = Delisted. L = Listed |
| SecurityDescription | string | Blank | Current Security Description |
| USIdentifier | string (name1;name2;…) | Blank | List of USIdentifiers for US securities used. If security had its USIdentifier changed, the field will have multiple identifiers separated by a semicolon “;” |
| USIdentifierStartToEndDate | string (yyyymmdd:yyyymmdd;…)| Blank | Start and end dates for each USIdentifier. EndDate = 20991231 when the USIdentifier is still being used|
| PrimaryExchange | string (exchange1;exchange2;…)| Never | List of Primary Exchange(s). If security had its Primary Exchange changed, the field will have multiple exchange names separated by a semicolon “;” |
| PrimaryExchangeStartToEndDate | string (yyyymmdd:yyyymmdd;…)| Never | Start and end dates for each Primary Exchange. EndDate = 20991231 when the Primary Exchange is still being used |
| SEDOL | string | Blank | Current Stock Exchange Daily Official List |
| Sic | integer | Blank | Current Standard Industrial Classification code |
| Sector | string | Blank | Current SIC Sector | 
| Industry | string | Blank | Current SIC Industry |
| FIGI | string (FIGI1; FIGI2;…) | Blank | Financial Instrument Global Identifier. If security had its FIGI changed, the field will have multiple exchange names separated by a semicolon “;” |

## US Equity Market Data

### Primary Adjusted OHLC Daily

| Field | type (format) | Description |
|-------|---------------|-------------|
| SecId | integer | algoseek unique Security ID |
| TradeDate | string (yyyymmdd) | Trading date in yyyymmdd format |
| Ticker | string | Symbol name |
| Name | string | Name of equity security |
| PrimaryExchange | string | Primary listing exchange on this TradeDate |
| ISIN | string | ISIN as of this trade date. Optional |
| OpenPrice | decimal | Primary exchange opening trade (see section “Opening Trade Identification”)|
| OpenSize | integer | Primary exchange open trade size|
| OpenTime | time | Time of the Primary exchange opening trade|
| HighPrice | decimal | Highest trade price from any exchange or Trade Reporting Facility (TRF)|
| HighTime | time | Time of the highest trade|
| LowPrice | decimal | Lowest trade price from any exchange or Trade Reporting Facility (TRF)|
| LowTime | time | Time of the lowest trade|
| ClosePrice | decimal | Primary exchange closing trade (see section “Closing Trade Identification”)|
| CloseSize | integer | Primary exchange close trade size|
| CloseTime | time | Time of the Primary exchange closing trade|
| ListedMarketHoursVolume | integer | Public Listed exchanges trading volume during regularmarket hours only|
| ListedMarketHoursTrades | integer | Number of trades during regular market hours in public listed exchanges |
| ListedTotalVolume | integer | Public Listed exchanges trading volume for the whole day (includes pre, regular, and post-market) |
| ListedTotalTrades | integer | Public Total number of trades for the trade date (includes pre-, regular, and post-market) in listed exchanges |
| FinraMarketHoursVolume | integer | FINRA/TRF trading volume during regular market hours only (normal trade day is 09:30:00 to 16:00:00 EST). FINRA/TRP represents off-exchange trading. |
| FinraMarketHoursTrades | integer | The number of FINRA/TRF trades during regular market hours. FINRA/TRF represents off-exchange trading. |
| FinraTotalVolume | integer | FINRA/TRF trading volume for the whole day (includes pre-, regular, and post-market) |
| FinraTotalTrades | integer | Total number of FINRA/TRF trades for the trade date (includes pre, regular, and post-market). FINRA/TRF represents off-exchange trading. |
| MarketVWAP | decimal | Volume weighted average price during regular market hours, normally between 09:30:00 and 16:00:00 EST plus the Opening and Closing Cross (which may be after 16:00:00 EST). |
| DailyVWAP | decimal | Volume weighted average price for the whole day including pre, regular, and post-market trades |