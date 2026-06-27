import { FormEvent, useState } from 'react'
import { useAppState } from '../context/AppStateContext'
import { queryKnowledgeBase } from '../services/api'

export default function SearchForm() {
  const { state, dispatch } = useAppState()
  const [question, setQuestion] = useState('')

  async function handleSubmit(e: FormEvent) {
    e.preventDefault()
    if (!question.trim() || state.loading) return

    dispatch({ type: 'START_QUERY' })
    try {
      const response = await queryKnowledgeBase(question.trim())
      dispatch({ type: 'SET_QUERY_RESPONSE', payload: response })
    } catch (err) {
      dispatch({
        type: 'SET_ERROR',
        payload: err instanceof Error ? err.message : 'An unexpected error occurred.',
      })
    }
  }

  return (
    <form onSubmit={handleSubmit} className="flex gap-2 w-full max-w-2xl">
      <input
        type="text"
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        placeholder="Ask a question about Cadre AI…"
        disabled={state.loading}
        className="flex-1 rounded-lg border border-gray-300 px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-100"
      />
      <button
        type="submit"
        disabled={state.loading || !question.trim()}
        className="rounded-lg bg-blue-600 px-5 py-2 text-sm font-medium text-white hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
      >
        {state.loading ? 'Searching…' : 'Search'}
      </button>
    </form>
  )
}
