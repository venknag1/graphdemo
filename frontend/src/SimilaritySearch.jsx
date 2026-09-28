import { useEffect, useState } from 'react'

const API_BASE = 'http://localhost:8000'

function SimilaritySearch() {
  const [accounts, setAccounts] = useState([])
  const [selectedAccount, setSelectedAccount] = useState('')
  const [metric, setMetric] = useState('cosine')
  const [results, setResults] = useState(null)
  const [error, setError] = useState(null)

  useEffect(() => {
    fetch(`${API_BASE}/accounts`)
      .then((res) => res.json())
      .then((data) => {
        setAccounts(data.accounts)
        setSelectedAccount(data.accounts[0] ?? '')
      })
      .catch((err) => setError(err.message))
  }, [])

  const handleSearch = () => {
    setError(null)
    fetch(`${API_BASE}/similar-accounts/${selectedAccount}?metric=${metric}`)
      .then((res) => res.json())
      .then((data) => setResults(data.similar))
      .catch((err) => setError(err.message))
  }

  return (
    <section>
      <h2>Similar Account Search</h2>
      <p>
        Each account&apos;s embedding is 6 real statistics computed from its
        actual transfers (in/out-degree, amounts sent/received), searched
        via Neo4j&apos;s vector index. Fraud-ring accounts often surface as
        each other&apos;s closest matches - but not always, since a normal
        account can occasionally share a similar transfer pattern by chance.
        Cosine compares direction only; Euclidean compares direction and
        magnitude, so the two can rank results differently.
      </p>

      <select value={selectedAccount} onChange={(e) => setSelectedAccount(e.target.value)}>
        {accounts.map((id) => (
          <option key={id} value={id}>
            {id}
          </option>
        ))}
      </select>

      <label>
        <input
          type="radio"
          name="metric"
          value="cosine"
          checked={metric === 'cosine'}
          onChange={() => setMetric('cosine')}
        />
        Cosine
      </label>
      <label>
        <input
          type="radio"
          name="metric"
          value="euclidean"
          checked={metric === 'euclidean'}
          onChange={() => setMetric('euclidean')}
        />
        Euclidean
      </label>

      <button type="button" onClick={handleSearch}>
        Find Similar
      </button>

      {error && <p>Failed to search: {error}</p>}

      {results && (
        <table>
          <thead>
            <tr>
              <th>Account</th>
              <th>Score</th>
            </tr>
          </thead>
          <tbody>
            {results.map((r) => (
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

export default SimilaritySearch
