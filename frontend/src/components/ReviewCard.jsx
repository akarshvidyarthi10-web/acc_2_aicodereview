export default function ReviewCard({ review }) {
  const securityCount = (review.security || []).length
  const smellCount = (review.smells || []).length
  const namingCount = (review.naming || []).length
  const suggestionCount = (review.suggestions || []).length

  const previewItem = (review.security && review.security[0]) || (review.smells && review.smells[0]) || (review.naming && review.naming[0])

  return (
    <div className="card">
      <h3>{review.title || 'PR Review'}</h3>
      <p>Status: {review.status || 'completed'}</p>
      <p><strong>Score:</strong> {review.review_score ?? review.reviewScore ?? '—'}/100</p>
      <div style={{display: 'flex', gap: '12px', marginTop: 8}}>
        <small>Security: {securityCount}</small>
        <small>Smells: {smellCount}</small>
        <small>Naming: {namingCount}</small>
        <small>Suggestions: {suggestionCount}</small>
      </div>

      {previewItem && (
        <div style={{marginTop: 8}}>
          <strong>Top finding:</strong>
          <div>{previewItem.issue || previewItem}</div>
          <div style={{color: '#666', fontSize: 12}}>{previewItem.file ? `${previewItem.file}:${previewItem.line || '?'} — ${previewItem.severity || ''}` : ''}</div>
        </div>
      )}

      {review.summary && (
        <div style={{marginTop: 8}}>
          <em>{review.summary}</em>
        </div>
      )}
    </div>
  )
}
