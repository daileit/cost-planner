'use client'

import { useEffect, useState } from 'react'

interface CostPlan {
  id: string
  name: string
  status: string
  total_budget: number
  total_estimated_cost: number
  total_actual_cost: number
  remaining_budget: number
  created_at: string
}

export default function Home() {
  const [plans, setPlans] = useState<CostPlan[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

  useEffect(() => {
    fetchPlans()
  }, [])

  const fetchPlans = async () => {
    try {
      const response = await fetch(`${API_URL}/api/v1/cost-plans`)
      if (!response.ok) throw new Error('Failed to fetch plans')
      const data = await response.json()
      setPlans(data)
      setError(null)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred')
    } finally {
      setLoading(false)
    }
  }

  return (
    <main style={{ padding: '2rem', maxWidth: '1200px', margin: '0 auto' }}>
      <h1 style={{ marginBottom: '2rem' }}>💒 Wedding Cost Planner</h1>
      
      {loading && <p>Loading plans...</p>}
      {error && <p style={{ color: 'red' }}>Error: {error}</p>}
      
      {!loading && !error && plans.length === 0 && (
        <p>No cost plans yet. Create one using the API!</p>
      )}
      
      {!loading && !error && plans.length > 0 && (
        <div style={{ display: 'grid', gap: '1rem' }}>
          {plans.map((plan) => (
            <div
              key={plan.id}
              style={{
                border: '1px solid #ddd',
                borderRadius: '8px',
                padding: '1.5rem',
                backgroundColor: '#f9f9f9'
              }}
            >
              <h2 style={{ margin: '0 0 0.5rem 0' }}>{plan.name}</h2>
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1rem', marginTop: '1rem' }}>
                <div>
                  <strong>Status:</strong> {plan.status}
                </div>
                <div>
                  <strong>Total Budget:</strong> ${plan.total_budget.toFixed(2)}
                </div>
                <div>
                  <strong>Estimated Cost:</strong> ${plan.total_estimated_cost.toFixed(2)}
                </div>
                <div>
                  <strong>Actual Cost:</strong> ${plan.total_actual_cost.toFixed(2)}
                </div>
                <div>
                  <strong>Remaining:</strong> ${plan.remaining_budget.toFixed(2)}
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
      
      <div style={{ marginTop: '2rem', padding: '1rem', backgroundColor: '#f0f0f0', borderRadius: '4px' }}>
        <p><strong>API Endpoint:</strong> {API_URL}</p>
        <p><strong>Docs:</strong> <a href={`${API_URL}/docs`} target="_blank" rel="noopener noreferrer">{API_URL}/docs</a></p>
      </div>
    </main>
  )
}
