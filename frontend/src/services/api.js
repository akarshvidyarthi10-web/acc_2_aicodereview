const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api'

export async function getReviews() {
  const response = await fetch(`${BASE_URL}/reviews`)
  if (!response.ok) {
    throw new Error('Failed to fetch reviews')
  }
  return response.json()
}

export async function getReview(id) {
  const response = await fetch(`${BASE_URL}/reviews/${id}`)
  if (!response.ok) {
    throw new Error('Failed to fetch review details')
  }
  return response.json()
}
