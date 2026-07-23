export default function ReviewDetails({ review }) {
  if (!review) {
    return <p>Select a review to see details.</p>
  }

  const renderList = (items) => {
    if (!items || items.length === 0) return <p>None found.</p>
    return (
      <ul>
        {items.map((it, idx) => (
          <li key={idx} style={{marginBottom: 8}}>
            <div style={{fontWeight: 600}}>{it.issue || it}</div>
            {it.file && <div style={{color: '#666'}}>{it.file}:{it.line ?? '?'}</div>}
            {it.suggestion && <div style={{marginTop: 4}}><strong>Fix:</strong> {it.suggestion}</div>}
          </li>
        ))}
      </ul>
    )
  }

  return (
    <div className="details-card">
      <h2>{review.title || 'Review details'}</h2>
      <section>
        <h3>Summary</h3>
        <p>{review.summary || 'No summary yet.'}</p>
      </section>

      <section>
        <h3>Security Issues</h3>
        {renderList(review.security)}
      </section>

      <section>
        <h3>Code Smells</h3>
        {renderList(review.smells)}
      </section>

      <section>
        <h3>Naming Issues</h3>
        {renderList(review.naming)}
      </section>

      <section>
        <h3>Suggestions</h3>
        {review.suggestions && review.suggestions.length > 0 ? (
          <ol>
            {review.suggestions.map((s, i) => <li key={i}>{s}</li>)}
          </ol>
        ) : <p>None</p>}
      </section>

      <section>
        <h3>Meta</h3>
        <p>Score: {review.review_score ?? review.reviewScore ?? '—'}/100</p>
        <p>Model: {review.model}</p>
        <p>Time: {review.processing_time}</p>
      </section>
    </div>
  )
}
