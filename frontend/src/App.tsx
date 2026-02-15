/* ── App Entry — React Router Setup ── */

import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import UploadPage from './routes/UploadPage';
import AnalysisPage from './routes/AnalysisPage';
import GeneratePage from './routes/GeneratePage';
import './index.css';

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<Layout />}>
          <Route path="/" element={<UploadPage />} />
          <Route path="/analysis" element={<AnalysisPage />} />
          <Route path="/generate" element={<GeneratePage />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}
