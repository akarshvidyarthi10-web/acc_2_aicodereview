import { useState } from 'react'
import { getReviews } from '../services/api'

export default function useReviews() {
  const [reviews, setReviews] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  async function fetchReviews() {
    setLoading(true)
    setError(null)
    try {
      const data = await getReviews()
      setReviews(data)
    } catch (err) {
      setError(err.message || 'Unable to load reviews')
    } finally {
      setLoading(false)
    }
  }

  return { reviews, loading, error, fetchReviews }
}
