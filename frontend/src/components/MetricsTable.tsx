import { useQuery } from '@tanstack/react-query'
import { fetchPrices } from '../api/client'

interface MetricsTableProps {
  ticker: string
}

export default function MetricsTable({ ticker }: MetricsTableProps) {
  const { data, isLoading, isError } = useQuery({
  queryKey: ['prices', ticker],
  queryFn: () => fetchPrices(ticker),
  enabled: !!ticker
})

  if (isLoading) return <div>Loading...</div>
  if (isError) return <div>Failed to load data</div>
  if (!data) return <div></div>

  const latest20 = {
    moving_average: data['20'].moving_average.at(-1)?.toFixed(2),
    volatility: data['20'].volatility.at(-1)?.toFixed(4),
    daily_return: data['20'].daily_returns.at(-1)?.toFixed(4)
  }

  const latest50 = {
    moving_average: data['50'].moving_average.at(-1)?.toFixed(2),
    volatility: data['50'].volatility.at(-1)?.toFixed(4),
  }

  return (
    <table>
      <thead>
        <tr>
          <th>Metric</th>
          <th>20-Day</th>
          <th>50-Day</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>Moving Average</td>
          <td>{latest20.moving_average}</td>
          <td>{latest50.moving_average}</td>
        </tr>
        <tr>
          <td>Volatility</td>
          <td>{latest20.volatility}</td>
          <td>{latest50.volatility}</td>
        </tr>
        <tr>
          <td>Daily Return</td>
          <td>{latest20.daily_return}</td>
          <td>—</td>
        </tr>
      </tbody>
    </table>
  )
}