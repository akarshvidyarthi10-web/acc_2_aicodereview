export default function ReviewCard({ review }) {
  return (
    <div className="card">
      <h3>{review.title || 'PR Review'}</h3>
      <p>Status: {review.status || 'pending'}</p>
      <p>Issues: {review.issues?.length ?? 0}</p>
    </div>
  )
}
