import React from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import Login from './components/Login';
import Register from './components/Register';
import Dashboard from './components/Dashboard';
import AccountDetails from './components/AccountDetails';
import Transfer from './components/Transfer';

function App() {
    return (
        <Router>
            <Routes>
                <Route path="/" element={<Navigate replace to="/login" />} />
                <Route path="/login" element={<Login />} />
                <Route path="/register" element={<Register />} />
                <Route path="/dashboard" element={<Dashboard />} />
                <Route path="/account/:id" element={<AccountDetails />} />
                <Route path="/transfer" element={<Transfer />} />
            </Routes>
        </Router>
    );
}

export default App;
