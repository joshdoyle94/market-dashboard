export async function fetchPrices(ticker: string) {
  const response = await fetch(`/api/prices?ticker=${ticker}`)
  if (!response.ok) throw new Error('Failed to fetch prices')
  return response.json()
}