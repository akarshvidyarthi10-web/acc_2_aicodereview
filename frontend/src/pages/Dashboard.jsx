import { useEffect } from 'react'
import PRList from '../components/PRList'
import useReviews from '../hooks/useReviews'

export default function Dashboard() {
  const { reviews, loading, error, fetchReviews } = useReviews()

  useEffect(() => {
    fetchReviews()
  }, [])

  return (
    <section className="page">
      <header>
        <h1>AI Code Review Dashboard</h1>
        <p>Track PR review status, issues, and AI suggestions.</p>
      </header>

      {loading && <p>Loading reviews...</p>}
      {error && <p className="error">{error}</p>}
      <PRList prs={reviews} />
    </section>
  )
}
