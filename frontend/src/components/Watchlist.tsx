interface WatchlistProps {
  tickers: string[]
  selectedTicker: string
  onSelect: (ticker: string) => void
}

export default function Watchlist({ tickers, selectedTicker, onSelect }: WatchlistProps) {
  return (
    <div>
      {tickers.map((ticker) => (
        <button
          key={ticker}
          onClick={() => onSelect(ticker)}
          style={{ fontWeight: ticker === selectedTicker ? 'bold' : 'normal' }}
        >
          {ticker}
        </button>
      ))}
    </div>
  )
}