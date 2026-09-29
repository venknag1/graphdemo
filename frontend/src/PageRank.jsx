import { useState } from 'react'

const API_BASE = 'http://localhost:8000'

function PageRank() {
  const [ranking, setRanking] = useState(null)
  const [error, setError] = useState(null)

  const handleRun = () => {
    setError(null)
    fetch(`${API_BASE}/pagerank`)
      .then((res) => res.json())
      .then((data) => setRanking(data.ranking))
      .catch((err) => setError(err.message))
  }

  return (
    <section>
      <h2>PageRank</h2>
      <p>
        Ranks accounts by importance: an account scores higher when money
        flows in from other important accounts. Note it tends to favor
        ordinary accounts that receive a lot but never send onward, rather
        than the fraud rings - which is why fraud-ring detection here uses
        a dedicated cycle-detection query instead of PageRank.
      </p>

      <button type="button" onClick={handleRun}>
        Run PageRank
      </button>

      {error && <p>Failed to run PageRank: {error}</p>}

      {ranking && (
        <table>
          <thead>
            <tr>
              <th>Account</th>
              <th>Score</th>
            </tr>
          </thead>
          <tbody>
            {ranking.map((r) => (
              <tr key={r.account}>
                <td>{r.account}</td>
                <td>{r.score.toFixed(4)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </section>
  )
}

export default PageRank
