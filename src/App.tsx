import { BrowserRouter as Router, Routes, Route } from "react-router-dom"
import LandingPage from "./pages/LandingPage"
import LoginPage from "./pages/auth/LoginPage"
import SignupPage from "./pages/auth/SignupPage"
import { DashboardLayout } from "./components/dashboard/DashboardLayout"
import DashboardHome from "./pages/dashboard/DashboardHome"
import GenerateNotes from "./pages/dashboard/GenerateNotes"
import GenerateAssignments from "./pages/dashboard/GenerateAssignments"
import GenerateFlashcards from "./pages/dashboard/GenerateFlashcards"
import { ProtectedRoute } from "./components/auth/ProtectedRoute"

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/signup" element={<SignupPage />} />

        <Route element={<ProtectedRoute />}>
          <Route path="/dashboard" element={<DashboardLayout />}>
            <Route index element={<DashboardHome />} />
            <Route path="notes" element={<GenerateNotes />} />
            <Route path="assignments" element={<GenerateAssignments />} />
            <Route path="flashcards" element={<GenerateFlashcards />} />
          </Route>
        </Route>
      </Routes>
    </Router>
  )
}

export default App
