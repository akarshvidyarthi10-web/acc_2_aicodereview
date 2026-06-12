import ReviewCard from './ReviewCard'

export default function PRList({ prs }) {
  if (!prs?.length) {
    return <p>No PR reviews available yet.</p>
  }

  return (
    <div className="grid">
      {prs.map((pr) => (
        <ReviewCard key={pr.id ?? pr.pull_request_number} review={pr} />
      ))}
    </div>
  )
}
