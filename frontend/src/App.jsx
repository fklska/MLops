import { useState, useEffect } from 'react'

const API_BASE_URL = 'https://fklska.asuscomm.com:48888/backend'

export default function App() {
  const [reviews, setReviews] = useState([])
  const [filmTitle, setFilmTitle] = useState('')
  const [filmYear, setFilmYear] = useState('')
  const [filmDesc, setFilmDesc] = useState('')
  
  const [revTitle, setRevTitle] = useState('')
  const [revDesc, setRevDesc] = useState('')
  const [revFilmName, setRevFilmName] = useState('')

  const [message, setMessage] = useState('')

  const fetchReviews = async () => {
    try {
      const res = await fetch(`${API_BASE_URL}/reviews/`)
      if (res.ok) {
        const data = await res.json()
        setReviews(data.reviews || [])
      }
    } catch (err) {
      console.error(err)
    }
  }

  useEffect(() => {
    fetchReviews()
    const interval = setInterval(fetchReviews, 5000)
    return () => clearInterval(interval)
  }, [])

  const handleCreateFilm = async (e) => {
    e.preventDefault()
    try {
      const res = await fetch(`${API_BASE_URL}/films/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title: filmTitle, year: parseInt(filmYear), description: filmDesc })
      })
      if (res.ok) {
        setMessage('Фильм успешно создан')
        setFilmTitle('')
        setFilmYear('')
        setFilmDesc('')
      } else {
        setMessage('Ошибка создания фильма')
      }
    } catch (err) {
      setMessage('Ошибка подключения')
    }
  }

  const handleCreateReview = async (e) => {
    e.preventDefault()
    try {
      const res = await fetch(`${API_BASE_URL}/reviews/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title: revTitle, description: revDesc, film_name: revFilmName })
      })
      if (res.ok) {
        setMessage('Ревью успешно отправлено')
        setRevTitle('')
        setRevDesc('')
        setRevFilmName('')
        fetchReviews()
      } else {
        setMessage('Ошибка создания ревью')
      }
    } catch (err) {
      setMessage('Ошибка подключения')
    }
  }

  const handleStartTrain = async () => {
    try {
      const res = await fetch(`${API_BASE_URL}/train/`, { method: 'POST' })
      if (res.ok) {
        setMessage('Задача переобучения запущена')
      } else {
        setMessage('Ошибка запуска переобучения')
      }
    } catch (err) {
      setMessage('Ошибка подключения')
    }
  }

  const getCardBg = (label) => {
    if (!label) return 'bg-white'
    const l = label.toUpperCase()
    if (l.includes('POSITIVE')) return 'bg-green-100 border-green-400'
    if (l.includes('NEGATIVE')) return 'bg-red-100 border-red-400'
    return 'bg-yellow-100 border-yellow-400'
  }

  return (
    <div class="container mx-auto p-4 max-w-6xl">
      <header class="flex justify-between items-center mb-6 pb-4 border-b">
        <h1 class="text-3xl font-bold text-gray-800">КиноОтзыв Аналитика</h1>
        <button onClick={handleStartTrain} class="bg-indigo-600 hover:bg-indigo-700 text-white font-semibold py-2 px-4 rounded shadow">
          Запустить переобучение
        </button>
      </header>

      {message && (
        <div class="mb-4 p-3 bg-blue-50 text-blue-700 border border-blue-200 rounded">
          {message}
        </div>
      )}

      <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
        <div class="bg-white p-6 rounded shadow">
          <h2 class="text-xl font-semibold mb-4">Создать фильм</h2>
          <form onSubmit={handleCreateFilm} class="space-y-3">
            <input type="text" placeholder="Название фильма" value={filmTitle} onChange={e => setFilmTitle(e.target.value)} required class="w-full p-2 border rounded" />
            <input type="number" placeholder="Год" value={filmYear} onChange={e => setFilmYear(e.target.value)} required class="w-full p-2 border rounded" />
            <textarea placeholder="Описание" value={filmDesc} onChange={e => setFilmDesc(e.target.value)} required class="w-full p-2 border rounded h-20"></textarea>
            <button type="submit" class="w-full bg-green-600 hover:bg-green-700 text-white p-2 rounded font-medium">Добавить фильм</button>
          </form>
        </div>

        <div class="bg-white p-6 rounded shadow">
          <h2 class="text-xl font-semibold mb-4">Создать ревью</h2>
          <form onSubmit={handleCreateReview} class="space-y-3">
            <input type="text" placeholder="Точное название фильма" value={revFilmName} onChange={e => setRevFilmName(e.target.value)} required class="w-full p-2 border rounded" />
            <input type="text" placeholder="Заголовок ревью" value={revTitle} onChange={e => setRevTitle(e.target.value)} required class="w-full p-2 border rounded" />
            <textarea placeholder="Текст отзыва" value={revDesc} onChange={e => setRevDesc(e.target.value)} required class="w-full p-2 border rounded h-20"></textarea>
            <button type="submit" class="w-full bg-blue-600 hover:bg-blue-700 text-white p-2 rounded font-medium">Отправить ревью</button>
          </form>
        </div>
      </div>

      <h2 class="text-2xl font-bold mb-4 text-gray-800">Лента последних 100 отзывов</h2>
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        {reviews.map((rev) => (
          <div key={rev.id} class={`p-4 rounded shadow border-l-4 flex flex-col justify-between ${getCardBg(rev.label)}`}>
            <div>
              <div class="text-xs text-gray-500 mb-1">Film ID: {rev.film_id}</div>
              <h3 class="text-lg font-bold mb-2 text-gray-900">{rev.title}</h3>
              <p class="text-sm text-gray-700 mb-4 line-clamp-4">{rev.description}</p>
            </div>
            <div class="pt-2 border-t border-gray-200/50 text-xs text-gray-600 space-y-1">
              <div>Метка: <span class="font-bold">{rev.label || 'Отсутствует'}</span></div>
              <div>Статус: <span class="font-semibold">{rev.status}</span></div>
              <div>Уверенность: <span class="font-mono">{rev.probability !== null && rev.probability !== undefined ? (rev.probability * 100).toFixed(1) + '%' : 'н/д'}</span></div>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}