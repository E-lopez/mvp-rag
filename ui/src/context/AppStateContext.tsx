import { createContext, useContext, useReducer, ReactNode } from 'react'

interface AppState {
  loading: boolean
  indexCreated: boolean
  answer: string | null
  sources: string[]
  error: string | null
}

type AppAction =
  | { type: 'START_QUERY' }
  | { type: 'SET_QUERY_RESPONSE'; payload: { answer: string; sources: string[] } }
  | { type: 'SET_INDEX_STATUS'; payload: boolean }
  | { type: 'SET_ERROR'; payload: string }

const initialState: AppState = {
  loading: false,
  indexCreated: false,
  answer: null,
  sources: [],
  error: null,
}

function appReducer(state: AppState, action: AppAction): AppState {
  switch (action.type) {
    case 'START_QUERY':
      return { ...state, loading: true, answer: null, sources: [], error: null }
    case 'SET_QUERY_RESPONSE':
      return { ...state, loading: false, answer: action.payload.answer, sources: action.payload.sources }
    case 'SET_INDEX_STATUS':
      return { ...state, indexCreated: action.payload }
    case 'SET_ERROR':
      return { ...state, loading: false, error: action.payload }
  }
}

interface AppStateContextValue {
  state: AppState
  dispatch: React.Dispatch<AppAction>
}

const AppStateContext = createContext<AppStateContextValue | null>(null)

export function AppStateProvider({ children }: { children: ReactNode }) {
  const [state, dispatch] = useReducer(appReducer, initialState)
  return (
    <AppStateContext.Provider value={{ state, dispatch }}>
      {children}
    </AppStateContext.Provider>
  )
}

export function useAppState() {
  const ctx = useContext(AppStateContext)
  if (!ctx) throw new Error('useAppState must be used within AppStateProvider')
  return ctx
}
