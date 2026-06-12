export default function ReviewDetails({ review }) {
  if (!review) {
    return <p>Select a review to see details.</p>
  }

  return (
    <div className="details-card">
      <h2>{review.title || 'Review details'}</h2>
      <section>
        <h3>Summary</h3>
        <p>{review.summary || 'No summary yet.'}</p>
      </section>
      <section>
        <h3>Issues</h3>
        <ul>
          {review.issues?.map((issue, idx) => (
            <li key={idx}>{issue}</li>
          ))}
        </ul>
      </section>
      <section>
        <h3>Suggestions</h3>
        <ul>
          {review.suggestions?.map((suggestion, idx) => (
            <li key={idx}>{suggestion}</li>
          ))}
        </ul>
      </section>
    </div>
  )
}
