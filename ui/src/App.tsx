import { useEffect } from 'react'
import { AppStateProvider, useAppState } from './context/AppStateContext'
import SearchForm from './components/SearchForm'
import ResponseDisplay from './components/ResponseDisplay'
import { createIndex } from './services/api'

function AppContent() {
  const { dispatch } = useAppState()

  useEffect(() => {
    async function initIndex() {
      try {
        await createIndex()
        dispatch({ type: 'SET_INDEX_STATUS', payload: true })
      } catch {
        dispatch({
          type: 'SET_ERROR',
          payload: 'Failed to initialize the knowledge base. Please refresh.',
        })
      }
    }
    initIndex()
  }, [dispatch])

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col items-center justify-start pt-24 px-4 gap-6">
      <div className="text-center">
        <h1 className="text-3xl font-bold text-gray-900">Cadre AI</h1>
        <p className="mt-2 text-sm text-gray-500">
          Ask anything about our AI services and offerings.
        </p>
      </div>
      <SearchForm />
      <ResponseDisplay />
    </div>
  )
}

export default function App() {
  return (
    <AppStateProvider>
      <AppContent />
    </AppStateProvider>
  )
}
