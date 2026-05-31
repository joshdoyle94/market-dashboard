const BASE_URL = import.meta.env.VITE_API_URL || ''
export async function fetchPrices(ticker: string) {
  const response = await fetch(`${BASE_URL}/prices?ticker=${ticker}`)
  if (!response.ok) throw new Error('Failed to fetch prices')
  return response.json()
}