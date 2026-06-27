export interface QueryResponse {
  answer: string
  sources: string[]
}

export interface IndexResponse {
  indexed: number
  message: string
}

export async function createIndex(): Promise<IndexResponse> {
  const health = await fetch(`/health`, { method: 'GET' })
  console.log("REsponse from createIndex:", health);
  const res = await fetch('/v1/create-index', { 
    method: 'POST',
    headers: {
      "Content-Type": "application/json",
    },
  })
  if (!res.ok) throw new Error('Failed to initialize knowledge base.')
  return res.json() as Promise<IndexResponse>
}

export async function queryKnowledgeBase(question: string): Promise<QueryResponse> {
  const res = await fetch('/v1/query', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ question }),
  })
  if (!res.ok) {
    const body = await res.json().catch(() => ({})) as { detail?: string }
    throw new Error(body.detail ?? 'Request failed.')
  }
  return res.json() as Promise<QueryResponse>
}
