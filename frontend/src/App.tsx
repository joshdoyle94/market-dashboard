import { useState } from 'react'
// import Watchlist from './components/Watchlist'
import TickerInput from './components/TickerInput'
import PriceChart from './components/PriceChart'
import MetricsTable from './components/MetricsTable'

// const TICKERS = ['TSLA', 'AAPL', 'NVDA', 'NFLX']

export default function App() {
  const [selectedTicker, setSelectedTicker] = useState('')

  return (
    <div>
      <h1>Market Dashboard</h1>
      <TickerInput
      onSetTicker={setSelectedTicker}
      />
      {/* <Watchlist
        tickers={TICKERS}
        selectedTicker={selectedTicker}
        onSelect={setSelectedTicker}
      /> */}
      <PriceChart ticker={selectedTicker} />
      <MetricsTable ticker={selectedTicker} />
    </div>
  )
}