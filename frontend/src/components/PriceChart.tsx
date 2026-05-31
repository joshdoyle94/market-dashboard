import { useQuery } from '@tanstack/react-query'
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts'
import { fetchPrices } from '../api/client'

interface PriceChartProps {
  ticker: string
}

export default function PriceChart({ ticker }: PriceChartProps) {
  const { data, isLoading, isError } = useQuery({
    queryKey: ['prices', ticker],
    queryFn: () => fetchPrices(ticker)
  })

  if (isLoading) return <div>Loading...</div>
  if (isError) return <div>Failed to load data</div>

  const chartData = data['20'].moving_average.map((value: number, index: number) => ({
    index,
    ma20: value,
    ma50: data['50'].moving_average[index]
  }))

  return (
    <ResponsiveContainer width="100%" height={300}>
      <LineChart data={chartData}>
        <XAxis dataKey="index" hide />
        <YAxis />
        <Tooltip />
        <Line type="monotone" dataKey="ma20" stroke="#8884d8" dot={false} name="MA20" />
        <Line type="monotone" dataKey="ma50" stroke="#82ca9d" dot={false} name="MA50" />
      </LineChart>
    </ResponsiveContainer>
  )
}