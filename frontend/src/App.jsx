import { useEffect, useState } from 'react'
import CytoscapeComponent from 'react-cytoscapejs'

const API_URL = 'http://localhost:8000/fraud-rings'

function ringsToElements(rings) {
  const seenNodes = new Set()
  const elements = []

  rings.forEach((ring, ringIndex) => {
    ring.accounts.forEach((id) => {
      if (!seenNodes.has(id)) {
        seenNodes.add(id)
        elements.push({ data: { id } })
      }
    })
    ring.transfers.forEach((transfer, i) => {
      elements.push({
        data: {
          id: `${ringIndex}-${i}`,
          source: transfer.source,
          target: transfer.target,
          amount: transfer.amount,
        },
      })
    })
  })

  return elements
}

const stylesheet = [
  {
    selector: 'node',
    style: {
      label: 'data(id)',
      'background-color': '#d64545',
      color: '#222',
      'font-size': 10,
      width: 28,
      height: 28,
    },
  },
  {
    selector: 'edge',
    style: {
      width: 2,
      'line-color': '#999',
      'target-arrow-color': '#999',
      'target-arrow-shape': 'triangle',
      'curve-style': 'bezier',
    },
  },
]

function App() {
  const [elements, setElements] = useState(null)
  const [error, setError] = useState(null)

  useEffect(() => {
    fetch(API_URL)
      .then((res) => res.json())
      .then((data) => setElements(ringsToElements(data.rings)))
      .catch((err) => setError(err.message))
  }, [])

  return (
    <div>
      <h1>Fraud Rings</h1>
      {error && <p>Failed to load fraud rings: {error}</p>}
      {!error && elements === null && <p>Loading...</p>}
      {!error && elements !== null && elements.length === 0 && (
        <p>No fraud rings detected.</p>
      )}
      {!error && elements !== null && elements.length > 0 && (
        <CytoscapeComponent
          elements={elements}
          stylesheet={stylesheet}
          layout={{ name: 'cose' }}
          style={{ width: '100%', height: '600px', textAlign: 'left' }}
        />
      )}
    </div>
  )
}

export default App
